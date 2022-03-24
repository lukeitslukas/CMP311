# Press Shift+F10 to execute it
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import nmap

Scan = nmap.PortScanner()

hostFile = open('targets.txt')
ipFile = open("IP list.txt", "w")
targets = hostFile.read()
hostFile.close()

first = True

if len(targets) != 0:
    Scan.scan(hosts=targets)
    print(targets)
    print('Scan Complete!')
    for host in Scan.all_hosts():
        if first:
            ipFile.write(host)
            first = False
        else:
            ipFile.write(", " + host)

        print('----------------------------------------------------')
        print('Host : %s (%s)' % (host, Scan[host].hostname()))
        print('State : %s' % Scan[host].state())
        for proto in Scan[host].all_protocols():
            print('----------')
            print('Protocol : %s' % proto)

            ports = Scan[host][proto].keys()
            for port in ports:
                print('port : %s\t state : %s' % (port, Scan[host][proto][port]['state']))
else:
    print('Targets list is empty, exiting.')

ipFile.close()
