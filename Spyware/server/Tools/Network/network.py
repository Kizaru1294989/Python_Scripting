import socket

def ip():
    """Récupère l'adresse IP locale du serveur."""
    hostname = socket.gethostname()
    your_ip = socket.gethostbyname(hostname)
    print("Server local IP :", your_ip)
    return str(your_ip)