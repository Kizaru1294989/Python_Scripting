import re

def parse_ipconfig_content_linux(content):
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
        print(r['Card Name'])  # Move the print statement here

    return result




def parse_ipconfig_content_windows(content):
    result = []
    lines = content.split('\n')
    number = 0
    card_name = None
    ip = None
    mask = None
    gateway = None
    for line in lines:
        if line.startswith("Carte"):
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

            card_name, ip, mask, gateway = None, None, None, None
            card_name = line.split("Carte Ethernet ")[-1].strip()

        elif "Adresse IPv4" in line:
            ip = line.split(":")[-1].strip()
        elif "Masque de" in line:
            mask = line.split(":")[-1].strip()
        elif "Passerelle par" in line:
            gateway = line.split(":")[-1].strip()
        #print(gateway)

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


    return result