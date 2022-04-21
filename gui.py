import PySimpleGUI as mwin
import os
from matplotlib.pyplot import margins

#main window

layout = [
    #[mwin.Text("Enter IP address to scan")],
    #[mwin.InputText()],
    #[mwin.Button("Scan Selected Network")],

    [mwin.Button("Execute Network Scanner")],
    [mwin.Button("Show IP address")],
    [mwin.Button("Exit")],

]

window = mwin.Window("Network Scanner", layout, margins=(200,100))

while True:
    event, values = window.read()
    # ipvalue = values[0]

    if event == "Execute Network Scanner":
        os.system('python merger.py')

    elif event == "Show IP address":
        os.system('ipconfig /all')


    elif event == "Exit" or event == mwin.WIN_CLOSED:
        break

window.close