""" Reporter Server Main """
import argparse
import logging
import logging.handlers

from .server import Server

logger = logging.getLogger(__name__)
# Parse the arguments for the options
parser = argparse.ArgumentParser(description="Reporter Server")
parser.add_argument(
    "--debug", "-d", action="store_true", help="Debugging enable"
)
parser.add_argument(
    "--port", "-p", default=9090, type=int, help="Web server port number"
)
args = parser.parse_args()

# Setup logging
log_level = logging.INFO
if args.debug:
    log_level = logging.DEBUG

logging.basicConfig(
    level=log_level,
    format=(
        "%(asctime)s - %(levelname)-8s - %(name)-20s:%(lineno)5d - "
        "%(message)s"
    ),
)

server = Server(args.port, args.debug)
server.start()
