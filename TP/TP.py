import platform
import sys
from Linux.linux import get_linux_info
from Windows.windows import get_windows_info
from help import display_help

def check_platform():
    return platform.system()



def main():
    if len(sys.argv) > 1 and sys.argv[1] == '-h':
        display_help()
    else:
        current_platform = check_platform()
        if current_platform == 'Windows':
            get_windows_info()
        elif current_platform == 'Linux':
            get_linux_info()
        else:
            print("Unsupported platform:", current_platform)


if __name__ == "__main__":
    main()

