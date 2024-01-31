import ipaddress
import argparse
from TP1 import check_platform
from TP1 import init
import socket
import struct
from ping3 import ping, verbose_ping
from Tools.mask import mask_cidr
import sys
from Tools.argument import display_argument_help

def netdiscover(masque):
    nombre_ip_disponibles = 2 ** (32 - masque) - 2
    #print(nombre_ip_disponibles)
    return nombre_ip_disponibles

def getAllIp(ip_address,range_ip):
    network_address = socket.inet_ntoa(struct.pack('>I', struct.unpack('>I', socket.inet_aton(ip_address))[0] & struct.unpack('>I', socket.inet_aton("255.255.255.0"))[0]))
    all_ips = [socket.inet_ntoa(struct.pack('>I', struct.unpack('>I', socket.inet_aton(network_address))[0] + i)) for i in range(1, int(range_ip))]
    print(f'{int(range_ip)} IP available')
    #print(all_ips)
    return all_ips



def scan_with_socket(host,port_list):
    debut_port = 1
    fin_port = 1024  # Vous pouvez ajuster cette valeur en fonction de vos besoins

    for port in range(debut_port, fin_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Définir le timeout pour la connexion
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"Port {port} : Ouvert")
        else:
            print(f"Port {port} : Fermé")
        sock.close()
    
   # saveResult('./online_ip.txt',result)
    
def ping_host(host):
    result = []
    r = ping(host, timeout=1)

    if r is not None:
        print(f"Ping to {host} successful. Round-trip time: {r} ms")
        if r != False:
            return host
        #result.append(host)
    else:
        print(f"Ping to {host} failed.")
    
   # saveResult('./online_ip.txt',result)

def saveResult(path, result):
    """
    Stocke le contenu de la variable result dans le fichier présent dans la variable path
    """
    with open(path, 'w') as file:
        file.write(result)
    
    print(f"ip online save at {path}")

def chooseInterface(ipList):
    for ip in ipList:
        print(ip)

    user_input = input("Enter the number off the card selected : ")
    choice = int(user_input)
    print("Network interface selected :")
    result = ipList[choice - 1]
    print(result)
    return result   


def main(param):
    result = []
    ipList = init()
    if param == 1:
        ipBlock = chooseInterface(ipList)
        ip_on_the_network = netdiscover(int(ipBlock["Subnet Mask"]))
        listIp = getAllIp(ipBlock["IP Address"],ip_on_the_network)
        for ip in listIp:
            online_ip = ping_host(ip)
            if online_ip is not None:
                result.append(online_ip)
        saveResult("./online_ip.txt",str(result))
    if param == 2:
        ipBlock = chooseInterface(ipList)
        ip_on_the_network = netdiscover(int(ipBlock["Subnet Mask"]))
        listIp = getAllIp(ipBlock["IP Address"],ip_on_the_network)
        for ip in listIp:
            online_ip = scan_with_socket(ip)
            if online_ip is not None:
                result.append(online_ip)
        saveResult("./online_ip.txt",str(result))
    else :
        display_argument_help()
     

if __name__ == "__main__":
    param = None
    if len(sys.argv) > 1 and sys.argv[1] == '-p':
        param = 1
    if len(sys.argv) > 1 and sys.argv[1] == '-s':
        param = 2
    if len(sys.argv) > 1 and sys.argv[1] == '-o':
        param = 3
        
    main(param)
    

