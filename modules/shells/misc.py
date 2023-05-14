from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style

class SendTypes:
    FILE = "FILE"
    NULL = "NULL"
    STRING = "STRING"
    REQUEST = "REQUEST"

    def get_string_size(string):
        return len(string)
    
class RecieveTypes:
    OK = "OK"
    ACCESS_DENIED = "ACCESS_DENIED"
    ACCESS_GRANTED = "ACCESS_GRANTED"
    
class Operations:
    SHUTDOWN = "SHUTDOWN"
    CLOSE = "CLOSE"
    SHELL_COMMAND = "SHELL_COMMAND"
    PYTHON_COMMAND = "PYTHON_COMMAND"
    
class BaseShellClass():
    HEADER_TEMPLATE = u"{},{},{}"
    def __init__(self, socket, lexer, style={'prompt': 'ansiblue bold',}):
        prompt_style = Style.from_dict(style)
        self.session = PromptSession(
            lexer=PygmentsLexer(lexer),
            style=prompt_style
        )
        self.socket = socket
    
    def format_header(self, data: str, operation: Operations):
        self.type = operation
        self.data = data.encode()
        self.header = self.HEADER_TEMPLATE.format(operation, SendTypes.get_string_size(data.encode()), SendTypes.NULL).encode()
        
    def eval_code(self, code):
        try:
            compile(code, '<string>', 'exec')
            return True
        except SyntaxError as e:
            print(f'Error: {e}')
            return False

    def send_code(self):
        self.socket.sendall(self.header)
        self.socket.sendall(self.data)
    