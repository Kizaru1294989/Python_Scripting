green = "\x1b[32m"
blue = "\x1b[34m"
red = "\x1b[31m"
orange = "\x1b[38;5;220m"



def display_help():
    print(f"{orange} [?] Usage: python.exe .\TP\TP.py")
    print(f"{orange} [?] Options:")
    print(f"{orange} [?]   -h: help")
    
    
    
def display_argument_help():
    print(f"{blue} [?] -p for netdiscover with ping")
    print(f"{blue} [?] -s for netdiscover with ping and port-scanner")
    print(f"{blue} [?] add -o for save the result of the netdiscover on a file")