import subprocess
import os
from Tools.interfaces import parse_ipconfig_content_windows

path_txt = './ifconfig_info.txt'

green = "\x1b[32m"
blue = "\x1b[34m"
red = "\x1b[31m"
orange = "\x1b[38;5;220m"

def get_windows_info():
    """
    Function to get network information on Windows.
    """
    print("Running on Windows")
    ipconfig_output = subprocess.check_output(['ipconfig'], universal_newlines=True)
    with open(path_txt, 'w') as file:
        file.write(ipconfig_output)
    files = os.listdir('.')
    print(f"{green} [+]Files in the current directory:", files)
    with open(path_txt, 'r') as file:
        content = file.read()
        #print("Content of ipconfig_info.txt:\n", content)
        #print(content)
        return parse_ipconfig_content_windows(content)
