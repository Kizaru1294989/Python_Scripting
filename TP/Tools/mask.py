

def mask_cidr(masque):
    octets = masque.split('.')
    bits_a_un = 0
    for octet in octets:
        bits_a_un += bin(int(octet)).count('1')
    cidr =str(bits_a_un)
    return cidr