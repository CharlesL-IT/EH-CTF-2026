'''
Note: Script code was written with the help of HopGPT after pseudocode/design was completed.
Also reviewed code manually to confirm logic and check for errors.
'''

#!/usr/bin/env python3
"""
Listen for IPv4 TCP packets to a specific local port where the only TCP flag set is URG.
When such a packet is observed, remove the iptables rule for that port by using:
    sudo iptables -D INPUT -p tcp --dport <port> --syn -j REJECT --reject-with tcp-reset

Run as root (needs permission to modify iptables)
"""

import system
import subprocess
import argparse
import time
from scapy.all import sniff, IP, TCP

def parse_args():
    p = argparse.ArgumentParser(description="Listen for URG-only TCP packet to a port and delete the iptables rule for that port if a packet is received.")
    p.add_argument("--port", "-p", required=True, help="Destination TCP port to monitor")
    p.add_argument("--iface", "-i", default=None, help="Interface to listen on (default: scapy default)")
    p.add_argument("--source", "-s", default=None, help="Optional source IP to accept (default: any)")
    p.add_argument("--dry-run", action="store_true", help="Don't actually run delete rule command on iptables; just report when matching packet received")
    p.add_argument("--once", action="store_true", help="Exit after first matching packet and action")
    return p.parse_args()

"""
Returns true if the only TCP flag set is URG.
scapy represents flags as an integer bitmask, URG is 0x20 (32).
"""
def tcp_flags_only_urg(tcp):
    URG_BIT = 0x20
    flags = int(tcp.flags)
    return (flags & URG_BIT) and (flags & ~URG_BIT) == 0

def handle_packet(pkt, cfg, state):
    # Ensure the packet has IP/TCP layers
    if IP not in pkt or TCP not in pkt:
        return False

    ip = pkt[IP]
    tcp = pkt[TCP]

    # Check destination port
    if tcp.dport != cfg.port:
        return False

    # Optionally check source IP
    if cfg.source and ip.src != cfg.source:
        return False

    if tcp_flags_only_urg(tcp):
        print(f"[*] Matching packet from {ip.src}:{tcp.sport} -> {ip.dst}:{tcp.dport} with flags={tcp.sprintf('%TCP.flags%')}")
        if cfg.dry_run:
            print("[*] Dry run: not modifying iptables.")
        else:
            cmd = ["sudo", "iptables", "-D", "INPUT", "-p", "tcp", "--dport", str(cfg.port), "--syn", "-j", "REJECT", "--reject-with", "tcp-reset"]
            print(f"[*] Executing: {' '.join(cmd)}")
            try:
                subprocess.run(cmd, check=True)
                print("[*] iptables rule deleted successfully.")
            except subprocess.CalledProcessError as e:
                print(f"[!] iptables command failed: {e}", file=sys.stderr)
        state['triggered'] = True
        #if configured to stop after one "correct" packet, return true so sniff's stop_filter can stop
        return cfg.once
    return False

def main():
    cfg = parse_args()
    state = {'triggered': False}
    bpf_filter = f"tcp and dst port {cfg.port}"
    print(f"Listening for IPv4 packets to port {cfg.port} (iface={cfg.iface}) with BPF filter '{bpf_filter}'")
    print(f"Run as root to capture packets and modify iptables (or use --dry-run for testing).")

    def stop_filter(pkt):
        try:
            return handle_packet(pkt, cfg, state)
        except Exception as e:
            print(f"[!] Error handling packet: {e}", file=sys.stderr)
            return False

    try:
        sniff(iface=cfg.iface, prn=lambda pkt: None, store=False, filter=bpf_filter, stop_filter=stop_filter)
    except KeyboardInterrupt:
        print("\nExiting on user interrupt.")
    except Exception as e:
        print(f"[!] Error while sniffing: {e}", file=sys.stderr)

    if state['triggered']:
        print(f"[*] Trigger condition met.")
    else:
        print(f"[*] Exiting without trigger.")

if __name__ = "__main__":
    main()
