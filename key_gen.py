import os
import subprocess
import platform
# Color
green = "\x1b[32m"
blue = "\x1b[34m"
red = "\x1b[31m"
orange = "\x1b[38;5;220m"
reset = "\x1b[0m"


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
        if not os.path.exists(Key):
            os.mkdir(Key)
            print(f"{orange} [+] {Key} directory created")
        
    #     # Créer les sous-dossiers CA et CERT dans le dossier SSL
            os.mkdir(os.path.join(Key, "CA"))
            os.mkdir(os.path.join(Key, "CERT"))
            print(f"{orange} [+] CA and CERT directories created within {Key}")
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






    
    