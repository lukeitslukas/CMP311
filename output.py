import pyndiff
import dominate
from dominate.tags import *


def createDiff():
    # create diff file from the two xml files
    diff = pyndiff.generate_diff(
        "oldOutput.xml",
        "newOutput.xml",
        ignore_udp_open_filtered=False,
        output_type="txt"
    )

    file = open('diff.txt', 'w')
    file.write(diff)
    file.close()


def nmapOutput(report):
    # take diff file and output to html
    diffFile = open("diff.txt", "r").read()

    # check if new host was found, if so red, if not but some entries yellow, if none green
    if len(diffFile.strip().split('\n')) == 2:
        resultsHeader(report, 'green', 'Nmap Results', 'There are no changes since the last scan')
    elif 'host' not in diffFile.lower():
        resultsHeader(report, 'yellow', 'Nmap Results', 'There are small changes since the last scan')
    else:
        resultsHeader(report, 'red', 'Nmap Results', 'There are several changes since the last scan')

    # filter content and output to html
    for line in open("diff.txt", "r"):
        if line.strip():
            if '-Nmap' in line.strip():
                insertParagraph(report, 'Old Scan details: ' + line.strip().partition('-')[2], "code")
            elif '+Nmap' in line.strip():
                insertParagraph(report, 'New Scan details: ' + line.strip().partition('+')[2], "code")
                report.add(br())
            elif line.strip()[0] == '-':
                if '/tcp' in line.strip():
                    insertParagraph(report, 'Removed: PORT    STATE  VERSION', "code")
                    insertParagraph(report, 'Removed: ' + line.strip().partition('-')[2], "code")
                elif '/udp' in line.strip():
                    insertParagraph(report, 'Removed: PORT    STATE  VERSION', "code")
                    insertParagraph(report, 'Removed: ' + line.strip().partition('-')[2], "code")
                else:
                    insertParagraph(report, 'Removed entry: ' + line.strip().partition('-')[2], "code")
            elif line.strip()[0] == '+':
                if '/tcp' in line.strip():
                    insertParagraph(report, 'Added: PORT    STATE  VERSION', "code")
                    insertParagraph(report, 'Added: ' + line.strip().partition('+')[2], "code")
                elif '/udp' in line.strip():
                    insertParagraph(report, 'Added: PORT    STATE  VERSION', "code")
                    insertParagraph(report, 'Added: ' + line.strip().partition('+')[2], "code")
                else:
                    insertParagraph(report, 'New entry: ' + line.strip().partition('+')[2], "code")
            elif '   ' in line.strip():
                continue
            elif '\n' in line.strip():
                report.add(br())
            else:
                insertParagraph(report, line.strip(), "code")

    report.add(hr())


def programOutput(report):
    # open programFile output and filter for html output
    outputArray = []
    with open("Results/MasterFile.csv", "r") as programFileOutput:
        for line in programFileOutput:
            temp = line.strip().split(':')
            temp[1] = temp[1].strip().split(',')
            outputArray.append(temp)

    # count banned files in list
    bannedOccur = 0
    for line in outputArray:
        for item in line[1]:
            with open("BannedPrograms.txt", "r") as bannedList:
                for program in bannedList:
                    program = program.strip()
                    item = item.strip()
                    if program.lower() in item.lower():
                        bannedOccur += 1

    # display red if more than 3 found, yellow for between 3 and 0 and green if none found
    if bannedOccur >= 3:
        resultsHeader(report, 'red', 'Device Program Search', 'Three or more banned programs were found')
    elif bannedOccur > 0:
        resultsHeader(report, 'yellow', 'Device Program Search', 'Less than three banned programs were found')
    else:
        resultsHeader(report, 'green', 'Device Program Search', 'No banned programs were found')

    # format for html output
    for line in outputArray:
        msg = line[0] + ": " + line[1][0]
        for i in range(1, len(line[1])):
            if line[1][i]:
                line[1][i] = line[1][i].strip()
                msg = msg + ', ' + line[1][i]
        insertParagraph(report, msg, "code")
    report.add(hr())


def passwordOutput(report):
    # setup variables for parsing
    totalPasswords = 0
    weakPasswords = 0
    accounts = []

    # open cracked passwords file and add users to array
    with open("output.txt", "r") as passwordResultFileOutput:
        for line in passwordResultFileOutput:
            weakPasswords += 1
            accounts.append(line.strip())

    # open all passwords file and count number of users
    with open("password.txt", "r") as passwordFileOutput:
        for line in passwordFileOutput:
            if line.strip().endswith(":::"):
                totalPasswords += 1

    # check number of passwords cracked and output to html
    if (weakPasswords / totalPasswords) > 0.25:
        resultsHeader(report, 'red', 'User Passwords', 'More than 25% of passwords cracked')
        insertParagraph(report, "The following users passwords were cracked:", "")
        for line in accounts:
            insertParagraph(report, line.strip(), "code")
    elif weakPasswords > 1:
        resultsHeader(report, 'yellow', 'User Passwords', 'One or more passwords were cracked')
        insertParagraph(report, "The following users passwords were cracked:", "")
        for line in accounts:
            insertParagraph(report, line.strip(), "code")
    else:
        resultsHeader(report, 'green', 'User Passwords', 'No passwords cracked')
    report.add(hr())


def setupDoc(report):
    # setup html report
    with report.head:
        link(rel='stylesheet', href='css/style.css')

    with report:
        with div(id='header'):
            h2('Smallwood Rugby Security Report')
    return report


def resultsHeader(report, colour, title, context):
    # creates a title showing coloured box depending on status
    with report:
        with div(style='font-weight: bold;'):
            p(title, cls='title ' + colour)

    report += (p(context))
    return report


def insertParagraph(report, context, pTag):
    # inserts a paragraph of text
    report.add(p(context, cls=pTag))
    return report


def main():
    # create report document
    report = dominate.document(title="Smallwood Rugby Security Report")

    # setup doc
    setupDoc(report)

    # insert first paragraph
    insertParagraph(report, 'This report is a human readable version of the security software results.', "")

    # add line
    report.add(hr())

    # create diff file for nmap output
    createDiff()

    # filter nmap output and add to report
    nmapOutput(report)

    # filter programFile output and add to report
    programOutput(report)

    # filter passwords output and add to report
    passwordOutput(report)

    # upload document
    uploadReport = open('index.html', 'w')
    uploadReport.write(report.render())
    uploadReport.close()


main()
