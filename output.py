import dominate
from dominate.tags import *


def setupDoc(report):
    with report.head:
        link(rel='stylesheet', href='css/style.css')

    with report:
        with div(id='header'):
            h2('Smallwood Rugby Security Report')
    return report


def resultsParagraph(report, colour, title, context):
    # creates a title showing coloured box depending on status
    message = ""
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

    resultsParagraph(report, 'red', 'NMap Scan Results', 'There are several changes since the last scan.')

    resultsParagraph(report, 'green', 'User Passwords', 'No user passwords were found in common password lists.')

    resultsParagraph(report, 'yellow', 'Installed Software', 'Some changes were found but are not concerning.')

    uploadReport = open('index.html', 'w')
    uploadReport.write(report.render())
    uploadReport.close()


main()
