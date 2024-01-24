import subprocess
import os

path_txt = './ifconfig_info.txt'

def get_linux_info():
    print("Running on Linux")
    ifconfig_output = subprocess.check_output(['ifconfig'], universal_newlines=True)
    with open(path_txt, 'w') as file:
        file.write(ifconfig_output)
    files = os.listdir('.')
    print("Files in the current directory:", files)
    with open(path_txt, 'r') as file:
        content = file.read()
        print("Content of ifconfig_info.txt:\n", content)