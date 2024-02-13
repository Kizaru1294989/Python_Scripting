from Tools.Color import colors


def terminal():
    """Fonction qui gère l'interaction avec l'utilisateur dans le terminal."""
    cli = input(f"{colors.rainbow}root:~$")
    return cli