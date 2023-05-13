import sys, socket, os
from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from pygments.lexers import PythonLexer
class SendTypes:
    FILE = "FILE"
    NULL = "NULL"
    STRING = "STRING"
    REQUEST = "REQUEST"
    
class RecieveTypes:
    OK = "OK"
    ACCESS_DENIED = "ACCESS_DENIED"
    ACCESS_GRANTED = "ACCESS_GRANTED"
    
class Operations:
    SHUTDOWN = "SHUTDOWN"
    CLOSE = "CLOSE"
    SHELL_COMMAND = "SHELL_COMMAND"
    PYTHON_COMMAND = "PYTHON_COMMAND"
    
class PythonInteractiveShell():
    HEADER_TEMPLATE = u"{},{},{}"
    def __init__(self, socket: socket.socket) -> None:
        prompt_style = Style.from_dict({
            'prompt': 'ansiblue bold',
        })
        self.session = PromptSession(
            lexer=PygmentsLexer(PythonLexer),
            style=prompt_style
        )
        self.socket = socket
    
    def main_loop(self):
        while True:
            try:
                code = self.session.prompt('>>> ')
                if code == 'exit':
                    break
                if self.eval_code(code):
                    self.format_header(code)
                    self.send_code(code)
            except KeyboardInterrupt:
                break
            
    def format_header(self, data):
        self.type = Operations.PYTHON_COMMAND
        self.header = self.HEADER_TEMPLATE.format(Operations.PYTHON_COMMAND, data, SendTypes.NULL).encode()
        
    def eval_code(self, code):
        try:
            compile(code, '<string>', 'exec')
            return True
        except SyntaxError as e:
            print(f'Error: {e}')
            return False

    def send_code(self, code):
        self.socket.sendall(self.header)
        