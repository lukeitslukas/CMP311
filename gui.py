import PySimpleGUI as mwin
import os
from matplotlib.pyplot import margins

#main window

layout = [
    [mwin.Button("Show IP")],
    [mwin.Button("Scan Network")],
    [mwin.Button("Scan Network and save to txt file")],
    [mwin.Button("Exit")],

]

window = mwin.Window("Network Scanner", layout, margins=(200,100))

while True:
    event, values = window.read()
    if event == "Show IP":
        os.system('ifconfig')

    elif event == "Scan Network and save to txt file":
        os.system('nmap 192.168.0.0/24 > output.txt')

    elif event == "Scan Network":
        os.system('nmap 192.168.0.0/24')

    elif event == "Exit" or event == mwin.WIN_CLOSED:
        break

window.close