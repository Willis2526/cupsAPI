# CupsApi Server Documentation

## Overview

The CupsApi module provides an interface to manage and control your printing tasks using the CUPS (Common UNIX Printing System) library through a FastAPI-based web service. This documentation outlines how to run and interact with the CupsApi module.

## Installation
---
>**NOTE**: This has been tested with python 3.5+ and can only be ran on Linux. A Debian based OS is assumed to be used.

### Setup Linux environment
Since pycups is a compiled C program with python bindings, certain development libraries are required to be installed. These programs are listed below. This assumes that a Debian based OS is being used.
- gcc
- make
- cups
- cups-devel (libcups2-dev)
- python3-devel (python3-dev)

Run the command below to update the system
```bash
sudo apt update && sudo apt upgrade -y
```

Run the command below to install the required applications
```bash
sudo apt install python3 python3-venv python3-dev libcups2-dev gcc cups
```

### Setup program environment
**To install just a local dev environment, run the commands below to install dependencies and a local environment**
```bash
make local
```

**To install the program as a service, run the commands below to install dependencies and the systemd service file**

>**NOTE**: Installing the service file assumes that the project is located under /opt/vertech

```bash
sudo make install
```

When installed, program can be ran from the command line:
```bash
python -m cupsAPI {args}
```

By default, the module runs on 0.0.0.0 (all network interfaces) and port 9095.

You can customize the behavior using the following command-line arguments:

    --debug or -d: Enable debugging mode.
    --port or -p: Set the web app's port number.
    --address or -a: Set the web app's address.
    --path: Define the path to your FastAPI application (e.g., cupsapi.app:app).

## Interacting with the API

Once the CupsApi module is running, you can interact with it via HTTP requests. The API exposes endpoints for printing tasks, and you can use HTTP clients like curl or Python libraries like requests to interact with it.

Here is an example of how to make a print request using curl:
```bash
curl -X POST http://localhost:9095/print \
  -F "printer_name=printerName" \
  -F "mode=text" \
  -F "cups_server=localhost" \
  -F "options=media=A4" \
  -F "options=sides=one-sided" \
  -F "text=Hello, World!"
```

Replace the parameter values with your specific printer details and printing options.

### API Endpoints

The CupsApi module provides the following API endpoints:

**GET /**

    Description: Main endpoint for information and usage instructions.

    Method: GET

    Usage: Access this endpoint to get instructions on how to interact with the CupsApi module.

**GET /printers**

    Description: View a list of available printers for a given server.

    Method: GET

    Usage: Access this endpoint to get a list of available printers for a cups server.

    Query Parameters:
        cups_server: The hostname or address for a cups server. The cups server must be accessible to this server.

**POST /print**

    Description: Submit print jobs with various printing options.

    Method: POST

    Usage: Use this endpoint to submit print jobs with customizable options. You can provide parameters such as printer_name, cups_server, options, text, and files to initiate printing tasks.

    Request Body Parameters:
        printer_name: The name of the printer you want to use.
        cups_server (optional): The CUPS server address (default is "localhost").
        options (optional): Additional printing options in the format "key=value."
        text (optional): Text content to print.
        files (optional): List of files to print.

## Troubleshooting

If you encounter issues or errors while using the CupsApi module, make sure to check the logs and consult this CupsApi documentation for further guidance.

## Conclusion

The CupsApi module simplifies the process of managing and controlling your printing tasks. By following the instructions outlined in this documentation, you can effectively utilize this module to meet your printing needs.

For any further assistance or questions, please feel free to reach out to our support team.

Enjoy printing with CupsApi!