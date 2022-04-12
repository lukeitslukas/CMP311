import nmap
import os

Scan = nmap.PortScanner()
os.remove("oldOutput.txt")
os.rename("newOutput.txt", "oldOutput.txt")

hostFile = open('targets.txt')
ipFile = open("IP list.txt", "w")
output = open("newOutput.txt", "w")
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

        output.write(host)

        mac = "-"
        vendorName = "-"

        if 'mac' in Scan[host]['addresses']:
            mac = Scan[host]['addresses']['mac']
            output.write(", " + mac)

        print('State : %s' % Scan[host].state())
        if Scan[host].all_protocols():
            output.write(", ")
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
            output.write("\n")
else:
    print('Targets list is empty, exiting.')

ipFile.close()
