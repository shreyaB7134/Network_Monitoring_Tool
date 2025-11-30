<<<<<<< HEAD
import subprocess
import platform
import socket
import psutil
import ipaddress
import concurrent.futures


def scan_network_devices(timeout_ms: int = 1000, max_workers: int = 100):
    """Perform a local network scan and return list of devices.

    Returns list of dicts: {'ip': str, 'mac': str, 'hostname': str, 'vendor': ''}
    This function is best-effort and wrapped with error handling so callers won't crash.
    """
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        return []

    # Get netmask if possible
    netmask = None
    try:
        for iface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if getattr(addr, 'address', None) == local_ip and getattr(addr, 'netmask', None):
                    netmask = addr.netmask
                    break
            if netmask:
                break
    except Exception:
        netmask = None

    try:
        if netmask:
            try:
                network = ipaddress.IPv4Network(f"{local_ip}/{netmask}", strict=False)
            except Exception:
                network = ipaddress.ip_network(f"{local_ip}/24", strict=False)
        else:
            network = ipaddress.ip_network(f"{local_ip}/24", strict=False)
    except Exception:
        return []

    hosts = [str(h) for h in network.hosts()]

    def ping(host: str) -> bool:
        try:
            if platform.system().lower() == 'windows':
                cmd = ['ping', '-n', '1', '-w', str(timeout_ms), host]
            else:
                cmd = ['ping', '-c', '1', '-W', str(int(timeout_ms / 1000)), host]
            res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return res.returncode == 0
        except Exception:
            return False

    alive = []
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = {ex.submit(ping, h): h for h in hosts}
            for fut in concurrent.futures.as_completed(futures):
                h = futures[fut]
                try:
                    if fut.result():
                        alive.append(h)
                except Exception:
                    continue
    except Exception:
        # If threaded pinging fails, fallback to no alive list
        alive = []

    macs = {}
    try:
        arp_out = subprocess.check_output(['arp', '-a'], universal_newlines=True)
        for line in arp_out.splitlines():
            parts = line.split()
            if len(parts) >= 2 and parts[0][0].isdigit():
                ip = parts[0]
                mac = parts[1]
                macs[ip] = mac
    except Exception:
        macs = {}

    # Try to include gateway from route table
    gateway = None
    try:
        route_out = subprocess.check_output(['route', 'print', '-4'] if platform.system().lower() == 'windows' else ['ip', 'route'], universal_newlines=True)
        for line in route_out.splitlines():
            if platform.system().lower() == 'windows':
                if '0.0.0.0' in line and line.strip().startswith('0.0.0.0'):
                    cols = line.split()
                    if len(cols) >= 3:
                        gateway = cols[2]
                        break
            else:
                if line.startswith('default'):
                    cols = line.split()
                    if 'via' in cols:
                        gw_index = cols.index('via') + 1
                        if gw_index < len(cols):
                            gateway = cols[gw_index]
                            break
    except Exception:
        gateway = None

    ips_set = set(alive) | set(macs.keys())
    if gateway:
        ips_set.add(gateway)

    devices = []
    for ip in sorted(ips_set, key=lambda s: tuple(int(x) for x in s.split('.')) if s and '.' in s else (0,)):
        mac = macs.get(ip, '')
        hostname = ''
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except Exception:
            # best-effort, don't crash
            hostname = ''
        devices.append({'ip': ip, 'mac': mac, 'hostname': hostname, 'vendor': ''})

    return devices
=======
import subprocess
import platform
import socket
import psutil
import ipaddress
import concurrent.futures


def scan_network_devices(timeout_ms: int = 1000, max_workers: int = 100):
    """Perform a local network scan and return list of devices.

    Returns list of dicts: {'ip': str, 'mac': str, 'hostname': str, 'vendor': ''}
    This function is best-effort and wrapped with error handling so callers won't crash.
    """
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        return []

    # Get netmask if possible
    netmask = None
    try:
        for iface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if getattr(addr, 'address', None) == local_ip and getattr(addr, 'netmask', None):
                    netmask = addr.netmask
                    break
            if netmask:
                break
    except Exception:
        netmask = None

    try:
        if netmask:
            try:
                network = ipaddress.IPv4Network(f"{local_ip}/{netmask}", strict=False)
            except Exception:
                network = ipaddress.ip_network(f"{local_ip}/24", strict=False)
        else:
            network = ipaddress.ip_network(f"{local_ip}/24", strict=False)
    except Exception:
        return []

    hosts = [str(h) for h in network.hosts()]

    def ping(host: str) -> bool:
        try:
            if platform.system().lower() == 'windows':
                cmd = ['ping', '-n', '1', '-w', str(timeout_ms), host]
            else:
                cmd = ['ping', '-c', '1', '-W', str(int(timeout_ms / 1000)), host]
            res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return res.returncode == 0
        except Exception:
            return False

    alive = []
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = {ex.submit(ping, h): h for h in hosts}
            for fut in concurrent.futures.as_completed(futures):
                h = futures[fut]
                try:
                    if fut.result():
                        alive.append(h)
                except Exception:
                    continue
    except Exception:
        # If threaded pinging fails, fallback to no alive list
        alive = []

    macs = {}
    try:
        arp_out = subprocess.check_output(['arp', '-a'], universal_newlines=True)
        for line in arp_out.splitlines():
            parts = line.split()
            if len(parts) >= 2 and parts[0][0].isdigit():
                ip = parts[0]
                mac = parts[1]
                macs[ip] = mac
    except Exception:
        macs = {}

    # Try to include gateway from route table
    gateway = None
    try:
        route_out = subprocess.check_output(['route', 'print', '-4'] if platform.system().lower() == 'windows' else ['ip', 'route'], universal_newlines=True)
        for line in route_out.splitlines():
            if platform.system().lower() == 'windows':
                if '0.0.0.0' in line and line.strip().startswith('0.0.0.0'):
                    cols = line.split()
                    if len(cols) >= 3:
                        gateway = cols[2]
                        break
            else:
                if line.startswith('default'):
                    cols = line.split()
                    if 'via' in cols:
                        gw_index = cols.index('via') + 1
                        if gw_index < len(cols):
                            gateway = cols[gw_index]
                            break
    except Exception:
        gateway = None

    ips_set = set(alive) | set(macs.keys())
    if gateway:
        ips_set.add(gateway)

    devices = []
    for ip in sorted(ips_set, key=lambda s: tuple(int(x) for x in s.split('.')) if s and '.' in s else (0,)):
        mac = macs.get(ip, '')
        hostname = ''
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except Exception:
            # best-effort, don't crash
            hostname = ''
        devices.append({'ip': ip, 'mac': mac, 'hostname': hostname, 'vendor': ''})

    return devices
>>>>>>> 6af5019e708331ae55f6ee6dd866da14832a579e
