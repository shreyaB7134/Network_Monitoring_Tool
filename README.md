# 🌐 Network Monitoring Tool

A simple and effective **Python-based GUI application** that helps users monitor and analyze their network in real time.  
Built using **Tkinter**, this tool provides features like IP information, device scanning, DNS utilities, speed testing, and basic network diagnostics.

---

## 📘 Project Overview

The **Network Monitoring Tool** combines multiple network utilities into a single interface. It is designed for:

- Students learning computer networks  
- Developers testing network performance  
- Users checking devices connected to their WiFi  
- Anyone who needs quick IP, DNS, speed, or network insights  

The backend logic is written in Python, and the interface is built using Tkinter.

---

## ✨ Features Summary

| Feature | Description |
|--------|-------------|
| 🌍 Public & Local IP Info | Shows public IP, ISP region, local IP, MAC address, hostname |
| 📡 Network Tools | Allows ping testing and port scanning |
| 🌐 DNS Tools | DNS Lookup and DNS Leak Test |
| 🚀 Speed Test | Measures download speed, upload speed, and ping |
| 🖥 Device Scanner | Scans active devices connected to your LAN |
| 📊 Dashboard | Shows summary: public IP, local IP, device count, last scan time |
| 🔒 Security Overview | Provides DNS leak test and basic security checks |

---

## 📁 Project Structure

```plaintext
Network_Monitoring_Tool/
├── main.py              # Starts the Tkinter application
├── ui.py                # GUI layout and user interaction
├── ip_utils.py          # Public & local IP information
├── dns_utils.py         # DNS lookup and DNS leak test
├── speedtest_utils.py   # Internet speed test functions
├── network_scanner.py   # LAN device scanner
└── README.md            # Documentation
```

---

## 🔧 Installation Guide

### Requirements
- Python **3.8+**

---

### Step 1: Clone the Repository

```bash
git clone https://github.com/shreyaB7134/Network_Monitoring_Tool.git
cd Network_Monitoring_Tool
```

### Step 2: Install Dependencies

```bash
pip install requests psutil speedtest-cli python-whois dnspython pillow matplotlib colorama tk
```

---

## ▶️ Running the Application

```bash
python main.py
```
This opens the graphical Dashboard.

---

## 🔍 Detailed Module Explanation

### main.py
Entry point for the project
- Launches Tkinter window
- Loads UI from ui.py

### ui.py
- Creates full GUI layout
- Manages all user actions
- Calls backend functions
- Displays results in tables, text boxes, and labels

### ip_utils.py
Fetches:
- Public IP
- ISP information
- Local IP
- MAC address
- Hostname
- Network interfaces

### dns_utils.py
- Performs DNS lookups
- Runs DNS leak tests

### speedtest_utils.py
- Measures download speed
- Measures upload speed
- Measures ping

### network_scanner.py
Scans LAN:
- Pings all IPs
- Reads ARP table
- Finds MAC & hostname
- Lists all active devices

---

## 🔄 Workflow of the Project

1. User opens the application
2. Tkinter GUI loads
3. User selects an option (Ping / DNS Lookup / Scan / Speed Test)
4. UI module calls backend function
5. Backend processes the request
6. Results are returned to UI
7. UI displays the output clearly

---

## 🛡 License
This project is licensed under the MIT License.

Made using Python and Tkinter.

---


