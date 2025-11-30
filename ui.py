import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from ip_utils import get_public_ip_info, get_local_network_info, lookup_ip
from dns_utils import run_dns_lookup, dns_leak_test
from speedtest_utils import run_speed_test
from network_scanner import scan_network_devices
import socket
import platform
import subprocess


class NetworkMonitoringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Monitoring Tool - v0.1")
        self.root.geometry('1100x720')
        self.create_widgets()
        self.setup_style()

    def create_widgets(self):
        # Main notebook and tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tab_dashboard = ttk.Frame(self.notebook)
        self.tab_ip = ttk.Frame(self.notebook)
        self.tab_tools = ttk.Frame(self.notebook)
        self.tab_dns = ttk.Frame(self.notebook)
        self.tab_speed = ttk.Frame(self.notebook)
        self.tab_devices = ttk.Frame(self.notebook)

    def setup_style(self):
        frame = self.tab_dashboard
        # Header
        header = ttk.Frame(frame)
        header.pack(fill=tk.X, pady=6, padx=6)
        ttk.Label(header, text='Overview', font=('Segoe UI', 12, 'bold')).pack(side=tk.LEFT)
        ttk.Button(header, text='Refresh', command=self.refresh_summary).pack(side=tk.RIGHT)

        # Stat cards
        cards = ttk.Frame(frame)
        cards.pack(fill=tk.X, padx=6)

        def make_card(parent, title):
            card = ttk.Frame(parent, relief=tk.RIDGE, borderwidth=1, padding=8)
            ttk.Label(card, text=title, font=('Segoe UI', 9, 'bold')).pack(anchor=tk.W)
            lbl = ttk.Label(card, text='Loading...', font=('Consolas', 12))
            lbl.pack(anchor=tk.W, pady=(6,0))
            return card, lbl

        c1, self.stat_public_ip = make_card(cards, 'Public IP')
        c2, self.stat_local_ip = make_card(cards, 'Local IP')
        c3, self.stat_devices = make_card(cards, 'Devices')
        c4, self.stat_last_scan = make_card(cards, 'Last Scan')

        c1.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=4, pady=4)
        c2.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=4, pady=4)
        c3.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=4, pady=4)
        c4.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=4, pady=4)

        # Summary area below
        ttk.Label(frame, text='Summary', font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W, pady=(8,0), padx=6)
        self.summary_text = scrolledtext.ScrolledText(frame, height=6)
        self.summary_text.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        # Quick scan button
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, padx=6, pady=(0,8))
        ttk.Button(btn_frame, text='Quick Scan Devices', command=self.quick_scan_devices).pack(side=tk.RIGHT)
        self.tab_speed = ttk.Frame(self.notebook)
        self.tab_devices = ttk.Frame(self.notebook)

        for t, label in [(self.tab_dashboard, 'Dashboard'), (self.tab_ip, 'IP Info'), (self.tab_tools, 'Network Tools'), (self.tab_dns, 'DNS Utilities'), (self.tab_speed, 'Speed Test'), (self.tab_devices, 'Devices')]:
            self.notebook.add(t, text=label)

        self.init_dashboard()
        self.init_ip_tab()
        self.init_tools_tab()
        self.init_dns_tab()
        self.init_speed_tab()
        self.init_devices_tab()

    def init_dashboard(self):
        frame = self.tab_dashboard
        ttk.Label(frame, text='Summary', font=('Segoe UI', 12, 'bold')).pack(anchor=tk.W, pady=6)
        self.summary_text = scrolledtext.ScrolledText(frame, height=8)
        self.summary_text.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        ttk.Button(frame, text='Refresh Summary', command=self.refresh_summary).pack(pady=6)

    def refresh_summary(self):
        def task():
            ipinfo = get_public_ip_info()
            local = get_local_network_info()
            public = ipinfo.get('ip') if isinstance(ipinfo, dict) else str(ipinfo)
            local_ip = local.get('local_ip') if isinstance(local, dict) else str(local)

            # Update stat cards
            self.root.after(0, lambda: self.stat_public_ip.config(text=public or 'N/A'))
            self.root.after(0, lambda: self.stat_local_ip.config(text=local_ip or 'N/A'))

            s = []
            s.append('Public IP: ' + str(public))
            s.append('Local IP: ' + str(local_ip))
            self.root.after(0, lambda: (self.summary_text.delete(1.0, tk.END), self.summary_text.insert(tk.END, '\n'.join(s))))
        threading.Thread(target=task, daemon=True).start()

    def quick_scan_devices(self):
        # show scanning
        self.stat_devices.config(text='Scanning...')
        self.stat_last_scan.config(text='-')

        def task():
            devices = scan_network_devices()
            count = len(devices) if isinstance(devices, list) else 0
            import time as _time
            now = _time.strftime('%Y-%m-%d %H:%M:%S')
            self.root.after(0, lambda: self.stat_devices.config(text=str(count)))
            self.root.after(0, lambda: self.stat_last_scan.config(text=now))
            # Optionally update devices tab tree as well
            self.root.after(0, lambda: (self.devices_tree.delete(*self.devices_tree.get_children()), [self.devices_tree.insert('', tk.END, values=(d.get('ip',''), d.get('mac',''), d.get('hostname',''), d.get('vendor') or 'Unknown')) for d in devices]))

        threading.Thread(target=task, daemon=True).start()

    def init_ip_tab(self):
        frame = self.tab_ip
        ttk.Label(frame, text='Public IP Info', font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W)
        self.ip_tree = ttk.Treeview(frame, columns=('Property','Value'), show='headings')
        self.ip_tree.heading('Property', text='Property')
        self.ip_tree.heading('Value', text='Value')
        self.ip_tree.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        ttk.Button(frame, text='Refresh', command=self.refresh_ip).pack(pady=6)

    def refresh_ip(self):
        def task():
            data = get_public_ip_info()
            self.ip_tree.delete(*self.ip_tree.get_children())
            if isinstance(data, dict):
                for k, v in data.items():
                    self.ip_tree.insert('', tk.END, values=(k, v))
            else:
                self.ip_tree.insert('', tk.END, values=('error', str(data)))
        threading.Thread(target=task, daemon=True).start()

    def init_tools_tab(self):
        frame = self.tab_tools
        # Ping
        ping_frame = ttk.Frame(frame)
        ping_frame.pack(fill=tk.X, pady=6, padx=6)
        ttk.Label(ping_frame, text='Ping Target:').pack(side=tk.LEFT)
        self.ping_entry = ttk.Entry(ping_frame)
        self.ping_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)
        ttk.Button(ping_frame, text='Ping', command=self.ping_target).pack(side=tk.LEFT)
        self.ping_result = scrolledtext.ScrolledText(frame, height=6)
        self.ping_result.pack(fill=tk.BOTH, expand=False, padx=6, pady=6)

        # Port scan
        port_frame = ttk.Frame(frame)
        port_frame.pack(fill=tk.X, pady=6, padx=6)
        ttk.Label(port_frame, text='Port Target:').pack(side=tk.LEFT)
        self.port_entry = ttk.Entry(port_frame)
        self.port_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)
        ttk.Button(port_frame, text='Scan', command=self.scan_ports).pack(side=tk.LEFT)
        self.port_result = scrolledtext.ScrolledText(frame, height=6)
        self.port_result.pack(fill=tk.BOTH, expand=False, padx=6, pady=6)

    def ping_target(self):
        target = self.ping_entry.get().strip()
        if not target:
            messagebox.showerror('Error','Enter target')
            return
        def task():
            try:
                param = '-n' if platform.system().lower() == 'windows' else '-c'
                count = '4'
                out = subprocess.check_output(['ping', param, count, target], universal_newlines=True)
            except Exception as e:
                out = str(e)
            self.ping_result.delete(1.0, tk.END)
            self.ping_result.insert(tk.END, out)
        threading.Thread(target=task, daemon=True).start()

    def scan_ports(self):
        target = self.port_entry.get().strip()
        if not target:
            messagebox.showerror('Error','Enter target')
            return
        def task():
            common_ports = [21,22,23,25,53,80,110,143,443,3306,3389]
            out = []
            for p in common_ports:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1)
                    res = s.connect_ex((target, p))
                    if res == 0:
                        out.append(f"Port {p}: OPEN")
                    else:
                        out.append(f"Port {p}: closed")
                    s.close()
                except Exception as e:
                    out.append(f"Port {p}: error {e}")
            self.port_result.delete(1.0, tk.END)
            self.port_result.insert(tk.END, '\n'.join(out))
        threading.Thread(target=task, daemon=True).start()

    def init_dns_tab(self):
        frame = self.tab_dns
        lookup_frame = ttk.Frame(frame)
        lookup_frame.pack(fill=tk.X, padx=6, pady=6)
        ttk.Label(lookup_frame, text='Domain:').pack(side=tk.LEFT)
        self.dns_entry = ttk.Entry(lookup_frame)
        self.dns_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)
        ttk.Button(lookup_frame, text='Lookup', command=self.do_dns_lookup).pack(side=tk.LEFT)
        self.dns_result = scrolledtext.ScrolledText(frame, height=8)
        self.dns_result.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        ttk.Button(frame, text='DNS Leak Test', command=self.do_dns_leak).pack(pady=6)

    def do_dns_lookup(self):
        domain = self.dns_entry.get().strip()
        if not domain:
            messagebox.showerror('Error','Enter domain')
            return
        def task():
            res = run_dns_lookup(domain)
            self.dns_result.delete(1.0, tk.END)
            self.dns_result.insert(tk.END, str(res))
        threading.Thread(target=task, daemon=True).start()

    def do_dns_leak(self):
        def task():
            res = dns_leak_test()
            self.dns_result.delete(1.0, tk.END)
            self.dns_result.insert(tk.END, str(res))
        threading.Thread(target=task, daemon=True).start()

    def init_speed_tab(self):
        frame = self.tab_speed
        ttk.Button(frame, text='Run Speed Test', command=self.run_speed).pack(pady=8)
        self.speed_result = scrolledtext.ScrolledText(frame, height=8)
        self.speed_result.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

    def run_speed(self):
        def task():
            res = run_speed_test()
            self.speed_result.delete(1.0, tk.END)
            self.speed_result.insert(tk.END, str(res))
        threading.Thread(target=task, daemon=True).start()

    def init_devices_tab(self):
        frame = self.tab_devices
        self.devices_tree = ttk.Treeview(frame, columns=('IP','MAC','Hostname','Vendor'), show='headings')
        for c,w in [('IP',140),('MAC',180),('Hostname',220),('Vendor',140)]:
            self.devices_tree.heading(c, text=c)
            self.devices_tree.column(c, width=w)
        self.devices_tree.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        ttk.Button(frame, text='Scan Network Devices', command=self.scan_devices).pack(pady=6)

    def scan_devices(self):
        # show scanning row
        self.devices_tree.delete(*self.devices_tree.get_children())
        self.devices_tree.insert('', tk.END, values=('Scanning...','','',''))

        def task():
            devices = scan_network_devices()
            # replace tree
            self.root.after(0, lambda: self.devices_tree.delete(*self.devices_tree.get_children()))
            for d in devices:
                ip = d.get('ip','')
                mac = d.get('mac','')
                host = d.get('hostname','')
                vendor = d.get('vendor','') or 'Unknown'
                self.root.after(0, lambda ip=ip,mac=mac,host=host,vendor=vendor: self.devices_tree.insert('', tk.END, values=(ip,mac,host,vendor)))
        threading.Thread(target=task, daemon=True).start()

    # Navigation helpers
    def show_dashboard(self):
        self.notebook.select(self.tab_dashboard)
    def show_ip_info(self):
        self.notebook.select(self.tab_ip)
    def show_network_tools(self):
        self.notebook.select(self.tab_tools)
    def show_dns_tools(self):
        self.notebook.select(self.tab_dns)
    def show_speed_test(self):
        self.notebook.select(self.tab_speed)
    def show_devices(self):
        self.notebook.select(self.tab_devices)
