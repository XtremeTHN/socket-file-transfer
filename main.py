import argparse, sys
from modules.client import ClientSocket
from modules.server import ServerSocket
from modules.gen_funcs import generate_certificates

parser = argparse.ArgumentParser("DataTransfer", description="Transfer information with sockets")

parser.add_argument("-c", "--connect", action="store", dest="code", metavar="CODE", help="Provide the code that the host give to you")
parser.add_argument("-s", "--start-server", action="store", default="default", metavar="PASSWORD", dest="start_serv", help="Start the server")

args = parser.parse_args()

if sys.argv == 0:
    parser.print_usage()
    sys.exit(1)

if args.code:
    