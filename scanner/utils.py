import logging
import json
import os
from datetime import datetime

def setup_logging():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(
        filename=f"logs/netprobe_{datetime.now().strftime('%Y%m%d')}.log",
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def load_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except:
        return {"default_threads": 200, "default_timeout": 1.5, "common_ports": [21,22,23,80,443,3306,3389]}