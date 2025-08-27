import socket
from django.shortcuts import render
from scapy.all import sniff, IP, TCP, UDP
from collections import Counter

# Devices
devices_list = []

def devices(request):
    global devices_list
    if request.method == "POST":
        ip = request.POST.get("ip")
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except Exception:
            hostname = "Unknown"
        devices_list.append({"ip": ip, "hostname": hostname, "mac": None})
    return render(request, "devices.html", {"devices": devices_list})


# Ports
def ports(request):
    result = None
    if request.method == "POST":
        ip = request.POST.get("ip")
        open_ports = []
        for port in [22, 80, 443, 3306]:
            try:
                s = socket.socket()
                s.settimeout(0.5)
                s.connect((ip, port))
                open_ports.append(port)
                s.close()
            except:
                pass
        result = {"ip": ip, "open_ports": open_ports}
    return render(request, "ports.html", {"result": result})


def analyze_packets(target_ip, packet_count=50):
    stats = Counter()

    def handler(pkt):
        if IP in pkt:
            # Filter by target_ip if provided
            # if target_ip and not (pkt[IP].src == target_ip or pkt[IP].dst == target_ip):
            #     return

            if pkt.haslayer(TCP):
                proto = f"TCP:{pkt[TCP].dport}"
            elif pkt.haslayer(UDP):
                proto = f"UDP:{pkt[UDP].dport}"
            else:
                proto = "Other"
            stats[proto] += 1

    sniff(prn=handler, count=packet_count, store=False)
    return stats

def traffic(request):
    ip = request.GET.get("ip", None)  # user enters IP via form
    data = None
    if ip:
        data = analyze_packets(ip, packet_count=50)  # sniff 50 packets for that IP

    return render(request, "traffic.html", {"protocols": dict(data) if data else None, "ip": ip})



# Firewall
# rules = []

# def firewall(request):
#     global rules
#     if request.method == "POST":
#         ip = request.POST.get("ip")
#         port = request.POST.get("port")
#         action = request.POST.get("action")
#         rules.append({"ip": ip, "port": port, "action": action})
#     return render(request, "firewall.html", {"rules": rules})
