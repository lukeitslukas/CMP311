import subprocess
import time
from datetime import datetime
import os
import glob
import csv
import os.path
from paramiko import SSHClient, AutoAddPolicy
from rich import print

save_path = 'C:/Results'  # Directory for all results
absolute_file = str("")  # Unique File name bundled with Directory (C:/Results/"PCname"/)


def create_directories(hostname):  # Create Results Directory, and subdirectories, if they do not already exist
    global absolute_file
    directory = "C:/Results/"
    sub_directory = directory + hostname
    print(sub_directory)
    if not os.path.exists(directory):  # Create Results Directory if it does not already exist
        os.makedirs(directory)
    if not os.path.exists(sub_directory):  # Create subdirectory (PC name in workgroup) if it does not already exist
        os.makedirs(sub_directory)

    absolute_file = sub_directory

    return absolute_file


def remote_connection():  # Code to connect to other machines, run batch file and write output to file
    hosts = ['192.168.0.32', '192.168.0.33']  # List of IPs for client PCs

    for host in hosts:
        client = SSHClient()
        user = os.getlogin()
        client.load_host_keys('C:/Users/' + user + '/.ssh/known_hosts')
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.load_system_host_keys()

        # client.connect('192.168.0.32', username='SecurityAdmin', password='admin')  # Dont use if SSH keys are
        # available
        client.connect(host, username='SecurityAdmin')

        # commands = ['echo Test', 'hostname']
        host_command = 'hostname'
        commands = ['softwareList.bat']  # Name of program on Remote PC

        stdin, stdout, stderr = client.exec_command(host_command)  # Command to receive name of PC
        stdin.close()

        if stdout.channel.recv_exit_status() == 0:
            hostname = f'{stdout.read().decode("utf8")}'
            print(hostname)  # DEBUG CODE REMOVE WHEN FINISHED
            hostname = hostname.strip('\r\n')
            create_directories(hostname)  # Pass PC name to create_directories function

        else:
            print(f'STDERR: {stderr.read().decode("utf8")}')  # Displays error message

        stdout.close()
        stderr.close()

        generate_file()  # Run generate_file function, has to be done after successfully getting hostname

        global absolute_file
        f = open(absolute_file, "w")

        for command in commands:  # Runs through commands
            stdin, stdout, stderr = client.exec_command(command)
            stdin.close()

            if stdout.channel.recv_exit_status() == 0:  # Checks for error / unexpected output
                output = f'{stdout.read().decode("utf8")}'  # Stores result of command in string
                print(output)
                for line in output:
                    f.write(line)  # Writing output to csv file
            else:
                print(f'STDERR: {stderr.read().decode("utf8")}')  # Displays error message

            stdout.close()
            stderr.close()
        client.close()


"""
# Old code that only ran on host machine, will remove in final version
def find_programs():
    global absolute_file
    f = open(absolute_file, "wb")

    output = subprocess.Popen(
        "softwareList.bat",
        stdout=subprocess.PIPE).stdout

    for line in output:
        f.write(line)  # Writing output to file

    output.close()
    print("Finished Successfully!")
    print(absolute_file)  # TEST LINE REMOVE WHEN FINISHED
    return
"""


def diff(lines1, lines2):  # Function to compare lists
    return list(set(lines1) - set(lines2)) + list(set(lines2) - set(lines1))  #


def compare_programs():  # Does not work with current version
    global absolute_file

    list_of_files = glob.glob('C:/Results/*.csv')  # Retrieves list of files in directory using the .csv format
    sorted_files = sorted(list_of_files, key=os.path.getctime)

    number_of_files = len(os.listdir("C:/Results"))
    if number_of_files > 1:

        print("COMPARE TEST CHECKPOINT 1")  # DEBUG CODE

        f1 = open(absolute_file, "r")  # Opens the newest file
        f2 = open(sorted_files[-2], "r")  # Opens the second-newest file

        lines1 = f1.readlines()  # Stored first file in list
        lines2 = f2.readlines()  # Stores second file in list

        diff_results = (diff(lines1, lines2))  # Use function to find differences between the two lists

        # Code to tidy up the output
        diff_results = list(map(lambda x: x.replace('DisplayName : ', '').replace('\n', ''), diff_results))

        diff_results2 = str(diff_results)[1:-1]  # Removes Square Brackets from output
        print(diff_results2)
        data = [diff_results2]

        with open("newPrograms.csv", 'w') as f:

            writer = csv.writer(f)

            writer.writerow(data)  # Write output to CSV file

    elif number_of_files < 1:  # Code to catch exception. Not sure how this would occur but coded in just for safety
        print("ERROR: There should be at least 1 file present in the directory")
        quit()

    else:  # On first use of the program, only one file is generated. Halts program before comparison fails
        print("Initial setup Complete. Run the program again to generate another file and compare installed programs.")
        quit()


def generate_file():
    current_datetime = datetime.now().strftime("%Y%m%d-%H%M%S")  # Using Date and time for unique file name
    global absolute_file
    file1 = current_datetime + ".csv"
    global save_path
    absolute_file = os.path.join(absolute_file, file1)  # Combing directory path and unique file name
    print(absolute_file)  # TESTING CODE
    f = open(absolute_file, 'x')  # Creating unique file in directory

    print("New File created : ", absolute_file)
    f.close()

    return absolute_file


def run_script():
    remote_connection()
    # compare_programs()  # Not fully implemented for current version


run_script()
