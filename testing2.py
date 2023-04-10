import nmap

target_host = "example.com"

nm = nmap.PortScanner()
nm.scan(hosts=target_host, arguments="-T4 -F")

for host in nm.all_hosts():
    print(f"Host : {host} ({nm[host].hostname()})")
    print(f"State : {nm[host].state()}")
    for proto in nm[host].all_protocols():
        print("----------")
        print(f"Protocol : {proto}")

        lport = nm[host][proto].keys()
        for port in lport:
            print(f"Port : {port}\tState : {nm[host][proto][port]['state']}")
