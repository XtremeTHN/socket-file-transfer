import socket, os, sys
from tqdm import tqdm
from modules.shells.misc import SendTypes, Operations, RecieveTypes

class SocketClient():
    HEADER_TEMPLATE = u"{},{},{}"
    def __init__(self, data: str, address: tuple | list, timeout=10):
        self.result = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Esperando confirmacion...')
        self.sock.connect(address)
        
        response = self.sock.recv(1024).decode()
        if response == "ACCESS_DENIED":
            self.sock.close()
            try:
                self.file.close()
            except:
                pass
            self.result = False
        print("Accesso permitido...")
        self.format_header(data)

        
    def format_header(self, data):
        if os.path.isfile(data):
            self.file = open(data, 'rb')
            self.size = os.path.getsize(data)
            print(self.size, data)
            self.type = SendTypes.FILE
            self.header = self.HEADER_TEMPLATE.format(SendTypes.FILE, os.path.basename(data), self.size).encode()
        elif data == Operations.SHUTDOWN:
            self.type = Operations.SHUTDOWN
            self.data = data
            self.header = self.HEADER_TEMPLATE.format(Operations.SHUTDOWN, SendTypes.NULL, SendTypes.NULL).encode()
        else:
            self.type = SendTypes.STRING
            self.data = data
            self.header = self.HEADER_TEMPLATE.format(SendTypes.STRING, SendTypes.get_string_size(data), SendTypes.NULL).encode()
        
    def run(self):
        print("Sending data...")
        self.sock.sendall(self.header)

        if self.type == SendTypes.FILE:
            if self.sock.recv(1024).decode() == RecieveTypes.ACCESS_GRANTED:
                progress_bar = tqdm(total=self.size, unit='B', unit_scale=True)
                while True:
                    chunk = self.file.read(1024)
                    if not chunk:
                        break
                    progress_bar.update(len(chunk))
                    self.sock.sendall(chunk)
                progress_bar.close()
            else:
                print("Se denego la operacion")
        elif self.type == Operations.SHUTDOWN:
            self.sock.sendall(SendTypes.NULL.encode())
        elif self.type == SendTypes.STRING or Operations.PYTHON_COMMAND or Operations.SHELL_COMMAND:
            self.sock.sendall(self.data.encode())

class SocketClientShell():
    HEADER_TEMPLATE = u"{},{},{}"
    def __init__(self, address, timeout=10):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Esperando confirmacion...')
        self.sock.settimeout(timeout)
        self.sock.connect((address, 8080))
        
        self.sock.sendall(SendTypes.REQUEST.encode())
        response = self.sock.recv(1024).decode()
        if response == "ACCESS_DENIED":
            self.sock.close()
            try:
                self.file.close()
            except:
                pass
            print("Se denego el acceso")
            sys.exit(14)
        self.serv_info = self.sock.recv(1024).decode()
    
    def close(self):
        self.sock.close()
    
    def set_data_to_send(self, data: str, operation=None):
        if os.path.isfile(data):
            self.file = open(data, 'rb')
            self.size = os.path.getsize(data)
            self.type = SendTypes.FILE
            self.header = self.HEADER_TEMPLATE.format(SendTypes.FILE, os.path.basename(data), self.size).encode()
        elif operation == Operations.SHUTDOWN:
            self.header = self.HEADER_TEMPLATE.format(Operations.SHUTDOWN, SendTypes.NULL, SendTypes.NULL).encode()
            self.data = data
            self.type = Operations.SHUTDOWN
        else:
            self.type = SendTypes.STRING
            self.data = data
            self.header = self.HEADER_TEMPLATE.format(SendTypes.STRING, SendTypes.get_string_size(data), SendTypes.NULL).encode()
    
    def send(self):
        self.sock.sendall(self.header)
        
        if self.type == SendTypes.FILE:
            progress_bar = tqdm(total=self.size, unit='B', unit_scale=True)
            while True:
                chunk = self.file.read(1024)
                if not chunk:
                    break
                progress_bar.update(len(chunk))
                self.sock.sendall(chunk)
            progress_bar.close()
        elif self.type == SendTypes.STRING or Operations.PYTHON_COMMAND or Operations.SHELL_COMMAND:
            self.sock.sendall(self.data.encode())
        elif self.type == Operations.CLOSE:
            self.sock.sendall(SendTypes.NULL.encode())
        elif self.type == Operations.SHUTDOWN:
            self.sock.sendall(SendTypes.NULL.encode())
        print("Datos enviados correctamente")