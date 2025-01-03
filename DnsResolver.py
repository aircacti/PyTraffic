import socket

class DnsResolver:
    @staticmethod
    def resolve_domain(domain):
        try:
            ip_address = socket.gethostbyname(domain)
            return ip_address
        except socket.gaierror:
            raise RuntimeError(f"Failed to resolve domain '{domain}'.")