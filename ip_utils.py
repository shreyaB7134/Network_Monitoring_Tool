import requests
import socket
import psutil
import uuid
import time


def get_public_ip_info(api_services=None, delay=1.0):
    services = api_services or [
        "https://ipinfo.io/json",
        "https://ipapi.co/json/",
        "https://api.myip.com"
    ]
    for s in services:
        try:
            r = requests.get(s, timeout=8)
            if r.status_code == 200:
                time.sleep(delay)
                return r.json()
        except Exception:
            continue
    return {"error": "Could not fetch IP info"}


def get_local_network_info():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        mac = ":".join(["{:02x}".format((uuid.getnode() >> e) & 0xff) for e in range(5, -1, -1)])
        interfaces = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        connection_type = "Wi-Fi" if "Wi-Fi" in interfaces else "Ethernet" if "Ethernet" in interfaces else "Unknown"
        speed = next((s.speed for s in stats.values() if s.speed > 0), 0)
        return {
            "hostname": hostname,
            "local_ip": local_ip,
            "mac_address": mac,
            "connection_type": connection_type,
            "speed": f"{speed} Mbps",
            "interfaces": {iface: [addr._asdict() for addr in addrs] for iface, addrs in interfaces.items()}
        }
    except Exception as e:
        return {"error": str(e)}


def lookup_ip(ip):
    try:
        services = [
            ("ipinfo.io", f"https://ipinfo.io/{ip}/json"),
            ("ipapi.co", f"https://ipapi.co/{ip}/json/")
        ]
        results = {}
        for name, url in services:
            try:
                r = requests.get(url, timeout=8)
                if r.status_code == 200:
                    results[name] = r.json()
                else:
                    results[name] = {"error": f"status {r.status_code}"}
            except Exception as e:
                results[name] = {"error": str(e)}
        return results
    except Exception as e:
        return {"error": str(e)}