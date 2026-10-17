# language: Python 3.10+, file: tools.py
"""Extra tools: reverse IP, subdomain enum, proxy check, hostname resolve."""
import socket
import sys
import time
import urllib.request

from cidrs import cdn_for_ip

_USE_COLOR = sys.stdout.isatty()
R = "\033[1;91m" if _USE_COLOR else ""
G = "\033[1;92m" if _USE_COLOR else ""
Y = "\033[1;93m" if _USE_COLOR else ""
C = "\033[1;96m" if _USE_COLOR else ""
D = "\033[2m"    if _USE_COLOR else ""
E = "\033[0m"    if _USE_COLOR else ""

UA = ("Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 "
      "Chrome/120 Mobile Safari/537.36")


def reverse_ip(ip: str) -> list[str]:
    out: set[str] = set()
    try:
        req = urllib.request.Request(
            f"https://api.hackertarget.com/reverseiplookup/?q={ip}",
            headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=10) as r:
            text = r.read().decode("utf-8", "replace")
        if "No records" not in text and not text.lower().startswith("error"):
            for line in text.splitlines():
                h = line.strip()
                if h and " " not in h:
                    out.add(h)
    except Exception:
        pass
    try:
        ptr = socket.gethostbyaddr(ip)
        if ptr and ptr[0]:
            out.add(ptr[0])
    except Exception:
        pass
    return sorted(out)


def hostname_to_ip(host: str) -> list[str]:
    ips: set[str] = set()
    try:
        for info in socket.getaddrinfo(host, None):
            ips.add(info[4][0])
    except Exception:
        pass
    return sorted(ips)


def subdomain_scan(domain: str, words=None) -> list[str]:
    if words is None:
        words = [
            "www", "api", "cdn", "static", "assets", "media", "mail",
            "app", "admin", "m", "dev", "test", "staging", "portal",
            "auth", "login", "secure", "img", "files", "download",
            "vpn", "docs", "blog", "shop", "store", "help", "support",
            "ns1", "ns2", "mx", "smtp", "ftp", "db", "backup",
        ]
    live: list[str] = []
    for sub in words:
        host = f"{sub}.{domain}"
        ips = hostname_to_ip(host)
        if ips:
            cdn = cdn_for_ip(ips[0]) or "-"
            col = C if cdn != "-" else D
            print(f"    {G}{host:<40}{E} {ips[0]:<16} {col}{cdn}{E}")
            live.append(host)
    return live


def proxy_check(proxy: str) -> dict:
    out = {"ok": False, "ip": "", "ms": 0.0, "err": ""}
    from urllib.request import ProxyHandler, build_opener
    t0 = time.perf_counter()
    handler = ProxyHandler({"http": f"http://{proxy}",
                            "https": f"http://{proxy}"})
    opener = build_opener(handler)
    try:
        req = urllib.request.Request("https://api.ipify.org",
                                     headers={"User-Agent": UA})
        with opener.open(req, timeout=8) as r:
            out["ip"] = r.read().decode().strip()
            out["ok"] = True
    except Exception as e:
        out["err"] = type(e).__name__
    out["ms"] = (time.perf_counter() - t0) * 1000
    return out
