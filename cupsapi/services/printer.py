""" Printer Service """
from cupsapi.services import BaseService
import tempfile
import cups

class Printer(BaseService):
    """ The main printer service for dealing with CUPS """
    def __init__(self, printer_name, cups_server="localhost", options={}):
        super().__init__()
        self.printer_name = printer_name
        self.cups_server = cups_server
        self.options = options
        self.print_job = "CUPSAPI Print"


    def print(self, text=None, file_data=None):
        """ Print to the printer """
        conn = cups.Connection(host=self.cups_server)
        if text:
            error = self._print_text(conn, text)

        if file_data:
            error = self._print_file(conn, file_data)

        return error


    def _print_text(self, conn, text):
        """ Print plain text """
        try:
            with tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8") as temp_file:
                temp_file.write(text)

            conn.printFile(
                self.printer_name,
                temp_file.name,
                self.print_job,
                self.options
            )
            return ""
        
        except FileNotFoundError:
            return "Error: Unable to create temporary file for printing."
        
        except cups.IPPError as e:
            return f"CUPS error: {e}"
        
    def _print_file(self, conn, file_data):
        """ print a file """
        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(file_data)

            conn.printFile(
                self.printer_name,
                temp_file.name,
                self.print_job,
                self.options
            )
            return ""
        
        except cups.IPPError as e:
            return f"CUPS error: {e}"