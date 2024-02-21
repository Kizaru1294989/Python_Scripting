import re
from Tools.mask import mask_cidr



def parse_ipconfig_content_linux(content):
    """
    Function for display and parse interfaces info on linux os
    """
    result = []
    interfaces = content.split('\n\n')
    number = 0

    for interface in interfaces:
        lines = interface.split('\n')
        card_name = None
        ip = None
        mask = None
        gateway = None

        for line in lines:
            if line.strip():
                card_name_match = re.match(r'^\d+: (\S+):', line)
                if card_name_match:
                    if card_name:
                        number += 1
                        info = {
                            "Number": number,
                            "Card Name": card_name,
                            "IP Address": ip,
                            "Subnet Mask": mask,
                            "Default Gateway": gateway
                        }
                        result.append(info)

                    card_name, ip, mask, gateway = card_name_match.group(1), None, None, None
                elif "inet" in line:
                    ip_match = re.search(r'inet (\S+)', line)
                    if ip_match:
                        ip = ip_match.group(1)
                        ip = ip.split('/')[0]

                        mask_match = re.search(r'inet \S+\/(\d+)', line)
                        if mask_match:
                            mask = mask_match.group(1)

                elif "brd" in line:
                    gateway_match = re.search(r'brd (\S+)', line)
                    if gateway_match:
                        gateway = gateway_match.group(1)

        if card_name:
            number += 1
            info = {
                "Number": number,
                "Card Name": card_name,
                "IP Address": ip,
                "Subnet Mask": mask,
                "Default Gateway": gateway
            }
            result.append(info)

    for r in result:
        #print(r)
        print(r['Card Name']) 

    return result




def parse_ipconfig_content_windows(content):
    """
    Function for display and parse interfaces info on Windows os
    """
    result = []
    lines = content.split('\n')
    number = 0
    card_name = None
    ip = None
    mask_input = None
    gateway = None
    for line in lines:
        if line.startswith("Carte"):
            if card_name:
                number += 1
                info = {
                    "Number": number,
                    "Card Name": card_name,
                    "IP Address": ip,
                    "Subnet Mask": mask_input,
                    "Default Gateway": gateway
                }
                result.append(info)

            card_name, ip, mask_input, gateway = None, None, None, None
            card_name = line.split("Carte Ethernet ")[-1].strip()

        elif "Adresse IPv4" in line:
            ip = line.split(":")[-1].strip()
        elif "Masque de" in line:
            mask_input = line.split(":")[-1].strip()
            mask_input = mask_cidr(mask_input)
        elif "Passerelle par" in line:
            gateway = line.split(":")[-1].strip()
        #print(gateway)

    if card_name:
        number += 1
        info = {
            "Number": number,
            "Card Name": card_name,
            "IP Address": ip,
            "Subnet Mask": mask_input,
            "Default Gateway": gateway
        }
        result.append(info)


    return result