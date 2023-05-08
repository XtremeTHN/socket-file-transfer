import socket, ssl
from modules.netfuncs import get_ip
from modules.gen_funcs import generate_password

class ServerSocket():
    def __init__(self):
        pass
    def init_server(password=None):
        CODE, HOST = get_ip(client=False)
        PASSWORD = password if password else generate_password()
        PORT = 8855

        # Crear un objeto socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            # Vincular el socket a la dirección y puerto especificados
            server_socket.bind((HOST, PORT))

            # Configurar el contexto SSL
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            try:
                context.load_cert_chain(certfile="certificates/server.crt", keyfile="certificates/server.key")  # Archivos de certificado y clave del servidor
            except:
                print()
            # Esperar conexiones entrantes
            server_socket.listen()

            print("Servidor creado con exito!")
            print(f"Codigo: {CODE}  Clave: {PASSWORD}")

            # Aceptar la conexión entrante y establecer una conexión segura
            client_socket, address = server_socket.accept()
            secure_socket = context.wrap_socket(client_socket, server_side=True)

            # Recibir la contraseña del cliente
            serv_password = secure_socket.recv(1024).decode()

            # Verificar la contraseña
            if serv_password == password:
                # Enviar una respuesta al cliente
                response = 'Contraseña correcta. Hola cliente seguro!'
                secure_socket.sendall(response.encode())
            else:
                # Enviar una respuesta al cliente
                response = 'Contraseña incorrecta. Conexión cerrada.'
                secure_socket.sendall(response.encode())

            # Cerrar la conexión segura
            secure_socket.close()
