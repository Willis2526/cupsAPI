""" The default routes for the application. """
from typing import List

from fastapi import File, Form, UploadFile

from cupsapi.routers import BaseRouter
from cupsapi.services import printer


class DefaultRouter(BaseRouter):
    """ The default router for the application. """

    def __init__(self):
        super().__init__()
        self.router.add_api_route(
            "/", self.index, methods=["GET"], include_in_schema=False
        )
        self.router.add_api_route("/print", self.print, methods=["POST"])

    async def index(self):
        instructions = {
            "success": True,
            "message": "Use one of the endpoints listed to interact.",
            "endpoints": ["/print"]
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

        return result
