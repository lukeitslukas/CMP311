import nmap
import os

Scan = nmap.PortScanner()           #Declaring an object for the nmap scan called Scan

if os.path.exists("oldOutput.xml"):         #Changing the name of the last output to oldOutput.xml so outputs can be compared
    os.remove("oldOutput.xml")

if os.path.exists("newOutput.xml"):
    os.rename("newOutput.xml", "oldOutput.xml")

hostFile = open('targets.txt')          #Opening the file containing the IP addresses to scan
ipFile = open("IP list.txt", "w")           #Opening the file to output the IP address of every host found to be up
xmlOutput = open("newOutput.xml", "wb")     #Opening the file to store the full output in XML format
targets = hostFile.read()
hostFile.close()
first = True

if len(targets) != 0:       #Outputting if there are targets to scan, otherwise quitting


    Scan.scan(hosts=targets, arguments='-T4')       #Assigning targets
    print(targets)
    print('Scan Complete!')

    xmlOutput.write(Scan.get_nmap_last_output())        #Outputting XML
    print("XML Output:\n")
    print(str(Scan.get_nmap_last_output()))

    for host in Scan.all_hosts():           #Outputting all hosts that are up
        if first:
            first = False
        else:
            ipFile.write(", ")

        ipFile.write(host)

else:
    print('Targets list is empty, exiting.')
