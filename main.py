import argparse, sys
from modules.client import ClientSocket
from modules.server import ServerSocket
from modules.gen_funcs import generate_self_signed_cert

parser = argparse.ArgumentParser("DataTransfer", description="Transfer information with sockets")

parser.add_argument("-c", "--connect", action="store", metavar="HOST", dest="host", help="Connect to a ip, you need to provide the server password with the --password argument")
parser.add_argument("-p", "--password", action="store", metavar="PASSWORD", dest="code")
parser.add_argument("--shell", action="store_true", dest="shell", help="Show a shell for executing commands")
parser.add_argument("--send", action="store", dest="send_info", help="Send information to the connected host")
parser.add_argument("-cs", "--create-server", action="store_true", dest="server", help="Start to host a socket server, you can define a password by providing --password argument")
parser.add_argument("-gc", "--generate-certifications", action="store_true", dest="gen_certs", help="Generate certifications for secure conections (SSL/TLS) (This certs files are not recommended)")
parser.add_argument("--kill-daemon", action="store_true", dest="thread", help="Kills the daemon thread")

args = parser.parse_args()

if sys.argv == 0:
    parser.print_usage()
    sys.exit(1)

if args.host:
    if not args.code:
        print("You need to define the password to connect to the server")
        sys.exit(2)
    client = ClientSocket(args.host, args.code)
    client.connect()
    client.send_string("Hola")

if args.server:
    server = ServerSocket()

    server.init_server(password=args.code)
    server.loop()

if args.gen_certs:
    generate_self_signed_cert('certificates/client_certificate.pem', 'certificates/client_key.pem')
    generate_self_signed_cert('certificates/server_certificate.pem', 'certificates/server_key.pem')