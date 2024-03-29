import platform
import sys
from Linux.linux import get_linux_info
from Windows.windows import get_windows_info
from Tools.argument import display_help 



def check_platform():
    """
    Function for check the current OS
    """
    return platform.system()

def init():
    """
    Function for initialize the first TP
    """
    network_list = []
    if len(sys.argv) > 1 and sys.argv[1] == '-h':
        display_help()
    else:
        current_platform = check_platform()
        if current_platform == 'Windows':
            network_list = get_windows_info()
            return network_list
        elif current_platform == 'Linux':
            network_list = get_linux_info()
            return network_list
        else:
            print("Unsupported platform:", current_platform)
            return ""



