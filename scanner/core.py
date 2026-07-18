import socket
import threading
import time
import random
from queue import Queue
from tqdm import tqdm
import os
from datetime import datetime
import logging
import webbrowser

from scanner.banner import grab_banner
from scanner.utils import load_config

class PortScanner:
    def __init__(self):
        self.config = load_config()
        self.open_ports = []
        self.results = {}
        self.lock = threading.Lock()
        self.live_callback = None

    def set_live_callback(self, callback):
        self.live_callback = callback

    def scan_port(self, target, port, stealth=False):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1.5)
                if s.connect_ex((target, port)) == 0:
                    banner = grab_banner(target, port)
                    service = self.identify_service(port)
                    port_info = {"port": port, "service": service, "banner": banner}
                    
                    with self.lock:
                        if not any(p['port'] == port for p in self.open_ports):
                            self.open_ports.append(port_info)
                            if self.live_callback:
                                self.live_callback(port_info)
                    return True
        except:
            pass
        return False

    def identify_service(self, port):
        services = {80:"HTTP", 443:"HTTPS", 22:"SSH", 21:"FTP", 25:"SMTP", 
                   53:"DNS", 3306:"MySQL", 3389:"RDP", 8080:"HTTP-Alt"}
        return services.get(port, "Unknown")

    def scan(self, target, start_port=1, end_port=500, threads=150, use_common=False, stealth=False):
        print(f"[+] Scanning {target} | Stealth: {stealth}")
        start_time = time.time()

        if use_common == "top100":
            ports = list(range(1, 101)) + [443, 80, 22, 21, 25, 53, 3306, 3389]
        else:
            ports = self.config.get("common_ports", [80, 443]) if use_common else range(start_port, end_port + 1)

        queue = Queue()
        for p in ports:
            queue.put(p)

        progress = tqdm(total=len(ports), desc="Scanning")

        def worker():
            while not queue.empty():
                port = queue.get()
                self.scan_port(target, port, stealth)
                progress.update(1)
                if stealth:
                    time.sleep(random.uniform(0.3, 1.0))
                queue.task_done()

        for _ in range(min(threads, len(ports))):
            threading.Thread(target=worker, daemon=True).start()

        queue.join()
        progress.close()

        self.results = {
            "target": target,
            "scan_time": round(time.time() - start_time, 2),
            "open_ports": sorted(self.open_ports, key=lambda x: x['port'])
        }

        self.save_reports_to_desktop(target)
        return self.results

    def save_reports_to_desktop(self, target):
        desktop = r"C:\Users\Abdo\Desktop"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        base = f"NetProbe_{target}_{timestamp}"

        txt_path = f"{desktop}\\{base}.txt"
        html_path = f"{desktop}\\{base}.html"

        # Text Report
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(f"NetProbe Scan Report\n{'='*60}\n")
            f.write(f"Target     : {target}\n")
            f.write(f"Time       : {datetime.now()}\n")
            f.write(f"Duration   : {self.results['scan_time']} seconds\n")
            f.write(f"Open Ports : {len(self.results['open_ports'])}\n\n")
            f.write("PORT\tSERVICE\t\tBANNER\n")
            f.write("-" * 80 + "\n")
            for p in self.results["open_ports"]:
                banner = p.get('banner', 'No banner')[:60]
                f.write(f"{p['port']:<6} {p['service']:<12} {banner}\n")

        # HTML Report
        self.create_html_report(html_path)

        print(f"\n✅ Scan Completed! Reports saved on Desktop")
        try:
            # Fixed way to open HTML
            html_url = "file:///" + html_path.replace("\\", "/")
            webbrowser.open(html_url)
        except:
            print("Report saved on Desktop but could not open automatically.")

    def create_html_report(self, html_path):
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>NetProbe Report - {self.results['target']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #0f0f0f; color: #00ff9d; margin: 40px; }}
        .container {{ background: #1a1a1a; padding: 30px; border-radius: 10px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; border: 1px solid #333; text-align: left; }}
        th {{ background: #007bff; color: white; }}
        h1 {{ color: #00ccff; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>NetProbe Scan Report</h1>
        <p><strong>Target:</strong> {self.results['target']}</p>
        <p><strong>Duration:</strong> {self.results['scan_time']} seconds</p>
        <p><strong>Open Ports Found:</strong> {len(self.results['open_ports'])}</p>
        
        <h2>Open Ports</h2>
        <table>
            <tr><th>Port</th><th>Service</th><th>Banner</th></tr>
"""
        for p in self.results["open_ports"]:
            banner = p.get('banner', 'No banner')[:70]
            html += f"<tr><td>{p['port']}</td><td>{p['service']}</td><td>{banner}</td></tr>"

        html += """
        </table>
        <hr>
        <p><small>Generated by NetProbe</small></p>
    </div>
</body>
</html>"""

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)