import socket, sys, os, threading, time, logging
from tqdm import tqdm
from modules.netfuncs import getip
from modules.shells.python import ServerPythonUtils
from modules.shells.os_shell import ServerCmdUtils

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
    def __init__(self, log_file_name, allow_shell=False, multi_connections=False):
        self.logger  = logging.getLogger("Server")
        self.allow_shell = allow_shell
        self.connect_thread = None
        self.connections = 0
        self.max_connections = 10
        self.ignore_exceptions = True
        self.log_file_name = log_file_name
        
        ip = getip()
        self.logger.info(f"Creating server in the address {ip}")
        with socket.socket() as self.sock:
            self.sock.bind((ip, 8080))
            self.running = True
            
            self.logger.info("Listening for connections...")
            self.sock.listen()
            serv_sock, address = self.sock.accept()
            self.logger.info(f"Device connected {address}")
            print(f"IP entrante: {address}")
            if input(f"Aceptas la conexion? (S/N): ") == "N":
                serv_sock.sendall(self.ACCESS_DENIED)
                serv_sock.close()
                self.sock.close()
                return
            serv_sock.sendall(self.ACCESS_GRANTED)
            if multi_connections:
                self.logger.info("Creating connection scanner thread...")
                self.connect_thread = threading.Thread(target=self.init_thread)
                self.threads = 0
            self.main_server_loop(serv_sock, address)

    def main_server_loop(self, serv_sock: socket.socket, address):
        if self.connect_thread:
            if not self.connect_thread.is_alive():
                self.threads += 1
                self.logger.info(f"Starting thread {self.threads}")
                self.connect_thread.start()
        
        print("Esperando datos de la conexion", address)
        serv_sock.sendall(sys.platform.encode())
        while self.running:
            try:
                header = serv_sock.recv(1024).decode().split(",")
                
                if header[0] == ResponseTypes.FILE:
                    self.handle_file_header(serv_sock, header)
                    
                elif header[0] == ResponseTypes.STRING:
                    self.logger.info("String header recieved")
                    self.handle_string_header(serv_sock, header)
                elif header[0] == Operations.CLOSE:
                    self.logger.info("Close header recieved, closing this connection...")
                    serv_sock.close()
                    break
                elif header[0] == Operations.SHUTDOWN:
                    self.logger.info("Shutdown header recieved")
                    if input("Alguien quiere apagar este servidor. Apagar? (S/N): ") != "N" or "n":
                        self.logger.info("Closing...")
                        serv_sock.close()
                        self.cleanup()
                        break
                    
                elif header[0] == Operations.SHELL_COMMAND:
                    self.logger.info("Shell command header recieved")
                    self.logger.info("Sending os information")
                    if self.allow_shell:
                        self.logger.debug(f"Executing command with length of {header[1]}")
                        ServerCmdUtils.exec_cmd(serv_sock, header[1])
                    else:
                        self.logger.warning("Commands are not allowed in this server")
                        print("No se permite ejecutar comandos en este servidor")
                        
                elif header[0] == Operations.PYTHON_COMMAND:
                    if self.allow_shell:
                        self.logger.debug(f"Executing command with length of {header[1]}")
                        ServerPythonUtils.exec_cmd(serv_sock, header[1])
                    else:
                        self.logger.warning("Commands are not allowed in this server")
                        print("No se permite ejecutar comandos en este servidor")
            except Exception as e:
                print(f"Error: {e}")
                if self.ignore_exceptions:
                    self.logger.exception("Current exception:", exc_info=True)
                    print("This exception will be ignored, but maybe will provocate another errors")
                    print(f"Note: The exception traceback will be in the current log file {self.log_file_name}")
                else:
                    print("Closing server...")
                    self.cleanup()

    def handle_file_header(self, serv_sock: socket.socket, header: list):
        self.logger.info("Received file header!")
        print("Archivo entrante")
        print(f"File name: {header[1]}    File size: {header[2]}")
        if input("Quieres recibirlo? (S/N): ") == "N":
            print("Rechazando...")
            serv_sock.sendall(self.ACCESS_DENIED)

        print("Recibiendo...")
        file = open(header[1], "wb")
        serv_sock.sendall(self.ACCESS_GRANTED)
                    
        progress_bar = tqdm(total=int(header[2]), unit='B', unit_scale=True)
        self.logger.info("Recieving file data...")
        while self.running:
            chunk = serv_sock.recv(1024)
            if not chunk:
                break
            file.write(chunk)
            progress_bar.update(len(chunk))
        file.close()
        progress_bar.clear()
        progress_bar.close()
        self.logger.info("Done!")
    
    def handle_string_header(self, serv_sock: socket.socket, header: list):
        print(serv_sock.recv(int(header[1])).decode())
    
    
    def grant_connect_permission_thread(self):
        while self.running:
            if self.connections >= self.max_connections:
                print("Ya no se permiten mas conexiones en este servidor")
                return
            self.sock.listen()
            serv_sock, address = self.sock.accept()
            print(f"IP entrante: {address}")
            if input(f"Aceptas la conexion? (S/N): ") == "N":
                serv_sock.sendall(self.ACCESS_DENIED)
                serv_sock.close()
                return
            serv_sock.sendall(self.ACCESS_GRANTED)
            print("Thread")
            threading.Thread(target=self.main_server_loop, args=[serv_sock, address]).start()
            self.connections += 1
            
    def cleanup(self):
        self.running = False
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