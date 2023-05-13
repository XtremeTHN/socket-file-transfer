import socket, sys, os, threading, time, signal
from tqdm import tqdm
from modules.netfuncs import getip

class ResponseTypes:
    FILE = "FILE"
    STRING = "STRING"
    REQUEST = "REQUEST"
    NULL = "NULL"

class Operations:
    SHUTDOWN = "SHUTDOWN"
    CLOSE = "CLOSE"
    SHELL_COMMAND = "SHELL_COMMAND"
    PYTHON_COMMAND = "PYTHON_COMMAND"
    
class SocketServer():
    ACCESS_DENIED = u"ACCESS_DENIED".encode()
    ACCESS_GRANTED = u"ACCESS_GRANTED".encode()
    def __init__(self, allow_shell=False, multi_connections=False):
        self.allow_shell = allow_shell
        self.connect_thread = None
        self.threads = []
        
        self.sock = socket.socket()
        self.sock.bind((getip(), 8080))
        self.running = True
        
        self.sock.listen()
        serv_sock, address = self.sock.accept()
        print(f"IP entrante: {address}")
        if input(f"Aceptas la conexion? (S/N): ") == "N":
            serv_sock.sendall(self.ACCESS_DENIED)
            serv_sock.close()
            self.sock.close()
            return
        serv_sock.sendall(self.ACCESS_GRANTED)
        if multi_connections:
            self.connect_thread = threading.Thread(target=self.init_thread)
        self.get_data_sended(serv_sock, address)

    def get_data_sended(self, serv_sock: socket.socket, address):
        if self.connect_thread:
            if not self.connect_thread.is_alive():
                self.connect_thread.start()
        
        print("Esperando datos de la conexion", address)
        while self.running:
            header = serv_sock.recv(1024).decode().split(",")
            
            if header[0] == ResponseTypes.FILE:
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
                while self.running:
                    chunk = serv_sock.recv(1024)
                    if not chunk:
                        break
                    file.write(chunk)
                    progress_bar.update(len(chunk))
                file.close()
                progress_bar.clear()
                progress_bar.close()
            elif header[0] == ResponseTypes.STRING:
                print(serv_sock.recv(1024).decode())
            elif header[0] == Operations.CLOSE:
                serv_sock.close()
                break
            elif header[0] == Operations.SHUTDOWN:
                if input("Alguien quiere apagar este servidor. Apagar? (S/N): ") != "N" or "n":
                    serv_sock.close()
                    self.running = False
                    self.sock.close()
                    break
                
            elif header[0] == Operations.SHELL_COMMAND:
                if self.allow_shell:
                    print(f"Ejecutando comando {header[1]}...")
                    os.system(header[1])
                else:
                    print("No se permite ejecutar comandos en este servidor")
            elif header[0] == Operations.PYTHON_COMMAND:
                if self.allow_shell:
                    print(f"Executing python command {header[1]}...")
                    try:
                        exec(header[1])
                    except Exception as e:
                        print(f"Error: {e}")
                else:
                    print("No se permite ejecutar comandos en este servidor")

    def grant_connect_permission_thread(self):
        while self.running:
            serv_sock, address = self.sock.accept()
            print(f"IP entrante: {address}")
            if input(f"Aceptas la conexion? (S/N): ") == "N":
                serv_sock.sendall(self.ACCESS_DENIED)
                serv_sock.close()
                return
            serv_sock.sendall(self.ACCESS_GRANTED)
            threading.Thread(target=self.get_data_sended, args=[serv_sock, address]).start()
    
    def cleanup(self):
        self.stop = True
        try:
            self.sock.close()
        except:
            pass
    
    def init_thread(self):
        while self.running:
            time.sleep(1)
            try:
                self.grant_connect_permission_thread()
            except OSError:
                print("Closing threads")
                break