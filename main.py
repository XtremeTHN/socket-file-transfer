import argparse, sys
from modules.client import ClientSocket
from modules.server import ServerSocket
from modules.gen_funcs import generate_certificates

parser = argparse.ArgumentParser("DataTransfer", description="Transfer information with sockets")

parser.add_argument("-c", "--connect", nargs=2, dest="code", metavar="CODE", help="Provide the code that the host give to you")
parser.add_argument("-s", "--start-server", action="store_true", dest="start_serv", help="Start the server")
parser.add_argument("--password", action="store", dest="password", help="Specifies the password")
parser.add_argument("-g", "--generate-certificates", action="store_true", dest="gen_cert", help="Generates the certifications files (only for testing)")

args = parser.parse_args()

if sys.argv == 0:
    parser.print_usage()
    sys.exit(1)

if args.code:
    client = ClientSocket(args.code[0], args.code[1]).connect()
    
if args.start_serv:
    server = ServerSocket().init_server()

if args.gen_cert:
    generate_certificates()