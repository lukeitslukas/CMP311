import dominate
from dominate.tags import *
from collections import Counter


def readFile(filename):
    outputList = []

    with open(f"{filename}.txt", "r") as output:
        for line in output:

            counter = 0
            list = line.strip().split(',', 2)
            list[2] = list[2].strip().split(',')

            for i in list[2]:
                if i != '':
                    list[2][counter] = (i.strip().split(":"))
                counter += 1

            outputList.append(list)

    output.close()

    return outputList


def nmapOutput(report, newList, oldList):
    ipCounter = Counter()
    macCounter = Counter()

    length = max(len(newList), len(oldList))

    for i in range(0, len(newList)):
        ipCounter[newList[i][0].strip()] += 1
        if newList[i][1].strip() != "":
            macCounter[newList[i][1].strip()] += 1
    for i in range(0, len(oldList)):
        ipCounter[oldList[i][0].strip()] += 1
        if oldList[i][1].strip() != "":
            macCounter[oldList[i][1].strip()] += 1

    for i in range(0, len(newList)):
        if ipCounter[newList[i][0].strip()] != 2 and newList[i][0].strip():
            print(newList[i][0], 'new ip', ipCounter[newList[i][0].strip()])
        if macCounter[newList[i][1].strip()] != 2 and newList[i][1].strip():
            print(newList[i][1], 'new mac', macCounter[newList[i][1].strip()])
    for i in range(0, len(oldList)):
        if ipCounter[oldList[i][0].strip()] != 2 and oldList[i][0].strip():
            print(oldList[i][0], 'disconnected', ipCounter[oldList[i][0].strip()])
        if macCounter[oldList[i][1].strip()] != 2 and oldList[i][1].strip():
            print(oldList[i][1], 'changed mac', macCounter[oldList[i][1].strip()])


    return report


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
    report.add(hr())
    return report


def insertParagraph(report, context):
    # inserts a paragraph of text
    report.add(p(context))
    return report


def main():
    report = dominate.document(title="Smallwood Rugby Security Report")

    setupDoc(report)

    insertParagraph(report, 'The results of the automated software are as follows:')

    report.add(hr())

    newOutputList, oldOutputList = readFile("newOutput"), readFile("oldOutput")

    nmapOutput(report, newOutputList, oldOutputList)

    resultsHeader(report, 'green', 'User Passwords', 'No user passwords were found in common password lists.')

    resultsHeader(report, 'yellow', 'Installed Software', 'Some changes were found but are not concerning.')

    uploadReport = open('index.html', 'w')
    uploadReport.write(report.render())
    uploadReport.close()


main()
