# language: Python 3.10+, file: main.py
"""KEITH TECH SCANNER V1.0 — authorized diagnostics menu."""
import asyncio
import os
import sys

import banner
from banner import R, Y, C, DIM, END

HERE = os.path.dirname(os.path.abspath(__file__))


def _ask(prompt: str, default: str = "") -> str:
    try:
        v = input(f"{C}{prompt}{END}").strip()
    except (EOFError, KeyboardInterrupt):
        return ""
    return v or default


def _read_lines_paste() -> list[str]:
    print(f"{DIM}  paste one per line. Blank line = done.{END}")
    out: list[str] = []
    while True:
        try:
            line = input().strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not line:
            break
        if line.startswith("#"):
            continue
        out.append(line)
    return out


def _looks_like_ip(s: str) -> bool:
    parts = s.split(".")
    if len(parts) != 4:
        return False
    try:
        for p in parts:
            if not 0 <= int(p) <= 255:
                return False
        return True
    except ValueError:
        return False


def opt_cidr_scan():
    banner.clear()
    print(f"{R}  ── IP / CIDR SCANNER ──{END}\n")

    src = _ask("  source [1] paste   [2] file: ", "1")
    if src == "2":
        path = _ask("  file path: ")
        if not os.path.isfile(path):
            banner.err("file not found"); return
        from scanner import load_file
        specs = load_file(path)
    else:
        specs = _read_lines_paste()

    if not specs:
        banner.warn("nothing to scan"); return

    port = int(_ask("  port [443]: ", "443") or "443")
    mode = _ask("  mode [1] tcp-only   [2] full TLS+HTTP: ", "2")
    conc = int(_ask("  concurrency [32]: ", "32") or "32")
    to   = float(_ask("  timeout seconds [6]: ", "6") or "6")

    sni = None
    full_tls = False
    if mode == "2":
        sni = _ask("  SNI (host header / cert name): ", "cloudflare.com")
        full_tls = True

    print()
    try:
        from scanner import scan_cidrs
        asyncio.run(scan_cidrs(specs, port, sni, concurrency=conc,
                                timeout=to, full_tls=full_tls))
    except KeyboardInterrupt:
        print(f"\n{Y}[~]{END} interrupted")


def opt_reverse_ip():
    banner.clear()
    print(f"{R}  ── REVERSE IP ──{END}\n")
    ip = _ask("  IP: ")
    if not ip:
        return
    banner.info(f"querying reverse for {ip}")
    from tools import reverse_ip
    hits = reverse_ip(ip)
    if not hits:
        banner.warn("no domains found"); return
    print(f"\n{banner.G}[+]{END} {len(hits)} domains:")
    for h in hits:
        print(f"    {banner.G}{h}{END}")


def opt_subdomain():
    banner.clear()
    print(f"{R}  ── SUBDOMAIN SCANNER ──{END}\n")
    domain = _ask("  domain (e.g. example.com): ")
    if not domain:
        return
    banner.info(f"probing common subdomains for {domain}")
    print()
    from tools import subdomain_scan
    live = subdomain_scan(domain)
    print(f"\n{banner.G}[+]{END} {len(live)} live")


def opt_txt_file():
    banner.clear()
    print(f"{R}  ── TXT FILE SCAN ──{END}\n")
    path = _ask("  file path: ")
    if not path or not os.path.isfile(path):
        banner.err("file not found"); return

    from scanner import load_file
    hosts = load_file(path)
    if not hosts:
        banner.warn("empty"); return
    banner.info(f"{len(hosts)} entries loaded")

    kind = _ask("  type [1] domains   [2] IPs/CIDRs: ", "2")
    port = int(_ask("  port [443]: ", "443") or "443")
    conc = int(_ask("  concurrency [32]: ", "32") or "32")
    to   = float(_ask("  timeout [8]: ", "8") or "8")

    if kind == "2":
        specs = []
        for h in hosts:
            specs.append(h if "/" in h else (f"{h}/32" if _looks_like_ip(h) else h))
        sni = _ask("  SNI (blank for tcp-only): ")
        try:
            from scanner import scan_cidrs
            asyncio.run(scan_cidrs(specs, port, sni or None,
                                    concurrency=conc, timeout=to,
                                    full_tls=bool(sni)))
        except KeyboardInterrupt:
            print(f"\n{Y}[~]{END} interrupted")
        return

    # domains — resolve each, scan /32
    import socket
    specs = []
    for h in hosts:
        try:
            specs.append(f"{socket.gethostbyname(h)}/32")
        except Exception:
            pass
    if not specs:
        banner.warn("nothing resolvable"); return
    sni = _ask("  SNI (blank = tcp-only): ")
    try:
        from scanner import scan_cidrs
        asyncio.run(scan_cidrs(specs, port, sni or None,
                                concurrency=conc, timeout=to,
                                full_tls=bool(sni)))
    except KeyboardInterrupt:
        print(f"\n{Y}[~]{END} interrupted")


def opt_proxy():
    banner.clear()
    print(f"{R}  ── PROXY CHECK ──{END}\n")
    src = _ask("  source [1] paste   [2] file: ", "1")
    if src == "2":
        path = _ask("  file path: ")
        if not os.path.isfile(path):
            banner.err("file not found"); return
        from scanner import load_file
        proxies = load_file(path)
    else:
        proxies = _read_lines_paste()
    if not proxies:
        return
    print()
    from tools import proxy_check
    for p in proxies:
        r = proxy_check(p)
        if r["ok"]:
            print(f"    {banner.G}✓{END} {p:<24} → {r['ip']:<16} "
                  f"{r['ms']:.0f}ms")
        else:
            print(f"    {banner.R}✗{END} {p:<24} {DIM}{r['err']}{END}")


def opt_hostname():
    banner.clear()
    print(f"{R}  ── HOSTNAME → IP ──{END}\n")
    h = _ask("  hostname: ")
    if not h:
        return
    from tools import hostname_to_ip
    from cidrs import cdn_for_ip
    ips = hostname_to_ip(h)
    if not ips:
        banner.warn("no records"); return
    for ip in ips:
        cdn = cdn_for_ip(ip) or "-"
        col = C if cdn != "-" else DIM
        print(f"    {banner.G}{ip:<16}{END} {col}{cdn}{END}")



MENU = [
    ("1", "IP / CIDR scanner       — TCP or TLS+HTTP, custom port"),
    ("2", "Reverse IP scanner      — domains behind an IP"),
    ("3", "Subdomain scanner       — quick wordlist probe"),
    ("4", "TXT file scan           — bulk domains or IPs from file"),
    ("5", "Proxy checker           — HTTP proxy reachability"),
    ("6", "Hostname → IP           — with CDN identification"),
    ("7", "Exit"),
]


def loop():
    while True:
        banner.show_banner()
        for k, label in MENU:
            print(f"  {R}[{k}]{END} {label}")
        print()
        try:
            choice = input(f"{C}  Select an option (1-7): {END}").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{DIM}  bye.{END}\n")
            return

        try:
            if   choice == "1": opt_cidr_scan()
            elif choice == "2": opt_reverse_ip()
            elif choice == "3": opt_subdomain()
            elif choice == "4": opt_txt_file()
            elif choice == "5": opt_proxy()
            elif choice == "6": opt_hostname()
            elif choice == "7": opt_domain_sni()
            elif choice == "8": opt_sni_flow()
            elif choice in ("7", "q", "exit"):
                print(f"\n{DIM}  bye.{END}\n"); return
            else:
                banner.warn("unknown option")
        except KeyboardInterrupt:
            print(f"\n{Y}[~]{END} cancelled")
        except Exception as e:
            print(f"\n{banner.R}[!]{END} {type(e).__name__}: {e}")

        try:
            input(f"\n{DIM}  [enter] to return{END}")
        except (EOFError, KeyboardInterrupt):
            return


if __name__ == "__main__":
    try:
        loop()
    except KeyboardInterrupt:
        print(f"\n\n{DIM}  bye.{END}\n")
