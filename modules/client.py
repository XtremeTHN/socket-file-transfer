import ssl, socket, sys, os, json
from modules.netfuncs import get_ip
from modules.gen_funcs import generate_password
class ClientSocket():
    def __init__(self, host, password):
        self.host = host
        self.socket = None
        self.password = password
    
    def connect(self):
        PORT = 8855

       # Crear un objeto socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Crear un contexto SSL
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

        # Establecer verificación del certificado (opcional)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        # Establecer ubicación del archivo de certificado (opcional)
        #context.load_cert_chain("certificates/client_certificate.pem", "certificates/client_key.pem")
        context.load_verify_locations('certificates/client_certificate.pem')

        # Conectar al servidor utilizando SSL
        with context.wrap_socket(client_socket, server_hostname=self.host) as ssl_socket:
            try:
                # Conectar al servidor
                ssl_socket.connect((self.host, PORT))

                # Realizar operaciones de envío y recepción de datos utilizando ssl_socket

                # Ejemplo: Enviar datos al servidor
                message = str(self.password).encode()
                ssl_socket.sendall(message)

                # Ejemplo: Recibir datos del servidor
                data = ssl_socket.recv(1024)
                if data.decode() == "ACCESS_DENIED":
                    print("El servidor ha rechazado la conexion")
                    ssl_socket.close()
                    sys.exit(45)
                else:
                    self.socket = ssl_socket
                    self.socket.sendall(u"NULL".encode())

            except ssl.SSLError as e:
                print('Error SSL:', e)
                ssl_socket.close()
                sys.exit(143)
                
    def _send(self, data, header="string"):
        info_to_send = json.dumps({"type":header, "data":data}).encode()
        print(info_to_send)
        self.socket.sendall(u"asd".encode())
    
    def send_string(self, msg: str):
        if self.socket == None:
            print("Socket Error: No te has conectado a un servidor")
            sys.exit(46)
        if not isinstance(msg, str):
            print("Socket Error: El mensaje no es una cadena de caracteres que se pueda codificar")
            sys.exit(47)
            
        self.socket.sendall(u"NULL".encode())
        self._send(msg)
    
    def send_file(self, upload_file):
        if not os.path.isfile(upload_file):
            print("El archivo no existe o no es un archivo")
        with open(upload_file, "rb") as file:
            self._send([os.path.basename(upload_file), file.read()], header="file")