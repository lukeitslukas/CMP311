from datetime import datetime
import os
import glob
import os.path
from paramiko import SSHClient, AutoAddPolicy
from rich import print

save_path = 'Results'  # Directory for all results
absolute_file = str("")  # Unique File name bundled with Directory (C:/Results/"PCname"/)
result_file = ""
sub_directory = ""
machine_name = ""  # Used for writing to Results file and MasterFile
master_file = "Results/MasterFile.csv"


def create_master():  # Creates master file if not already created
    if not os.path.exists(master_file):
        f = open(master_file, 'x')
        f.close()
    open(master_file, 'w').close()  # Wipes master file on each run


def create_directories(hostname):  # Create Results Directory, and subdirectories, if they do not already exist
    global absolute_file, sub_directory
    directory = "Results/"
    sub_directory = directory + hostname + "Logs"
    if not os.path.exists(directory):  # Create Results Directory if it does not already exist
        os.makedirs(directory)
    if not os.path.exists(sub_directory):  # Create subdirectory (PC name in workgroup) if it does not already exist
        os.makedirs(sub_directory)

    absolute_file = sub_directory

    return absolute_file, sub_directory


def remote_connection():  # Code to connect to other machines, run batch file and write output to file
    global machine_name
    hosts = ['192.168.0.32', '192.168.0.33']  # List of IPs for client PCs

    for host in hosts:
        client = SSHClient()
        user = os.getlogin()
        client.load_host_keys('C:/Users/' + user + '/.ssh/known_hosts')
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.load_system_host_keys()

        # Do not alter program to connect using password, as it will be visible in plaintext in this file
        client.connect(host, username='SecurityAdmin')  # No password as SSH keys are used

        host_command = 'hostname'  # Command to retrieve name of PC
        commands = ['softwareList.bat']  # Name of batch file on Remote PC

        stdin, stdout, stderr = client.exec_command(host_command)  # Command to receive name of PC
        stdin.close()

        if stdout.channel.recv_exit_status() == 0:
            hostname = f'{stdout.read().decode("utf8")}'
            hostname = hostname.strip('\r\n')
            print("Connected to:", hostname)
            machine_name = hostname
            create_directories(hostname)  # Pass PC name to create_directories function

        else:
            print(f'STDERR: {stderr.read().decode("utf8")}')  # Displays error message

        stdout.close()
        stderr.close()

        generate_file(hostname)  # Run generate_file function, has to be done after successfully getting hostname

        global absolute_file
        f = open(absolute_file, "w")

        for command in commands:  # Runs through commands
            stdin, stdout, stderr = client.exec_command(command)
            stdin.close()

            if stdout.channel.recv_exit_status() == 0:  # Checks for error / unexpected output
                output = f'{stdout.read().decode("utf8")}'  # Stores result of command in string
                for line in output:
                    f.write(line)  # Writing output to csv file
                f.close()
                print("Finding Newly installed programs...")
                compare_programs()  # Runs function
            else:
                print(f'STDERR: {stderr.read().decode("utf8")}')  # Displays error message

            stdout.close()
            stderr.close()
        client.close()  # Closes SSH connection with Client machine


def compare_programs():
    global absolute_file, result_file, sub_directory, machine_name, master_file

    list_of_files = glob.glob(sub_directory + '\*.csv')  # Retrieves list of files in directory using the .csv format
    list_of_files.sort(reverse=True, key=os.path.getctime)  # Sort files by creation date, newest to oldest

    number_of_files = len(os.listdir(sub_directory))  # Finds number of files in directory
    if number_of_files > 1:  # Checks to make sure there is more than one file so comparison doesn't fail

        t1 = open(list_of_files[0], 'r')  # Opens file newly created
        file1 = t1.readlines()   # Reads file line by line, stores it
        t1.close()  # Closes file

        t2 = open(list_of_files[1], 'r')  # Opens second-newest file in Directory
        file2 = t2.readlines()  # Reads file line by line, stores it
        t2.close()  # Closes file

        with open(result_file, 'w') as f:  # Opens file for writing
            f.write(machine_name + ': ')  # Writes name of machine current connected to with SSH
            for line in file1:
                if line not in file2:  # Writes any new lines not present in file2 to result_file
                    line = line.strip()  # Removes new line (\n)
                    f.write(line)  # Writes line
                    f.write(", ")  # Writes comma for separation of programs
        f.close()  # Closes file

        with open(result_file, 'r') as firstfile, open(master_file, 'a') as secondfile:  # Opens result and master file
            for line in firstfile:  # Writing each line from result file to master file
                secondfile.write(line)
            secondfile.write('\n')  # Writes new line so there's a space between each list of programs

        firstfile.close()  # Closes file
        secondfile.close()  # Closes file

        print("Results for", machine_name, "have been stored in the MasterFile.")

    elif number_of_files < 1:  # Code to catch exception. Not sure how this would occur but coded in just for safety
        print("ERROR: There should be at least 1 file present in the directory")
        return

    else:  # On first use of the program, only one file is generated. Halts program before comparison fails
        print("Initial setup Complete. Run the program again to generate another file and compare installed programs.")
        return


def generate_file(hostname):
    current_datetime = datetime.now().strftime("%Y%m%d-%H%M%S")  # Using Date and time for unique file name
    global absolute_file, result_file, master_file
    directory = "Results/"
    filename = current_datetime + ".csv"
    result_file = hostname + ".csv"
    global save_path
    absolute_file = os.path.join(absolute_file, filename)  # Combing directory path and unique file name
    result_file = directory + result_file
    f = open(absolute_file, 'x')  # Creating unique file in directory

    print("New Log created:", absolute_file)
    f.close()

    if not os.path.exists(result_file):  # Check to see if file already exists, if not, creates it
        f2 = open(result_file, 'x')  # Creating file for comparison results (1 per client machine)
        f2.close()

    return absolute_file, result_file


def run_script():  # Order functions are executed, do not change
    create_master()
    remote_connection()
    print("Program Finished Successfully!")


run_script()  # Runs program
