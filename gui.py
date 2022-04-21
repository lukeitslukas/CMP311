import PySimpleGUI as mwin
import os
from matplotlib.pyplot import margins

#main window layout with buttons

layout = [ 

    [mwin.Button("Execute Network Scanner")],
    [mwin.Button("Show IP address")],
    [mwin.Button("Exit")],

]

#main window name at the top

window = mwin.Window("Network Scanner", layout, margins=(200,100)) 

#loop that waits for user input from the menu

while True:
    event, values = window.read()
    

    if event == "Execute Network Scanner":
        os.system('python merger.py') #executes merger.py script to execute scripts one after another

    elif event == "Show IP address":
        os.system('ipconfig /all')


    elif event == "Exit" or event == mwin.WIN_CLOSED:
        break

window.close