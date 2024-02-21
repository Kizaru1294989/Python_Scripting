

def mask_cidr(masque):
    """
    Function for convert a binary mask to CIDR mask
    """
    octets = masque.split('.')
    bits_a_un = 0
    for octet in octets:
        bits_a_un += bin(int(octet)).count('1')
    cidr =str(bits_a_un)
    return cidr