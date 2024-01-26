import platform
import sys
from Linux.linux import get_linux_info
from Windows.windows import get_windows_info
from Tools.help import display_help

def check_platform():
    return platform.system()

def init():
    network_list = []
    if len(sys.argv) > 1 and sys.argv[1] == '-h':
        display_help()
    else:
        current_platform = check_platform()
        if current_platform == 'Windows':
            network_list = get_windows_info()
            return network_list
        elif current_platform == 'Linux':
            get_linux_info()
            return ""
        else:
            print("Unsupported platform:", current_platform)
            return ""



