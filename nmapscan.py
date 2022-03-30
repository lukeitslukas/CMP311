# Press Shift+F10 to execute it
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import nmap

Scan = nmap.PortScanner()

hostFile = open('targets.txt')
ipFile = open("IP list.txt", "w")
output = open("Full output.txt", "w")
targets = hostFile.read()
hostFile.close()

first = True

if len(targets) != 0:
    Scan.scan(hosts=targets, arguments='-T4')
    print(targets)
    print('Scan Complete!')
    for host in Scan.all_hosts():
        if first:
            first = False
        else:
            ipFile.write(", ")

        ipFile.write(host)

        print('----------------------------------------------------')
        print('Host : %s (%s)' % (host, Scan[host].hostname()))

        output.write(host + ", ")

        mac = "-"
        vendorName = "-"

        if 'mac' in Scan[host]['addresses']:
            mac = Scan[host]['addresses']['mac']
            output.write(mac + ", ")

        print('State : %s' % Scan[host].state())
        for proto in Scan[host].all_protocols():
            print('----------')
            print('Protocol : %s' % proto)
            output.write(proto + "; ")
            ports = Scan[host][proto].keys()

            fst = True
            for port in ports:
                if fst:
                    fst = False
                else:
                    output.write(", ")
                output.write(str(port) + ": " + Scan[host][proto][port]['state'])
                print('port : %s\t state : %s' % (port, Scan[host][proto][port]['state']))
            output.write("\n")
else:
    print('Targets list is empty, exiting.')

ipFile.close()
