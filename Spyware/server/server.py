import socket
import ssl
import os
import sys
from Tools.Main.main import main

if __name__ == '__main__':
    param = None
    if len(sys.argv) <= 1  :
        param = 3
    if len(sys.argv) > 1 and sys.argv[1] == '-h' or len(sys.argv) > 1 and sys.argv[1] == '--help' :
        param = 1
    if len(sys.argv) > 1 and sys.argv[1] == '-l' or len(sys.argv) > 1 and sys.argv[1] == '--listen' :
        if len(sys.argv) > 2 and sys.argv[2] != '':
            param = 2
        else:
            print('please specify a port to listen')
    if len(sys.argv) > 1 and sys.argv[1] == '-s' or len(sys.argv) > 1 and sys.argv[1] == '--show' :
        param = 4
    if len(sys.argv) > 1 and sys.argv[1] == '-r' or len(sys.argv) > 1 and sys.argv[1] == '--readfile' :
        if len(sys.argv) > 2 and sys.argv[2] != '':
            param = 5
        else:
            print('please specify a file to read')
    main(param)
