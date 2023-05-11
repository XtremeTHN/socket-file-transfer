from modules.client import SocketClientShell, Operations
from modules.netfuncs import getip
def analyze_command(args: list, minimun_args):
    if len(args) - 1 < minimun_args:
        print(f"{args[0]}: No hay argumentos suficientes")
        return False
    else:
        return True

class Shell():
    def __init__(self, default_welcome_msg="Linea de comandos. Para mas informacion escribe help [command]"):
        self.default_welcome_msg = default_welcome_msg
        self.client = None
        
    def start(self):
        print(self.default_welcome_msg)
        while True:
            args = input("> ").split(" ")
            if args[0] == "client":
                if analyze_command(args, 2):
                    if args[1] == "connect":
                        
                        self.client = SocketClientShell(args[2] if args[2] != "localhost" else getip())
                    elif args[1] == "send":
                        self.client.set_data_to_send(args[2])
                        self.client.send()
                    
                    elif args[1] == "close":
                        self.client.set_data_to_send("", operation=Operations.SHUTDOWN)
                        self.client.send()
                        self.client.close()
                    
            elif args[0] == "exit":
                break