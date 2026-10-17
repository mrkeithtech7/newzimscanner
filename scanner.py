# language: Python 3.10+, file: scanner.py
"""Async CIDR/TXT scanner. Streams hits as they land."""
import asyncio
import ipaddress
import ssl
import sys
import time

from cidrs import cdn_for_ip

_USE_COLOR = sys.stdout.isatty()
R = "\033[1;91m" if _USE_COLOR else ""
G = "\033[1;92m" if _USE_COLOR else ""
Y = "\033[1;93m" if _USE_COLOR else ""
M = "\033[1;95m" if _USE_COLOR else ""
C = "\033[1;96m" if _USE_COLOR else ""
D = "\033[2m"    if _USE_COLOR else ""
E = "\033[0m"    if _USE_COLOR else ""

UA = ("Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 "
      "Chrome/120 Mobile Safari/537.36")


def _status_color(code: int | None) -> str:
    if code == 200:                  return G
    if code in (301, 302, 307, 308): return Y
    if code == 401:                  return M
    if code and 400 <= code < 500:   return R
    if code and code >= 500:         return R
    return D


MAX_TARGETS = 256

def expand_cidr(cidr: str, cap: int = MAX_TARGETS) -> list[str]:
    """Expand only small explicit ranges; never silently truncate a network."""
    net = ipaddress.ip_network(cidr, strict=False)
    host_count = net.num_addresses
    if net.version == 4 and net.prefixlen < 31:
        host_count -= 2
    if host_count > min(cap, MAX_TARGETS):
        raise ValueError(f"range exceeds the {MAX_TARGETS}-address safety limit")
    hosts = list(net.hosts())
    return [str(h) for h in hosts]


async def _tcp(ip: str, port: int, timeout: float) -> bool:
    try:
        r, w = await asyncio.wait_for(
            asyncio.open_connection(ip, port), timeout=timeout)
        w.close()
        try: await w.wait_closed()
        except Exception: pass
        return True
    except Exception:
        return False


async def _tls_http(ip: str, port: int, sni: str, timeout: float) -> dict:
    out = {"status": None, "bytes": 0, "err": "", "ms": 0.0}
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    t0 = time.perf_counter()
    try:
        r, w = await asyncio.wait_for(
            asyncio.open_connection(ip, port, ssl=ctx, server_hostname=sni),
            timeout=timeout)
    except Exception as e:
        out["err"] = type(e).__name__
        out["ms"] = (time.perf_counter() - t0) * 1000
        return out
    try:
        req = (f"GET / HTTP/1.1\r\nHost: {sni}\r\n"
               f"User-Agent: {UA}\r\nAccept: */*\r\n"
               f"Connection: close\r\n\r\n")
        w.write(req.encode())
        await w.drain()
        data = await asyncio.wait_for(r.read(4096), timeout=timeout)
        out["bytes"] = len(data)
        if data:
            first = data.split(b"\r\n", 1)[0].decode("latin1", "replace")
            parts = first.split(" ")
            if len(parts) > 1 and parts[1].isdigit():
                out["status"] = int(parts[1])
    except Exception as e:
        out["err"] = type(e).__name__
    finally:
        try:
            w.close()
            await w.wait_closed()
        except Exception:
            pass
    out["ms"] = (time.perf_counter() - t0) * 1000
    return out


def _print_row(ip, status, ms, cdn, extra=""):
    cdn_col = C if cdn and cdn != "-" else D
    if status is None:
        st = f"{D}tcp-open{E}"
    else:
        st = f"{_status_color(status)}{status}{E}"
    print(f"    {G}{ip:<16}{E} {st:<18} {ms:>5.0f}ms  "
          f"{cdn_col}{cdn:<16}{E} {D}{extra}{E}")


async def scan_cidrs(cidrs, port, sni, concurrency=32, timeout=6.0,
                     full_tls=False):
    all_ips: list[str] = []
    try:
        for c in cidrs:
            all_ips.extend(expand_cidr(c))
            if len(all_ips) > MAX_TARGETS:
                raise ValueError(f"combined targets exceed {MAX_TARGETS} addresses")
    except ValueError as e:
        print(f"{R}[!]{E} scan refused: {e}")
        return {"total": 0, "open": 0, "tls_ok": 0}

    if not all_ips:
        return {"total": 0, "open": 0, "tls_ok": 0}

    print("Only scan systems you own or are explicitly authorized to test.")
    if input("Type AUTHORIZED to confirm permission and begin: ").strip() != "AUTHORIZED":
        print(f"{Y}[~]{E} cancelled")
        return {"total": 0, "open": 0, "tls_ok": 0}

    print(f"{C}[i]{E} {len(all_ips)} IPs · port {port} · "
          f"conc {concurrency} · timeout {timeout}s")
    if full_tls and sni:
        print(f"{C}[i]{E} TLS+HTTP mode · SNI={sni}")
    print(f"{D}    {'IP':<16} {'STATUS':<18} {'MS':<8} {'CDN':<16} INFO{E}")
    print(f"{D}    {'-'*78}{E}")

    sem = asyncio.Semaphore(concurrency)
    stats = {"total": len(all_ips), "open": 0, "tls_ok": 0}
    t0 = time.time()

    async def worker(ip: str):
        async with sem:
            ok = await _tcp(ip, port, timeout)
            if not ok:
                return
            stats["open"] += 1
            cdn = cdn_for_ip(ip) or "-"
            if not full_tls or not sni:
                _print_row(ip, None, 0, cdn, "tcp-open")
                return
            r = await _tls_http(ip, port, sni, timeout)
            if r["status"] is not None:
                stats["tls_ok"] += 1
            extra = f"{r['bytes']}B" if r["bytes"] else (r["err"] or "")
            _print_row(ip, r["status"], r["ms"], cdn, extra)

    tasks = [asyncio.create_task(worker(ip)) for ip in all_ips]
    try:
        await asyncio.gather(*tasks)
    except (KeyboardInterrupt, asyncio.CancelledError):
        for t in tasks:
            t.cancel()
        raise

    elapsed = time.time() - t0
    print(f"\n{G}[+]{E} done in {elapsed:.1f}s — "
          f"{stats['open']} open / {stats['total']} scanned"
          + (f" · {stats['tls_ok']} TLS-ok" if full_tls else ""))
    return stats


def load_file(path: str) -> list[str]:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return [ln.strip() for ln in f
                if ln.strip() and not ln.strip().startswith("#")]
