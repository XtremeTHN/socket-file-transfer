import socket, sys
from tqdm import tqdm

class SocketServer():
    ACCESS_DENIED = u"ACCESS_DENIED".encode()
    ACCESS_GRANTED = u"ACCESS_GRANTED".encode()
    def __init__(self):
        self.sock = socket.socket()
        self.sock.bind(("localhost", 8080))
        
        self.sock.listen()
        serv_sock, address = self.sock.accept()
        print(f"IP entrante: {address}")
        if input(f"Aceptas la conexion? (S/N): ") == "N":
            serv_sock.sendall(self.ACCESS_DENIED)
            serv_sock.close()
            self.sock.close()
            return
        
        print("Recibiendo encabezado...")
        header = serv_sock.recv(1024).decode().split(",")
        if header[0] == "FILE":
            print("Archivo entrante")
            print(f"File name: {header[1]}    File size: {header[2]}")
            if input("Quieres recibirlo? (S/N): ") == "N":
                print("Rechazando...")
                serv_sock.sendall(self.ACCESS_DENIED)
                serv_sock.close()
                file.close()
                sys.exit(1)
            print("Recibiendo...")
            file = open(header[1], "wb")
            serv_sock.sendall(self.ACCESS_GRANTED)
            
            progress_bar = tqdm(total=int(header[2]), unit='B', unit_scale=True)
            while True:
                chunk = serv_sock.recv(1024)
                if not chunk:
                    break
                file.write(chunk)
                progress_bar.update(len(chunk))
            file.close()
        elif header[0] == "STRING":
            print(header[1])