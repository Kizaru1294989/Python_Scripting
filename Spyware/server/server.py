import socket
import ssl
import os

#Setting
def ip():
    hostname = socket.gethostname()
    your_ip = socket.gethostbyname(hostname)
    print("Server local IP :", your_ip)
    return str(your_ip)

host = ip()
port = 10500
socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Start Server
socket_obj.bind((host, port))
socket_obj.listen(5)
print("Serveur Up")

# Load the Server Certificate and his private key
cert_dir = os.path.join(os.getcwd(), "SSL", "CERT")
cert_file = os.path.join(cert_dir, "cert-server.pem")
key_file = os.path.join(cert_dir, "cert-key.pem")

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(cert_file, key_file)

# Secure Server by ssl
server_ssl = context.wrap_socket(socket_obj, server_side=True)

# Accept Connection
client_ssl, _ip = server_ssl.accept()
print(f"Client ip : {_ip}")

while True:
    try:
        # Send message
        msg = str(input("Server : ")).encode()
        client_ssl.send(msg)

        # Get message
        msg = client_ssl.recv(1024).decode()
        print(f"Client : {msg}")
    except Exception as e:
        print(f"Error: {e}")
        break

print("-- END --")
client_ssl.close()
server_ssl.close()
socket_obj.close()
