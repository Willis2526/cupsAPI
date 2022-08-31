# CUPS REST API Server

## Introduction 
---
A server for sending print requests to a CUPS printer. Data can either be raw binary such as a PDF/image or plain text. Data types are specified using the Content-Type header.

Content-Type headers currently supported:
 - text/plain
 - application/octet-stream (PDF)
 - image/imageType (with imagetype being either png, jpg, gif, etc.)

## Installation
---
>**NOTE**: This has been tested with python 3.5+ and can only be ran on Linux. A Debian based OS is assumed to be used.

### Setup Linux environment
Since pycups is a compiled C program with python bindings, certain development libraries are required to be installed. These programs are listed below. This assumes that a Debian based OS is being used.
- gcc
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

The program is to be stored in **/opt/vertech**. If the directory doesn't exist, create it. Copy current contents to that directory.
```bash
sudo mkdir -p /opt/vertech/cupsAPI
sudo cp -r . /opt/vertech/cupsAPI
cd /opt/vertech/cupsAPI
```

### Setup program environment
**To install just a local dev environment, run the commands below to install dependencies and a local environment**
```bash
make local
```

When installed, program can be ran from the command line:
```bash
python -m cupsAPI {args}
```

Optional arguments:
```
--debug, -d              (Debugging logging enable)
--port PORT, -p    PORT  (Web server port number) (default: 9090)
```

**To install the program as a service, run the commands below to install dependencies and the systemd service file**

```bash
sudo make install
```

## Sending requests
### There are currently 3 endpoints configured.
**Index (/) [GET]**
   - Displays information about the server and version number.

**Config (/config) [POST]**
   - Accepts data in format below to configure printer and server for a single print job. Must be called before the print endpoint can be called. Will be reset after every print job.
```json
    {
        "server": "cups server address",
        "printer": "printer name"
    }
```

**Print (/print) [POST]**
 - Accepts data in format specified in the **Content-Type** header. This sends the posted data to the configured printer.
