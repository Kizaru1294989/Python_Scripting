import subprocess
import os
from Tools.interfaces import parse_ipconfig_content

path_txt = './ifconfig_info.txt'

def get_windows_info():
    print("Running on Windows")
    ipconfig_output = subprocess.check_output(['ipconfig'], universal_newlines=True)
    with open(path_txt, 'w') as file:
        file.write(ipconfig_output)
    files = os.listdir('.')
    print("Files in the current directory:", files)
    with open(path_txt, 'r') as file:
        content = file.read()
        #print("Content of ipconfig_info.txt:\n", content)
        #print(content)
        return parse_ipconfig_content(content)
