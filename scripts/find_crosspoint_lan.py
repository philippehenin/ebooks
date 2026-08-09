#!/usr/bin/env python3
"""
LAN Scanner for CrossPoint Reader X4
====================================
Scans 192.168.128.0/23 to locate the active IP address of the Xteink X4 CrossPoint Web Server.
"""

import socket
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

SUBNET_RANGES = [
    f"192.168.128.{i}" for i in range(1, 255)
] + [
    f"192.168.129.{i}" for i in range(1, 255)
] + [
    f"192.168.4.{i}" for i in range(1, 20)  # Check default ESP SoftAP range too
]

PORTS = [80, 8080, 8000, 8081]

def probe_ip(ip):
    found = []
    for port in PORTS:
        # Fast socket connect check first
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)
        res = s.connect_ex((ip, port))
        s.close()

        if res == 0:
            # Port is open! Probe HTTP response
            url = f"http://{ip}:{port}" if port != 80 else f"http://{ip}"
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=1.0) as resp:
                    body = resp.read(2048).decode('utf-8', errors='ignore')
                    found.append((ip, port, url, body))
            except Exception as e:
                found.append((ip, port, url, str(e)))
    return found

def main():
    print(f"🔎 Scanning LAN ({len(SUBNET_RANGES)} IPs) for CrossPoint Reader X4 Web Server...")
    discovered = []

    with ThreadPoolExecutor(max_workers=64) as executor:
        futures = {executor.submit(probe_ip, ip): ip for ip in SUBNET_RANGES}
        for future in as_completed(futures):
            results = future.result()
            if results:
                for ip, port, url, body_snippet in results:
                    print(f"✨ Found active HTTP service: {url}")
                    if "crosspoint" in body_snippet.lower() or "upload" in body_snippet.lower() or "epub" in body_snippet.lower() or "x4" in body_snippet.lower():
                        print(f"🎯 CONFIRMED CROSSPOINT X4 DEVICE AT: {url}")
                    discovered.append((ip, port, url))

    if not discovered:
        print("⚠️ No active HTTP web servers discovered on LAN yet.")
        print("Tips: Ensure Wi-Fi is turned ON on your X4 screen and connected to the same Wi-Fi network.")
    else:
        print(f"\nDiscovered {len(discovered)} active HTTP services.")

if __name__ == '__main__':
    main()
