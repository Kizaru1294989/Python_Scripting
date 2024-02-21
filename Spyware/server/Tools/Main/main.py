import ssl
import sys
import os
from Tools.Color import colors
import socket
from Tools.Help.help import display_help
from Tools.Network.network import ip
from Tools.Loop.loop import loop
from Tools.File_Tools.file import print_directory_tree, read_file_in_target


def main(param):
    """Fonction principale du programme."""
    if param == 3:
        print(f"{colors.blue} You need a argument to specify --help for more details")
    if param == 1:
        display_help()
    if param == 4:
        print_directory_tree('Target')
    if param == 5:
        content_file = read_file_in_target(sys.argv[2])
        print(content_file)
    if param == 2:
        port = sys.argv[2]
        host = ip()
        socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_obj.bind((host, int(port)))
        socket_obj.listen(5)
        print("Serveur Up")
        cert_dir = os.path.join(os.getcwd(), "SSL", "CERT")
        cert_file = os.path.join(cert_dir, "cert-server.pem")
        key_file = os.path.join(cert_dir, "cert-key.pem")
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert_file, key_file)
        server_ssl = context.wrap_socket(socket_obj, server_side=True)
        client_ssl, ip_client_side = server_ssl.accept()
        ip_client = ip_client_side[0]
        print(f"Client Connected ! : {ip_client}")
        while True:
            try:
                loop(port,host,client_ssl,ip_client)
            except Exception as e:
                print(f"Error: {e}")
                break
        print("-- END --")
        client_ssl.close()
        server_ssl.close()
        socket_obj.close()