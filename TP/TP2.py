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



green = "\x1b[32m"
blue = "\x1b[34m"
red = "\x1b[31m"
orange = "\x1b[38;5;220m"

def netdiscover(mask):
    ip = 2 ** (32 - mask) - 2
    return ip


def getAllIp(ip_address, range_ip):
    network_address = socket.inet_ntoa(struct.pack('>I', struct.unpack('>I', socket.inet_aton(ip_address))[0] &
                                                   struct.unpack('>I', socket.inet_aton("255.255.255.0"))[0]))
    all_ips = [socket.inet_ntoa(struct.pack('>I', struct.unpack('>I', socket.inet_aton(network_address))[0] + i)) for i
               in range(1, int(range_ip))]
    print(f'{blue} [+]{int(range_ip)} IP available')
    # print(all_ips)
    return all_ips


def scan_with_socket(host, port_list):
    r = ping(host, timeout=5)

    if r is not False and r != None:
        print(f"{green} [✅] Ping to {host} successful. time: {r} ms")
        print(f"{blue}----------------PORT----------------")
        for port in port_list:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            if result == 0:
                print(f"{green} [✅] Port {port} of {host} : open")
            else:
                print(f"{red} [❌] Port {port} of {host} : close")
            sock.close()
        print(f"{blue}-------------------------------------")
        return host
    else:
        print(f"{red} [❌] ping failed {host}.")
        return None


# saveResult('./online_ip.txt',result)

def ping_host(host):
    result = []
    r = ping(host, timeout=1)

    if r is not False and r != None :
        #print(r)
        print(f"{green} [✅]Ping to {host} successful. time: {r} ms")
        return host
        # result.append(host)
    else:
        print(f"{red} [❌]Ping to {host} failed.")


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
        print("PING")
        ipBlock = chooseInterface(ipList)
        ip_on_the_network = netdiscover(int(ipBlock["Subnet Mask"]))
        listIp = getAllIp(ipBlock["IP Address"], ip_on_the_network)
        for ip in listIp:
            online_ip = ping_host(ip)
            if online_ip is not None:
                result.append(online_ip)

        if len(sys.argv) > 2 and sys.argv[2] == '-o':
            saveResult("./ip_online_ping.txt", str(result))
        else:
            print("done !")

    if param == 2:
        print(f"{green} [+]PING / SCAN")
        ipBlock = chooseInterface(ipList)
        ip_on_the_network = netdiscover(int(ipBlock["Subnet Mask"]))
        listIp = getAllIp(ipBlock["IP Address"], ip_on_the_network)
        port_list = [80, 22, 443, 21, 587, 23, 102, 9200, 5601]
        for ip in listIp:
            online_ip = scan_with_socket(ip, port_list)
            if online_ip is not None:
                result.append(online_ip)
        if len(sys.argv) > 2 and sys.argv[2] == '-o':
            saveResult("./ip_online_ping_and_scan.txt", str(result))
        else:
            print("done !")
    elif param == None:
        display_argument_help()


if __name__ == "__main__":
    param = None
    if len(sys.argv) > 1 and sys.argv[1] == '-p':
        param = 1
    if len(sys.argv) > 1 and sys.argv[1] == '-s':
        param = 2

    main(param)
