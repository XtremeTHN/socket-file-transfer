import requests, socket

def check_wifi():
    try:
        requests.get("https://www.google.com")
        return True
    except:
        return False

def get_ip(client=True):
    # Crear un socket UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            # Intentar conectar a un host externo
            s.connect(('8.8.8.8', 80))
            # Obtener la dirección IP asignada al socket
            ip_address = s.getsockname()[0]
            if client:
                return ip_address[:len(ip_address) - 3]
            else:
                return ip_address[:len(ip_address) - 3], ip_address
        except socket.error:
            # En caso de error, retornar None o manejarlo de acuerdo a tus necesidades
            return None