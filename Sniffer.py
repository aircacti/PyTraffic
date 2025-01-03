import psutil
from scapy.all import sniff, IP

from Logger import Logger
from Notify import Notify


class Sniffer:
    def __init__(self):
        self.interface = None

    def get_available_interfaces(self):
        try:
            interfaces = psutil.net_if_addrs()
            if not interfaces:
                raise RuntimeError("No network interfaces found on this system.")

            structured_interfaces = []

            for index, interface_name in enumerate(interfaces.keys(), start=1):
                structured_interfaces.append({
                    "index": index,
                    "name": interface_name,
                })

            return structured_interfaces
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve network interfaces: {e}")

    def get_number_of_available_interfaces(self):
        try:
            interfaces = self.get_available_interfaces()
            return len(interfaces)
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve number of interfaces: {e}")

    def start_sniffing(self, interface_name, blocked_ips):
        self.interface = interface_name

        def process_packet(packet):
            if packet.haslayer(IP):
                src = packet[IP].src
                dst = packet[IP].dst

                if src in blocked_ips or dst in blocked_ips:
                    logger = Logger()
                    logger.log("WARNING", f"Niebezpieczne połączenie {src}<->{dst}")
                    Notify.alert()

        try:
            sniff(iface=self.interface, prn=process_packet, store=False)
        except Exception as e:
            raise RuntimeError(f"Failed to start sniffing on interface '{self.interface}'. Details: {e}")

