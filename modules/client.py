import socket, os
from tqdm import tqdm

class SocketClient():
    HEADER_TEMPLATE = u"{},{},{}"
    def __init__(self, data: str, address: tuple | list):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Esperando confirmacion...')
        self.sock.connect(("localhost", 8080))
        
        if os.path.isfile(data):
            self.file = open(data, 'rb')
            self.size = os.path.getsize(data)
            self.type = "FILE"
            self.header = self.HEADER_TEMPLATE.format("FILE", os.path.basename(data), self.size).encode()
        else:
            self.type = "STRING"
            self.header = self.HEADER_TEMPLATE.format("STRING", str(data), "NULL").encode()
        
        
    def run(self):
        self.sock.sendall(self.header)
        response = self.sock.recv(1024).decode()

        if response == "ACCESS_DENIED":
            self.sock.close()
            try:
                self.file.close()
            except:
                pass
            return False
        
        if self.type == "FILE":
            progress_bar = tqdm(total=self.size, unit='B', unit_scale=True)
            while True:
                chunk = self.file.read(1024)
                if not chunk:
                    break
                progress_bar.update(len(chunk))
                self.sock.sendall(chunk)
            progress_bar.close()
        print("Datos enviados correctamente")