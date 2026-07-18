import customtkinter as ctk
from tkinter import scrolledtext, messagebox
import threading

from scanner.core import PortScanner

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class NetProbeApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("NetProbe - Advanced Port Scanner")
        self.root.geometry("1050x750")
        self.scanner = PortScanner()
        self.create_gui()

    def create_gui(self):
        ctk.CTkLabel(self.root, text="NetProbe", font=ctk.CTkFont(size=34, weight="bold")).pack(pady=15)
        ctk.CTkLabel(self.root, text="Professional Port Scanner", font=ctk.CTkFont(size=16)).pack(pady=5)

        ctk.CTkLabel(self.root, text="Target IP / Domain:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=40, pady=(20,5))
        self.target_entry = ctk.CTkEntry(self.root, width=500, placeholder_text="dns.google or scanme.nmap.org")
        self.target_entry.pack(pady=8)

        mode_frame = ctk.CTkFrame(self.root)
        mode_frame.pack(pady=15)
        self.mode_var = ctk.StringVar(value="common")
        ctk.CTkRadioButton(mode_frame, text="Common Ports", variable=self.mode_var, value="common").grid(row=0, column=0, padx=20)
        ctk.CTkRadioButton(mode_frame, text="Top 100 Ports", variable=self.mode_var, value="top100").grid(row=0, column=1, padx=20)
        ctk.CTkRadioButton(mode_frame, text="Custom 1-500", variable=self.mode_var, value="custom").grid(row=0, column=2, padx=20)

        self.stealth_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(self.root, text="Stealth Mode (Slower - Harder to Detect)", 
                       variable=self.stealth_var, font=ctk.CTkFont(size=14)).pack(pady=12)

        self.scan_btn = ctk.CTkButton(self.root, text="🚀 Start Scan", height=55, 
                                     font=ctk.CTkFont(size=18, weight="bold"),
                                     command=self.start_scan)
        self.scan_btn.pack(pady=20)

        ctk.CTkLabel(self.root, text="Live Scan Results", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=40)
        self.result_text = scrolledtext.ScrolledText(self.root, height=24, bg="#111111", fg="#00ffaa", font=("Consolas", 12))
        self.result_text.pack(fill="both", expand=True, padx=40, pady=10)

    def start_scan(self):
        target = self.target_entry.get().strip()
        if not target:
            messagebox.showerror("Error", "Please enter a target")
            return

        self.scan_btn.configure(state="disabled", text="Scanning...")
        self.result_text.delete(1.0, "end")
        self.result_text.insert("end", f"Starting scan on {target}...\n\n")

        mode = self.mode_var.get()
        stealth = self.stealth_var.get()

        threading.Thread(target=self.run_scan, args=(target, mode, stealth), daemon=True).start()

    def run_scan(self, target, mode, stealth):
        try:
            self.scanner.set_live_callback(self.live_update)
            if mode == "top100":
                self.scanner.scan(target, use_common="top100", stealth=stealth)
            elif mode == "custom":
                self.scanner.scan(target, start_port=1, end_port=500, stealth=stealth)
            else:
                self.scanner.scan(target, use_common=True, stealth=stealth)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
        finally:
            self.root.after(0, self.finish_scan)

    def live_update(self, port_info):
        text = f"✓ Open → Port {port_info['port']} | {port_info['service']} | {port_info.get('banner','')[:50]}\n"
        self.root.after(0, lambda: self.result_text.insert("end", text))

    def finish_scan(self):
        self.scan_btn.configure(state="normal", text="🚀 Start Scan")

if __name__ == "__main__":
    app = NetProbeApp()
    app.root.mainloop()