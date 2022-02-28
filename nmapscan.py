import nmap
import sys

Scan = nmap.PortScanner()

position = 1
hosts = ''

while len(sys.argv) > position:
    hosts = hosts + sys.argv[position]
    position = position + 1

if len(sys.argv) == 1:
    print('Please provide target(s)')

else:
    Scan.scan(hosts=hosts)

    for host in Scan.all_hosts():
        print('----------------------------------------------------')
        print('Host : %s (%s)' % (host, Scan[host].hostname()))
        print('State : %s' % Scan[host].state())
        for proto in Scan[host].all_protocols():
            print('----------')
            print('Protocol : %s' % proto)

            ports = Scan[host][proto].keys()
            for port in ports:
                print('port : %s\t state : %s' % (port, Scan[host][proto][port]['state']))