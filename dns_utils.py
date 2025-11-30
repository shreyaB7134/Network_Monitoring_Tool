import dns.resolver
import requests


def run_dns_lookup(domain, record_type='A'):
    try:
        resolver = dns.resolver.Resolver()
        answers = resolver.resolve(domain, record_type)
        return [str(rdata) for rdata in answers]
    except Exception as e:
        return {"error": str(e)}


def dns_leak_test():
    results = {}
    servers = [
        "https://api.ipify.org",
        "https://icanhazip.com",
        "https://ident.me",
        "https://ifconfig.me"
    ]
    for s in servers:
        try:
            ip = requests.get(s, timeout=5).text.strip()
            results[s] = ip
        except Exception as e:
            results[s] = {"error": str(e)}
    return results