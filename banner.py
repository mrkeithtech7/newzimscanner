# language: Python 3.10+, file: banner.py
"""Banner + ANSI colors — KEITH TECH SCANNER."""
import os
import sys

_USE_COLOR = (
    os.environ.get("NO_COLOR") is None
    and os.environ.get("TERM", "") not in ("", "dumb")
    and sys.stdout.isatty()
)

R    = "\033[1;91m" if _USE_COLOR else ""
G    = "\033[1;92m" if _USE_COLOR else ""
Y    = "\033[1;93m" if _USE_COLOR else ""
B    = "\033[1;94m" if _USE_COLOR else ""
M    = "\033[1;95m" if _USE_COLOR else ""
C    = "\033[1;96m" if _USE_COLOR else ""
W    = "\033[1;97m" if _USE_COLOR else ""
DIM  = "\033[2m"    if _USE_COLOR else ""
BOLD = "\033[1m"    if _USE_COLOR else ""
END  = "\033[0m"    if _USE_COLOR else ""

SKULL = r"""
                    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
                ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
              ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
           ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
          ▓▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓  ▓▓  ▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓▓▓▓▓▓
          ▓▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓  ▓▓  ▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓▓▓▓▓▓
          ▓▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓  ▓▓  ▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓▓▓▓▓▓
          ▓▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓  ▓▓  ▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓▓▓▓▓▓
          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ▓▓▓  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ▓▓▓▓▓  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
            ▓▓▓▓▓▓▓▓  ▓▓▓▓  ▓▓▓▓  ▓▓▓▓  ▓▓▓▓▓▓
            ▓▓▓▓▓▓▓▓  ▓▓▓▓  ▓▓▓▓  ▓▓▓▓  ▓▓▓▓▓▓
            ▓▓▓▓▓▓▓▓  ▓▓▓▓  ▓▓▓▓  ▓▓▓▓  ▓▓▓▓▓▓
              ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
                ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
                  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
"""

KEITH = r"""
 ██   ██ ███████ ██ ████████ ██   ██     ████████ ███████  ██████ ██   ██
 ██  ██  ██      ██    ██    ██   ██        ██    ██      ██      ██   ██
 █████   █████   ██    ██    ███████        ██    █████   ██      ███████
 ██  ██  ██      ██    ██    ██   ██        ██    ██      ██      ██   ██
 ██   ██ ███████ ██    ██    ██   ██        ██    ███████  ██████ ██   ██
"""

SUBTITLE = "          N E W   Z I M   S C A N N E R   ·   V 1 . 0"
HANDLE   = "              github.com/mrkeithtech7   ·   @mrkeith"


def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def show_banner() -> None:
    clear()
    print(f"{R}{SKULL}{END}")
    print(f"{R}{KEITH}{END}")
    print(f"{Y}{SUBTITLE}{END}")
    print(f"{C}{HANDLE}{END}")
    print(f"{DIM}     CIDR · TXT · SNI · Reverse-IP · Proxy · Subdomain{END}\n")


def ok(msg: str) -> None:    print(f"{G}[+]{END} {msg}")
def warn(msg: str) -> None:  print(f"{Y}[~]{END} {msg}")
def err(msg: str) -> None:   print(f"{R}[!]{END} {msg}")
def info(msg: str) -> None:  print(f"{C}[i]{END} {msg}")
def dim(msg: str) -> None:   print(f"{DIM}    {msg}{END}")
