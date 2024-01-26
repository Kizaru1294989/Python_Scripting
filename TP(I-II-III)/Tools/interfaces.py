

def parse_ipconfig_content(content):
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


