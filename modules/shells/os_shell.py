import sys, socket, os, subprocess

from modules.shells.misc import BaseShellClass, Operations, SendTypes
    
class CmdExecutor(BaseShellClass):
    HEADER_TEMPLATE = u"{},{},{}"
    def __init__(self, socket: socket.socket, platform: str) -> None:
        
        if platform == "win32":
            self.WELCOME_MSG = "Windows Powershell cmds executer, you can execute a command in the server and get the output!"
            self.DEFAULT_SHELL = ["powershell", "-NonInteractive"]
            from pygments.lexers.shell import PowerShellLexer as ShellLexer
        else:
            self.WELCOME_MSG = "Unix shell commands executer, you can execute a unix command in the server and get the output!"
            from pygments.lexers.shell import BashLexer as ShellLexer
        super().__init__(socket, ShellLexer)
    
    def main_loop(self):
        print(self.WELCOME_MSG)
        while True:
            cmd = self.session.prompt("Posh > ")
            if cmd == "exit":
                break
            
            print(self.exec_cmd(cmd).decode())
    def exec_cmd(self, cmd) -> bytes:
        self.format_header(cmd, Operations.SHELL_COMMAND)
        self.send_code()
        buffer_size = self.socket.recv(4096)
        output = self.socket.recv(int(buffer_size))
        return output
        
class ServerCmdUtils:
    def exec_cmd(serv_sock: socket.socket, buffer: str | int):
        cmd = serv_sock.recv(int(buffer)).decode()
        if sys.platform == "win32":
            DEFAULT_SHELL = ["powershell", "-NonInteractive"]
        else:
            DEFAULT_SHELL = []
        DEFAULT_SHELL.append(cmd)
        output = subprocess.Popen(DEFAULT_SHELL, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = output.communicate()
        print(stdout.decode())
        serv_sock.sendall(str(SendTypes.get_string_size(stdout)).encode())
        serv_sock.sendall(stdout)
        