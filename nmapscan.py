import nmap
import os

Scan = nmap.PortScanner()

if os.path.exists("oldOutput.xml"):
    os.remove("oldOutput.xml")

if os.path.exists("newOutput.xml"):
    os.rename("newOutput.xml", "oldOutput.xml")

hostFile = open('targets.txt')
ipFile = open("IP list.txt", "w")
xmlOutput = open("newOutput.xml", "wb")
targets = hostFile.read()
hostFile.close()
first = True

if len(targets) != 0:
    Scan.scan(hosts=targets, arguments='-T4')
    print(targets)
    print('Scan Complete!')

    xmlOutput.write(Scan.get_nmap_last_output())
    print("XML Output:\n")
    print(str(Scan.get_nmap_last_output()))

    for host in Scan.all_hosts():
        if first:
            first = False
        else:
            ipFile.write(", ")

        ipFile.write(host)
else:
    print('Targets list is empty, exiting.')

ipFile.close()
xmlOutput.close()
