from modules.client import SocketClientShell, Operations
from modules.server import SocketServer
from modules.shells.python import PythonInteractiveShell
from modules.netfuncs import getip

import shlex, os, sys

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory


class Shell():
    def __init__(self):
        self.client = None
    def run(self):
        history = FileHistory('.shell_history')  # Historial de comandos guardado en un archivo

        while True:
            user_input = prompt('>>> ', history=history, auto_suggest=AutoSuggestFromHistory())
            args = shlex.split(user_input)
            if args[0] == "client":
                try:
                    if args[1] == "connect":
                        self.client = SocketClientShell(args[2])
                    elif args[1] == "send":
                        self.client.set_data_to_send(args[2])
                        self.client.send()
                    elif args[1] == "execute":
                        if args[2] == "python":
                            py_shell = PythonInteractiveShell(self.client.sock)
                            if args[-1] == "python":
                                py_shell.main_loop()
                            else:
                                if py_shell.eval_code(args[3]):
                                    py_shell.format_header(args[3])
                                    py_shell.send_code(args[3])

                    elif args[1] == "close":
                        self.client.set_data_to_send("", Operations.CLOSE)
                        self.client.send()
                    elif args[1] == "poweroff":
                        self.client.set_data_to_send("", Operations.SHUTDOWN)
                        self.client.send()
                except IndexError:
                    print(f"{args[0]}: No hay argumentos suficientes")
                    continue
                except (ConnectionAbortedError, AttributeError):
                    print(f"{args[0]}: No hay servidores conectados")
                    continue
            elif args[0] == "server":
                try:
                    if args[1] == "start":
                        print(f"{args[0]}: Esperando conexiones en {getip()} puerto 8080")
                        SocketServer(allow_shell=True if "--allow-command-exec" in args else False, multi_connections=True if "--allow-multi-connections" in args else False)
                except IndexError:
                    print(f"{args[0]}: No hay argumentos suficientes")
            elif args[0] == "clear":
                os.system("cls" if sys.platform == "win32" else "clear")
            elif args[0] == "exit":
                break