# KEITH TECH SCANNER V1.0

A lightweight, Termux-friendly network diagnostics utility for **systems you own or are explicitly authorized to test**. It includes bounded TCP/TLS checks, hostname resolution, CDN range identification, reverse-IP lookups, and basic subdomain checks. It uses Python's standard library.

Repository: <https://github.com/mrkeithtech7/newzimscanner>

## Safety and scope

- Every active scan requires typing `AUTHORIZED` at the prompt.
- A scan is limited to **256 IP addresses total**; larger or combined ranges are rejected (not silently truncated).
- Use only on systems for which you have clear permission. Respect provider policies and applicable law.
- This project does not include carrier zero-rating/bypass discovery or attempt to evade billing, access controls, or rate limits.
- Network operations can still generate traffic and may be logged by target systems.

## Install on Termux

```bash
pkg update -y
pkg install -y python git
git clone https://github.com/mrkeithtech7/newzimscanner.git
cd newzimscanner
bash install.sh
```

Then run:

```bash
python3 main.py
# Optional local launcher
./kts
```

## Menu

1. TCP or TLS+HTTP checks for a small list of authorized IPs/CIDRs.
2. Reverse-IP lookup (uses the HackerTarget public endpoint and DNS PTR).
3. Basic common-subdomain resolution for a domain you control or are authorized to assess.
4. Read a text file of authorized domains or IPs/CIDRs.
5. Check explicitly supplied HTTP proxies.
6. Resolve a hostname and identify known CDN ranges.
7. Test TLS/HTTP flow for a domain you control or are authorized to assess.
8. Exit.

CIDR entries are bounded to 256 total addresses per scan. Use `/32` for a single IPv4 host; IPv6 ranges are subject to the same address limit.

## Requirements

Python 3.10 or later. No third-party packages are required.

## License

MIT. See [LICENSE](LICENSE).
