import argparse, sys
from modules.server import SocketServer
from modules.client import SocketClient

parser = argparse.ArgumentParser(prog="transfer", description="Data transferer with sockets")

parser.add_argument("-cs", "--create-server", action="store_true", dest="server_host", help="Host a socket server")
parser.add_argument("-c", "--connect", action="store", dest="host", help="Connect to a server")
parser.add_argument("--file", action="store", dest="file", help="Sends a file to a connected server")
parser.add_argument("--data", action="store", dest="data", help="Sends data to a connected server")
parser.add_argument("-s", "--shell", action="store_true", dest="shell", help="Show a shell for executing commands on the socket server")

args = parser.parse_args()

if args.server_host:
    print(f"Escuchando en {args.server_host} en el puerto 8080")
    try:
        server = SocketServer()
    except ConnectionRefusedError:
        print("No se pudo conectar al servidor")
        sys.exit(1)
        
if args.host:
    if args.file:
        data = args.file
    elif args.data:
        data = args.data

    client = SocketClient(data, (args.host, 8080))
    client.run()
