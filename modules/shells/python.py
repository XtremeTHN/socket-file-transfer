import sys, socket, os
from modules.shells.misc import BaseShellClass, Operations
from pygments.lexers import PythonLexer

class PythonExecutor(BaseShellClass):
    def __init__(self, socket: socket.socket) -> None:
        super().__init__(socket, PythonLexer)
    
    def main_loop(self):
        while True:
            try:
                code = self.session.prompt('>>> ')
                if code == 'exit':
                    break
                if self.eval_code(code):
                    self.format_header(code, Operations.PYTHON_COMMAND)
                    self.send_code()
            except KeyboardInterrupt:
                break
    
class ServerPythonUtils:
    def exec_cmd(serv_sock, buffer):
        cmd = serv_sock.recv(int(buffer)).decode()
        print(f"Executing python command {cmd}...")
        try:
            exec(cmd)
        except Exception as e:
            print(f"Error: {e}")