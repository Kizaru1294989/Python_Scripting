#!/usr/bin/env python3

import argparse
from TP.TP import main

def getAllIp(ipList):
    """
    Récupère une liste d'adresse ip avec leur sous réseau.
    Décompose la liste avec toute les ip possibles.
    10.10.10.1/24 => 10.10.10.1 à 10.10.10.254
    """
    
def ping(ip):
    TP.display_help
    """
    Retourne si l'ip est disponible et répond aux pings.
    """

def saveResult(path, result):
    """
    Stocke le contenu de la variable result dans le fichier présent dans la variable path
    """

def chooseInterface(ipList):
    """
    Demande à l'utisateur de choisir le bloc d'ip à scanner.
    """

if __name__ == "__main__":
    os = TP1.get_os()
    ipList = TP1.get_ip_configuration(os)        # Retourne la liste des ip des cartes réseaux de la machine
    ipBlock = chooseInterface(ipList)          # L'utilisateur choisit son bloc d'ip
    listIp = getAllIp(ipBlock)

    result = []
    for ip in listIp:
        result.append(ping(ip))
        
    saveResult("./result.txt", result) 