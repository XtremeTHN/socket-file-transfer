import ssl, socket
from modules.netfuncs import get_ip
from modules.gen_funcs import generate_password
class ClientSocket():
    def __init__(self, code, password=None):
        self.host = get_ip() + code
        self.password = password
    
    def connect(self):
        
        PORT = 8855

        # Definir la contraseña para la conexión segura
        if self.password == None:
            self.password = generate_password()

        # Crear un objeto socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # Conectarse al servidor
            client_socket.connect((self.host, PORT))

            # Configurar el contexto SSL
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            # Establecer una conexión segura
            secure_socket = context.wrap_socket(client_socket, server_hostname=self.host)

            # Enviar la contraseña al servidor
            secure_socket.sendall(str(self.password).encode())

            # Recibir la respuesta del servidor
            response = secure_socket.recv(1024).decode()
            print('Respuesta del servidor:', response)

            # Cerrar la conexión segura
            secure_socket.close()