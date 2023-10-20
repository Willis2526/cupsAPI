""" CupsApi module entrypoint """
import argparse
import logging

import uvicorn

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.DEBUG,
    format=(
        "%(asctime)s - %(levelname)-8s - %(name)-20s:%(lineno)5d - "
        "%(message)s"
    ),
)

# Parse the arguments for the options
parser = argparse.ArgumentParser(description="CupsApi")
parser.add_argument(
    "--debug", "-d", action="store_true", help="Debugging enable"
)
parser.add_argument(
    "--port", "-p", default=9095, type=int, help="Web app port number"
)
parser.add_argument(
    "--address", "-a", default="0.0.0.0", type=str, help="Web app address"
)
parser.add_argument(
    "--path", default="cupsapi.app:app", type=str, help="app path"
)
args = parser.parse_args()

reload = False
if args.debug:
    reload = True

# Run the app
uvicorn.run(args.path, host=args.address, port=args.port, reload=reload)