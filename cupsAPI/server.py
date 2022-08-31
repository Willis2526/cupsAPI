""" Reporter Server """
import base64
import json
import logging

import waitress
from flask import Flask, jsonify, request
from flask_cors import cross_origin

from cupsAPI.printer import CupsPrinter

logger = logging.getLogger(__name__)


class Server:
    """ Main server thread """

    def __init__(self, web_port, debug):
        self.app = Flask(__name__)
        self.debug = debug
        self.port = web_port

        self.version = "1.0.0"
        self.name = "CUPS REST API"

        # Store print configuration
        self.config = {"server": "", "printer": "", "reportName": "Report"}

        logging.info("Program started")

        # Setup endpoints
        self.app.add_url_rule("/", "Index", self.index, methods=["GET"])
        self.app.add_url_rule("/print", "Print", self.print, methods=["POST"])
        self.app.add_url_rule(
            "/config", "Config", self.setConfig, methods=["POST"])

    def start(self):
        """ The main target """
        if self.debug:
            self.app.run(
                host="0.0.0.0",
                port=str(self.port),
                debug=True,
                use_reloader=True,
            )
        else:
            # Disable the queue depth warning
            logging.getLogger("waitress.queue").setLevel(logging.CRITICAL)
            logger.info("Web server started on port %s", self.port)
            waitress.serve(self.app, port=self.port, _quiet=True)

    def index(self):
        """ Main entrypoint. Shows info about server """
        data = {
            "config": self.config,
            "name": self.name,
            "version": self.version
        }
        response = {"data": data, "success": False, "message": ""}

        response["success"] = True
        return jsonify(response)

    @cross_origin()
    def setConfig(self):
        """ Set print configuration """
        response = {"data": {}, "success": False, "message": ""}

        try:
            requestData = request.json

            # Set config
            self.config["server"] = requestData.get("server", "localhost")
            self.config["printer"] = requestData["printer"]
            self.config["reportName"] = requestData.get("reportName", "report")

            response["message"] = "Successfully set print configuration"
            response["success"] = True

        except Exception as e:
            response["message"] = str(e)
            logger.error("Failed to set print config: {}".format(e))

        return jsonify(response)

    @cross_origin()
    def print(self):
        """ CUPS Printer entrypoint """
        response = {"data": {}, "success": False, "message": ""}

        # Default data Content-Type should be application/octet-stream

        try:
            if not self.config["server"]:
                response["message"] = "CUPS server not set"

            elif not self.config["printer"]:
                response["message"] = "CUPS printer name not set"

            else:
                reportData = request.data

                # Check headers for anything other than
                # application/octet-stream

                # text/plain
                if request.headers["Content-Type"] == "text/plain":
                    reportData = reportData.decode()

                # image/<imageType>
                if "image" in request.headers["Content-Type"]:
                    reportData = reportData.decode("UTF-8")
                    reportData = reportData.split("base64,")[1]
                    reportData = base64.b64decode((reportData))

                dataType = type(reportData)

                c = CupsPrinter(self.config["server"], self.config["printer"])

                if dataType == bytes:
                    c.printReport(reportData, self.config["reportName"])
                if dataType == str:
                    c.printText(reportData, self.config["reportName"])

                # Reset print configuration
                self.config = {
                    "server": "",
                    "printer": "",
                    "reportName": "Report"
                }

                response["success"] = True

        except Exception as e:
            response["message"] = str(e)
            logger.error("Failed to print: {}".format(e))

        return jsonify(response)
