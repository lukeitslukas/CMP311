import subprocess
from datetime import datetime
import os
import glob

save_path = 'C:/Results'  # Directory for all results
absolute_file = str("")  # Unique File name bundled with Directory (C:/Results)


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


def diff(lines1, lines2):  # Function to compare lists
    return list(set(lines1) - set(lines2)) + list(set(lines2) - set(lines1))  #


def compare_programs():
    list_of_files = glob.glob('C:/Results/*.txt')  # Retrieves list of files in directory using the .txt format
    latest_file = max(list_of_files, key=os.path.getctime)  # Gets the file that was lasted created in the directory
    sorted_files = sorted(list_of_files, key=os.path.getctime)

    number_of_files = len(os.listdir("C:/Results"))
    if number_of_files > 1:
        print("The latest file created is : ", sorted_files[-1])  # Finds File newly created
        print("The second latest file created is : ", sorted_files[-2])  # Finds File previously created

        print("COMPARE TEST CHECKPOINT 1")  # DEBUG CODE

        f1 = open(sorted_files[-1], "r")  # Opens the newest file
        f2 = open(sorted_files[-2], "r")  # Opens the second-newest file

        lines1 = f1.readlines()  # Stored first file in list
        lines2 = f2.readlines()  # Stores second file in list

        print(diff(lines1, lines2))  # Use function to find differences between the two lists

    elif number_of_files < 1:  # Code to catch exception. Not sure how this would occur but coded in just for safety
        print("ERROR: There should be at least 1 file present in the directory")
        quit()

    else:  # On first use of the program, only one file is generated. Halts program before comparison fails
        print("Initial setup Complete. Run the program again to generate another file and compare installed programs.")
        quit()


def generate_file():
    current_datetime = datetime.now().strftime("%Y%m%d-%H%M%S")  # Using Date and time for unique file name
    global absolute_file
    file1 = current_datetime + ".txt"
    global save_path
    absolute_file = os.path.join(save_path, file1)  # Combing directory path and unique file name
    print(absolute_file)  # TESTING CODE
    f = open(absolute_file, 'x')  # Creating unique file in directory

    print("New File created : ", absolute_file)
    f.close()

    return absolute_file


def run_script():  # Order executing functions in
    generate_file()
    find_programs()
    compare_programs()


run_script()
