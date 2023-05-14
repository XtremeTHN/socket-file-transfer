import argparse, sys, os, logging
from modules.server import SocketServer
from modules.client import SocketClient, Operations
from modules.exception_handler import ExceptionHandler
from modules.misc import init_log
from modules.netfuncs import getip
from modules.json_extra import Json
from modules.shells.shell import Shell

parser = argparse.ArgumentParser(prog="transfer", description="Data transferer with sockets", epilog="If you want to executea command in the server, you need to use the shell incorporated in this program")

serv_parser = parser.add_argument_group("Server side args")
serv_parser.add_argument("-cs", "--create-server", action="store_true", dest="server_host", help="Host a socket server")
serv_parser.add_argument("--allow-shell", action="store_true", dest="allow_shell", help="Allows python code execution in the server")
serv_parser.add_argument("--allow-multi-connection", action="store_true", dest="allow_multi", help="Allows multiple connections in the server")
client_parser = parser.add_argument_group("Client side args")
client_parser.add_argument("-c", "--connect", action="store", dest="host", help="Connect to a server")
client_parser.add_argument("--file", action="store", dest="file", help="Sends a file to a connected server")
client_parser.add_argument("--data", action="store", dest="data", help="Sends data to a connected server")
client_parser.add_argument("--shutdown", action="store_true", dest="poweroff", help="Power's of the server")
client_parser.add_argument("-s", "--shell", action="store_true", dest="shell", help="Show a shell for executing commands on the socket server")

args = parser.parse_args()
exc_h = ExceptionHandler()
#sys.excepthook = exc_h.global_handler
logger = logging.getLogger("Transfer")

conf_obj = Json("configs/preferences.json", {'timeout':10, 'max_logs':10, 'activated_by_default':{'allow_shell':False, 'allow_multi_connections':True}}, indent=4)
config = conf_obj.get()
log_file_name = init_log("SocketFileTransfer", config['max_logs'])

if args.server_host:
    print(f"Esperando conexiones en {getip()} en el puerto 8080")
    try:
        logger.info("Starting server...")
        perms = [config['activated_by_default']['allow_shell'], config['activated_by_default']['allow_multi_connections']]
        if args.allow_shell:
            perms[0] = args.allow_shell
        if args.allow_multi:
            perms[1] = args.allow_multi
            
        server = SocketServer(log_file_name, allow_shell=perms[0], multi_connections=perms[1])
    except ConnectionRefusedError:
        print("No se pudo conectar al servidor")
        sys.exit(1)
        
if args.host:
    if args.file:
        data = args.file
    elif args.data:
        data = args.data
    elif args.poweroff:
        data = Operations.SHUTDOWN
    else:
        print("Especifica los datos que quieras enviar al servidor")
        sys.exit(5)
    logger.info(f"Sending data {data}")
    client = SocketClient(data, (args.host if not args.host == "localhost" else getip(), 8080), timeout=config['timeout'])
    if client.result:
        client.run()
    else:
        print("Acceso denegado al servidor")

if args.shell:
    logger.info("Starting shell...")
    Shell().run()