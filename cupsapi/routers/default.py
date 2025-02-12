""" The default routes for the application. """
from typing import Any, List, Optional

from fastapi import File, Form, UploadFile

from cupsapi.routers import BaseRouter
from cupsapi.services import printer
from fastapi import Request

class DefaultRouter(BaseRouter):
    """ The default router for the application. """

    def __init__(self):
        super().__init__()
        self.router.add_api_route(
            "/", self.index, methods=["GET"], include_in_schema=False
        )
        self.router.add_api_route("/print", self.print, methods=["POST"])
        self.router.add_api_route("/printers", self.list_printers, methods=["GET"])

    async def index(self, request: Request):
        # Get the base URL from the request
        scheme = request.headers.get("x-forwarded-proto", request.url.scheme)
        hostname = request.headers.get("x-forwarded-host", request.url.hostname)
        port = request.url.port

        # If x-forwarded-host is missing, fall back to request.base_url
        if not hostname:
            base_url = str(request.base_url).rstrip("/")
        else:
            base_url = f"{scheme}://{hostname}"
            if port and port not in [80, 443]:  # Include port if it's not default
                base_url += f":{port}"
        
        instructions = {
            "success": True,
            "message": "You can interact with the CupsAPI module using the following endpoints.",
            "endpoints": [
                {
                    "path": f"{base_url}/print",
                    "methods": ["POST"],
                    "description": "Submit print jobs with various printing options."
                },
                {
                    "path": f"{base_url}/printers",
                    "methods": ["GET"],
                    "description": "View a list of available printers for a given server."
                },
                {
                    "path": f"{base_url}/docs",
                    "methods": ["GET"],
                    "description": "Access API documentation for the CupsAPI module."
                }
            ]
        }
        return instructions
    
    async def list_printers(self, cups_server: str):
        """ List the printers on a cups server """
        result = {"success": False, "message": "", "printers": []}

        try:
            printer_response = printer.get_printers_list(cups_server)

            if printer_response["message"]:
                result["message"] = printer_response["message"]
                return result

            result["success"] = True
            result["printers"] = printer_response["printers"]
        except Exception as e:
            result["message"] = str(e)

        return result

    async def print(
        self,
        printer_name: str = Form(...),
        cups_server: str = Form(None),
        options: Optional[List[str]] = Form(None),
        text: Optional[str] = Form(None),
        files: Optional[Any] = File(None)
    ):
        result = {"success": False, "message": ""}
        error = None

        # Add in default options
        if not options or options and options[0] == "":
            options = ["media=A4", "sides=one-sided"]

        try:
            try:
                parsed_options = dict(option.split("=") for option in options)
            except ValueError:
                result["message"] = 'Invalid options format. Use "key=value" format.'
                return result
            
            print_job = printer.Printer(
                printer_name,
                cups_server,
                parsed_options
            )

            if not text and not files:
                result["message"] = "Either files or text must be sent"
                return result

            if files:
                if not isinstance(files, list):
                    files = [files]

                for file in files:
                    file_data = file.file.read()
                    error = print_job.print(file_data=file_data)

            if text:
                error = print_job.print(text=text)

            if error:
                result["message"] = error
                return result

            result["success"] = True
            result["message"] = f"Sent to printer {printer_name}"
            
        except Exception as e:
            result["message"] = str(e)

        return result
