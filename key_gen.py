import os
import subprocess
import platform
import socket
# Color
green = "\x1b[32m"
blue = "\x1b[34m"
red = "\x1b[31m"
orange = "\x1b[38;5;220m"



Key = "SSL"


def check_OpenSSL(os):
    if os == "Linux":
        try:
            output = os.popen('openssl version').read()
            if output.split(' ')[0] in ["LibreSSL", "OpenSSL"]:
                    print(" [+] OpenSSL is installed")
                    return True
            else:
                    print(f"{red} [-] Error SSL\n     Try 'sudo apt install openssl'")
                    exit(0)
        except Exception as e:
                print(f"{red} [-] Error SSL\n     {e}\n     Try 'sudo apt install openssl'")
                exit(0)

    try:
        result = subprocess.run(['openssl', 'version'], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            output = result.stdout.strip()
            print(output)
            if output.split(' ')[0] in ["LibreSSL", "OpenSSL"]:
                print(" [+] OpenSSL is installed")
                return True
            else:
                exit(0)
        else:
            exit(0)
    except Exception as e:
        print(f" [-] Error: {e}")
        exit(0)



def check_platform():
    return platform.system()



def key_generation():
    openssl_config_path = r'C:\xampp\apache\conf\openssl.cnf' # remplacer avec le path de ca config openssl 
    if not os.path.exists(Key):
        os.mkdir(Key)
        print(f"{orange} [+] {Key} directory created")

        # Créer les sous-dossiers CA et CERT dans le dossier SSL
        os.mkdir(os.path.join(Key, "CA"))
        os.mkdir(os.path.join(Key, "CERT"))
        print(f"{orange} [+] CA and CERT directories created in {Key}")

        # Génération de la clé privée du CA
        try:
            #openssl genrsa -aes256 -out ca-key.pem 4096
            subprocess.run(['openssl', 'genrsa', '-aes256', '-out', f'{Key}/CA/ca-key.pem', '4096'], check=True)
            print(f"{orange} [+] CA private key generated")
        except subprocess.CalledProcessError as e:
            print(f"{orange} [-] Error generating CA private key: {e}")

        # Génération du certificat public CA
        try:
            subprocess.run(['openssl', 'req', '-new', '-x509', '-sha256', '-days', '365', '-key', f'{Key}/CA/ca-key.pem', '-out', f'{Key}/CA/ca-cert.pem', '-config', openssl_config_path], check=True)
            print(f"{orange} [+] CA certificate generated")
        except subprocess.CalledProcessError as e:
            print(f"{orange} [-] Error generating CA certificate: {e}")

        # Génération de la clé privée du serveur
            


            ################ CERT
        try:
            subprocess.run(['openssl', 'genrsa', '-out', f'{Key}/CERT/cert-key.pem', '4096'], check=True)
            print(f"{orange} [+] Server private key generated")
        except subprocess.CalledProcessError as e:
            print(f"{orange} [-] Error generating server private key: {e}")

        # Génération de la demande de certificat
            

            #openssl req -new -sha256 -subj "/CN=<CN NAME>" -key cert-key.pem -out cert-query.csr
        try:
            subprocess.run(['openssl', 'req', '-new', '-sha256', '-subj' ,'/CN=<CN NAME>' ,  '-key', f'{Key}/CERT/cert-key.pem', '-out', f'{Key}/CERT/cert-query.csr' , '-config', openssl_config_path], check=True)
            print(f"{orange} [+] Certificate request generated")
        except subprocess.CalledProcessError as e:
            print(f"{orange} [-] Error generating certificate request: {e}")

        # Génération de extfile.cnf
        try:
            with open(f'{Key}/CERT/extfile.cnf.txt', 'w') as f:
                hostname=socket.gethostname()
                ip=socket.gethostbyname(hostname)
                print(ip)
                f.write(f'subjectAltName=IP:{ip}\n')
            print(f"{orange} [+] extfile.cnf.txt generated")
        except Exception as e:
            print(f"{orange} [-] Error generating extfile.cnf.txt: {e}")

        try:
            subprocess.run(['openssl', 'x509', '-req', '-sha256', '-days', '365', '-in', f'{Key}/CERT/cert-query.csr', '-CA', f'{Key}/CA/ca-cert.pem', '-CAkey', f'{Key}/CA/ca-key.pem', '-out', f'{Key}/CERT/cert-server.pem', '-extfile', f'{Key}/CERT/extfile.cnf.txt','-CAcreateserial'], check=True)
            print(f"{orange} [+] Certificate signed by CA")
        except subprocess.CalledProcessError as e:
            print(f"{orange} [-] Error signing certificate by CA: {e}")
    else:
        print(f"{orange} [+] {Key} directory already exists")

def os_check():
    current_platform = check_platform()
    if current_platform == 'Windows':
        return 'Windows'
    elif current_platform == 'Linux':
        return 'Linux'
    else:
        return None

def init():
    os_local = os_check()
    print(os_local)
    check_OpenSSL(os_local)
    if check_OpenSSL :
        key_generation()
         
         
    # if os_local is None:
    #     print(f"{red} [+] OS not recognized")
    #     return
    


if __name__ == '__main__':
    init()






    
    