""" 
Wrapper for CUPS C library. Provides printing functionality to CUPS printer.

Documentation can be found here:
http://nagyak.eastron.hu/doc/system-config-printer-libs-1.2.4/pycups-1.9.51/html/

Based on pycups:
https://github.com/OpenPrinting/pycups

"""

import io
import sys

import cups
from reportlab.lib.pagesizes import landscape, letter, portrait
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas

HEIGHT, WIDTH = letter
HEADER_TITLE = HEIGHT - (0.45 * inch)
ROW_SIZE = 14
ROW_START = HEIGHT - (1.5 * inch)
ROW_STOP = 1.00 * inch
PORTRAIT = 3
LANDSCAPE = 4


class CupsPrinter:
    """ Class for communicating with CUPS printer """

    def __init__(self, server, printerName, user="python") -> None:
        self.canvasPageOrientations = {
            "landscape": landscape,
            "portrait": portrait
        }

        # Set CUPS server and user to connect as
        cups.setServer(server)
        cups.setUser(user)

        self.conn = cups.Connection()
        self.printer = printerName

    def createPrintJob(self, fileName, format=cups.CUPS_FORMAT_AUTO, params=None):
        """ Create a print job """
        if not self.conn or not self.printer:
            return

        printParams = {"document-format": format}
        if params:
            printParams.update(params)

        jobId = self.conn.createJob(
            self.printer,
            fileName,
            printParams
        )
        self.conn.startDocument(
            self.printer,
            jobId,
            fileName,
            cups.CUPS_FORMAT_AUTO,
            1
        )

    def finishPrintJob(self):
        """ Finish the print job """
        self.conn.finishDocument(self.printer)

    def printText(self, text, fileName, orientation="portrait"):
        """ print text to printer """
        pageOrientation = self.canvasPageOrientations[orientation.lower()]

        self.createPrintJob(fileName)

        with io.BytesIO() as fileobj:
            c = Canvas(fileobj, pagesize=pageOrientation(letter))
            c.drawCentredString(WIDTH / 2, HEADER_TITLE, text)
            c.save()
            pdf = fileobj.getvalue()
            pdfSize = sys.getsizeof(pdf)
            self.conn.writeRequestData(pdf, pdfSize)

        self.finishPrintJob()

    def printReport(self, report, fileName, orientation="portrait"):
        """ Print binary report file to printer """
        reportSize = sys.getsizeof(report)

        self.createPrintJob(fileName)
        self.conn.writeRequestData(report, reportSize)
        self.finishPrintJob()


if __name__ == "__main__":
    c = CupsPrinter("10.0.10.2", "EPSON_ET_3710_Series")
    c.printText("Hello from CUPS printer wrapper", "Test DOC", "landscape")
