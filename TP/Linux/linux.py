import subprocess
import os
from Tools.interfaces import parse_ipconfig_content_linux

path_txt = './ifconfig_info.txt'
green = "\x1b[32m"
blue = "\x1b[34m"
red = "\x1b[31m"
orange = "\x1b[38;5;220m"

def get_linux_info():
    print("Running on Linux")
    ifconfig_output = subprocess.check_output(['ip a'], shell=True, universal_newlines=True)
    with open(path_txt, 'w') as file:
        file.write(ifconfig_output)
    files = os.listdir('.')
    print(f"{green} [+]Files in the current directory:", files)
    with open(path_txt, 'r') as file:
        content = file.read()
        #print("Content of ifconfig_info.txt:\n", content)
        return parse_ipconfig_content_linux(content)