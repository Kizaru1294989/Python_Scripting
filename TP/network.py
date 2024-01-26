import ipaddress
import argparse
from TP import check_platform
from TP import init
import socket
import struct


def getAllIp(ip_address):
    # Obtenir l'adresse IP du réseau
    network_address = socket.inet_ntoa(struct.pack('>I', struct.unpack('>I', socket.inet_aton(ip_address))[0] & struct.unpack('>I', socket.inet_aton("255.255.255.0"))[0]))

    # Générer toutes les adresses IP du réseau
    all_ips = [socket.inet_ntoa(struct.pack('>I', struct.unpack('>I', socket.inet_aton(network_address))[0] + i)) for i in range(1, 255)]
    print(all_ips)
    return all_ips


    
def ping(ip):
    """
    Retourne si l'ip est disponible et répond aux pings.
    """

def saveResult(path, result):
    """
    Stocke le contenu de la variable result dans le fichier présent dans la variable path
    """

def chooseInterface(ipList):
    for ip in ipList:
        print(ip)

    user_input = input("Enter the number off the card selected : ")
    choice = int(user_input)
    print("Network interface selected :")
    result = ipList[choice - 1]
    print(result)
    return result
    

if __name__ == "__main__":
    ipList = init()
    #ip = getAllIp(ipList)
    ipBlock = chooseInterface(ipList)

    listIp = getAllIp(ipBlock["IP Address"])  
    

