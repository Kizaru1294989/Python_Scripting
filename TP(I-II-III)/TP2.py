import ipaddress
import argparse
from TP1 import check_platform
from TP1 import init
import socket
import struct
import os
import subprocess
import platform
from ping3 import ping, verbose_ping

def netdiscover(masque):
    nombre_ip_disponibles = 2 ** (32 - masque) - 2
    #print(nombre_ip_disponibles)
    return nombre_ip_disponibles

def getAllIp(ip_address,range_ip):
    network_address = socket.inet_ntoa(struct.pack('>I', struct.unpack('>I', socket.inet_aton(ip_address))[0] & struct.unpack('>I', socket.inet_aton("255.255.255.0"))[0]))
    all_ips = [socket.inet_ntoa(struct.pack('>I', struct.unpack('>I', socket.inet_aton(network_address))[0] + i)) for i in range(1, int(range_ip))]
    print(f'{int(range_ip)} IP range')
    #print(all_ips)
    return all_ips
    
def ping_host(host):
    result = []
    r = ping(host, timeout=1)

    if r is not None:
        print(f"Ping to {host} successful. Round-trip time: {r} ms")
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
    result = []
    ipList = init()
    ipBlock = chooseInterface(ipList)
    ip_on_the_network = netdiscover(int(ipBlock["Subnet Mask"]))
    listIp = getAllIp(ipBlock["IP Address"],ip_on_the_network)
    for ip in listIp:
        online_ip = ping_host(ip)
        if online_ip is not None:
            result.append(online_ip)

    saveResult("./online_ip.txt",str(result))
    

