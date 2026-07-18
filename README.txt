NetProbe is a professional-grade network port scanner with a modern GUI interface. It's designed for network administrators, security researchers, and enthusiasts to discover open ports and services on target systems quickly and efficiently.

📋 Features
Multi-threaded Scanning - Fast and efficient port scanning using concurrent threads

Banner Grabbing - Retrieves service banners from open ports for detailed information

Stealth Mode - Slower scanning with randomized delays to avoid detection

Multiple Scan Options:

Common ports (predefined set)

Top 100 ports

Custom range (1-500)

Live Results Display - Real-time updates showing open ports as they're discovered

Comprehensive Reports - Generates both TXT and HTML reports automatically

Modern GUI - Clean, dark-themed interface built with CustomTkinter

Service Identification - Recognizes common services like HTTP, SSH, FTP, MySQL

🚀 Installation
Prerequisites
Python 3.6 or higher

pip (Python package manager)

Step 1: Clone the Repository
bash
git clone https://github.com/yourusername/netprobe.git
cd netprobe
Step 2: Install Required Dependencies
bash
pip install customtkinter tqdm
💻 Quick Start
Using the GUI Application
bash
python main.py
Example Usage
Enter target IP or domain (e.g., scanme.nmap.org or dns.google)

Select scan mode:

Common Ports: Quick scan of most common services

Top 100 Ports: Scans the most frequently used 100 ports

Custom 1-500: Comprehensive scan of 500 ports

Toggle Stealth Mode if needed

Click "Start Scan"

View live results in the console area

Reports are automatically saved to your desktop

📁 Project Structure
text
netprobe/
├── main.py                  # GUI application entry point
├── scanner/
│   ├── __init__.py
│   ├── core.py             # Core scanning engine
│   ├── banner.py           # Banner grabbing functionality
│   └── utils.py            # Utilities (logging, config)
├── config.json             # Configuration file
├── requirements.txt        # Python dependencies
└── README.md              # This file
🛠️ Configuration
You can customize the scanner by editing config.json:

json
{
  "default_threads": 200,
  "default_timeout": 1.5,
  "common_ports": [21, 22, 23, 80, 443, 3306, 3389]
}
📊 Reports
When a scan completes, NetProbe automatically generates two reports on your desktop:

TXT Report
text
NetProbe Scan Report
============================================================
Target     : 8.8.8.8
Time       : 2024-01-01 12:00:00
Duration   : 2.34 seconds
Open Ports : 2

PORT	SERVICE		BANNER
----------------------------------------------------------------
53      DNS             No banner
443     HTTPS           HTTP/1.1 200 OK
HTML Report
Modern, visually appealing format

Color-coded results

Easy to share and view in any browser

⚡ Performance
Scan Speed: 150-200 ports per second with default settings

Memory Usage: ~50MB RAM

Network Usage: Minimal, optimized packet sending

⚠️ Disclaimer
Important: This tool is for educational and authorized testing purposes only. Always obtain proper permission before scanning any network or system. Unauthorized port scanning may violate laws and regulations in your jurisdiction.

🛡️ Safety & Ethics
Only scan systems you own or have explicit permission to test

Use stealth mode when appropriate

Respect network policies and rate limits

Do not use for malicious purposes

🔧 Troubleshooting
Common Issues
Q: The scanner can't connect to a target

Ensure the target is reachable

Check your internet connection

Try using an IP address instead of domain
