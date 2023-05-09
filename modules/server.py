import socket, ssl, json, time
from modules.netfuncs import get_ip
from modules.gen_funcs import generate_password
from progress.bar import Bar

class ServerSocket():
    def __init__(self):
        pass
    def init_server(self, password=None):
        HOST = get_ip()
        if password == None:
            PASSWORD = generate_password()
        else:
            PASSWORD = password
        PORT = 8855
        ACCESS_GRANTED = u"ACCESS_GRANTED".encode()
        ACCESS_DENIED = u"ACCESS_DENIED".encode()

        # Crear un objeto socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            # Vincular el socket a la dirección y puerto especificados
            server_socket.bind((HOST, PORT))

            # Configurar el contexto SSL
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            try:
                context.load_cert_chain(certfile="certificates/server_certificate.pem", keyfile="certificates/server_key.pem")  # Archivos de certificado y clave del servidor
            except:
                print()
            # Esperar conexiones entrantes
            server_socket.listen()

            print("Servidor creado con exito!")
            print(f"Host: {HOST}   Clave: {PASSWORD}")

            # Aceptar la conexión entrante y establecer una conexión segura
            while True:
                client_socket, address = server_socket.accept()
                secure_socket = context.wrap_socket(client_socket, server_side=True)

                # Recibir la contraseña del cliente
                serv_password = secure_socket.recv(1024).decode()

                # Verificar la contraseña
                if str(serv_password) == str(PASSWORD):
                    # Enviar una respuesta al cliente
                    secure_socket.sendall(ACCESS_GRANTED)
                    break
                else:
                    # Enviar una respuesta al cliente
                    print(type(serv_password), type(PASSWORD), serv_password, PASSWORD, serv_password == PASSWORD)
                    secure_socket.sendall(ACCESS_DENIED)
                    print("Una maquina intento conectarse con una contrasena incorrecta")
                    continue

            # Cerrar la conexión segura
            self.socket = secure_socket
    
    def loop(self):
        while True:
            BUFFER_SIZE = 4096
            print("Recibiendo datos...")
            data_sended = self.socket.recv(BUFFER_SIZE).decode()
            if data_sended == "NULL" or "":
                time.sleep(2)
                continue
            
            data_sended = json.loads(data_sended)
            
            if data_sended['type'] == 'string':
                print(data_sended['data'])
            elif data_sended['type'] == 'file':
                progress = Bar("Recibiendo archivo", max=int(self.socket.recv(BUFFER_SIZE).decode()))
                with open(data_sended["data"][0], 'wb') as file:
                    while True:
                        chunk = self.socket.recv(BUFFER_SIZE)
                        if not chunk:
                            break
                        file.write(chunk)
                        progress.next(n=len(chunk))