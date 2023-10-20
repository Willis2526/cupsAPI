""" The default routes for the application. """
from typing import List

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

    async def index(self, request: Request):
        # Get the base URL from the request
        base_url = str(request.base_url)
        
        instructions = {
            "success": True,
            "message": "You can interact with the CupsAPI module using the following endpoints.",
            "endpoints": [
                {
                    "path": f"{base_url}print",
                    "methods": ["POST"],
                    "description": "Submit print jobs with various printing options."
                },
                {
                    "path": f"{base_url}docs",
                    "methods": ["GET"],
                    "description": "Access API documentation for the CupsAPI module."
                }
            ]
        }
        return instructions

    async def print(
        self,
        printer_name: str = Form(...),
        cups_server: str = Form(None),
        options: list = Form([]),
        text: str = Form(None),
        files: List[UploadFile] = File(None)
    ):
        result = {"success": False, "message": ""}
        error = None

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

        return result
