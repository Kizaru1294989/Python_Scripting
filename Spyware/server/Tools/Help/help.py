from Tools.Color import colors

def display_help():
    """Affiche l'aide et les différentes options disponibles."""
    print(f"{colors.green}-h/--help : affiche l'aide et les différentes options.")
    print(f"-l/--listen <port> : se met en écoute sur le port TCP saisi par l'utilisateur et attend les données du spyware.")
    print(f"-s/--show : affiche la liste des fichiers réceptionnées par le programme.")
    print(f"-r/--readfile <nom_fichier> : affiche le contenu du fichier stocké sur le serveur du spyware. Le contenu doit")
    print(f"-k/--kill : arrête toute les instances de serveurs en cours, avertit le spyware de s'arrêter et de supprimer la capture")