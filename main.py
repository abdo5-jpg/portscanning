#!/usr/bin/env python3
"""
NetProbe - Advanced Port Scanner
"""

import argparse
import sys
from scanner.core import PortScanner
from gui.app import NetProbeApp
from scanner.utils import setup_logging

def cli_mode():
    parser = argparse.ArgumentParser(description="NetProbe Port Scanner")
    parser.add_argument("target", help="Target IP or hostname")
    parser.add_argument("-p", "--ports", type=str, default="1-1024")
    parser.add_argument("--common", action="store_true")
    parser.add_argument("-t", "--threads", type=int, default=200)

    args = parser.parse_args()
    scanner = PortScanner()
    
    if args.common:
        results = scanner.scan(args.target, use_common=True)
    else:
        start, end = map(int, args.ports.split('-'))
        results = scanner.scan(args.target, start, end, threads=args.threads)

if __name__ == "__main__":
    setup_logging()
    if len(sys.argv) > 1:
        cli_mode()
    else:
        print("🚀 Starting GUI...")
        app = NetProbeApp()
        app.root.mainloop()