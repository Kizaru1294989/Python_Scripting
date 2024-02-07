import socket
import ssl
import os

def main():
    # Load the CA CERT
    print('main active')
    ca_cert_path = os.path.join(os.getcwd(), "SSL", "CA", "ca-cert.pem")
    print(ca_cert_path)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(cafile=ca_cert_path)

    # Setting
    host = str(input("Server IP : "))
    port = 10500
    socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Secure the socket
    client_ssl = context.wrap_socket(socket_obj, server_hostname=host)
    client_ssl.connect((host, port))

    while True:
        try:
            # Get message
            msg = client_ssl.recv(1024).decode()
            print(f"Server : {msg}")

            # Send message
            msg = str(input("Client : ")).encode()
            client_ssl.send(msg)
        except Exception as e:
            print(f"Error: {e}")
            break

    print("-- END --")
    client_ssl.close()

if __name__ == "__main__":
    main()
