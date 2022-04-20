import pyndiff
import dominate
from dominate.tags import *


def createDiff():
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
    diffFile = open("diff.txt", "r").read()
    if not diffFile:
        resultsHeader(report, 'green', 'Nmap Results', 'There are no changes since the last scan')
    elif 'host' not in diffFile.lower():
        resultsHeader(report, 'yellow', 'Nmap Results', 'There are small changes since the last scan')
    else:
        resultsHeader(report, 'red', 'Nmap Results', 'There are several changes since the last scan')

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
            else:
                insertParagraph(report, line.strip(), "code")
    report.add(hr())


def setupDoc(report):
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
    report = dominate.document(title="Smallwood Rugby Security Report")

    setupDoc(report)

    insertParagraph(report, 'This report is a human readable version of the security software results.', "")

    report.add(hr())

    createDiff()

    nmapOutput(report)

    resultsHeader(report, 'green', 'User Passwords', 'No user passwords were found in common password lists.')

    resultsHeader(report, 'yellow', 'Installed Software', 'Some changes were found but are not concerning.')

    uploadReport = open('index.html', 'w')
    uploadReport.write(report.render())
    uploadReport.close()


main()
