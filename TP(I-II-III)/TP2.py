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

def getAllIp(ip_address):
    network_address = socket.inet_ntoa(struct.pack('>I', struct.unpack('>I', socket.inet_aton(ip_address))[0] & struct.unpack('>I', socket.inet_aton("255.255.255.0"))[0]))
    all_ips = [socket.inet_ntoa(struct.pack('>I', struct.unpack('>I', socket.inet_aton(network_address))[0] + i)) for i in range(1, 255)]
    #print(all_ips)
    return all_ips
    
def ping_host(host):
    r = ping(host, timeout=5)

    if r is not None:
        print(f"Ping to {host} successful. Round-trip time: {r} ms")
    else:
        print(f"Ping to {host} failed.")
    

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
    ipBlock = chooseInterface(ipList)
    listIp = getAllIp(ipBlock["IP Address"])
    result = []
    for ip in listIp:
        #print(ping_host(ip))
        result.append(ping_host(ip))

    print(result)
    

