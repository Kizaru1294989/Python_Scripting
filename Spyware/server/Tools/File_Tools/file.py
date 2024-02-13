import os


def receive_file(conn, filename):
    """Reçoit un fichier du client et le sauvegarde localement."""
    with open(filename, 'wb') as f:
            chunk = conn.recv(1024) 
            if not chunk:
                exit(1)
            f.write(chunk)
            
def print_directory_tree(root_dir, indent=''):
    """
    Affiche l'arborescence du répertoire à partir de root_dir.
    """
    if os.path.isdir(root_dir):
        print(indent + os.path.basename(root_dir) + '/')
        indent += '  '
        for item in os.listdir(root_dir):
            print_directory_tree(os.path.join(root_dir, item), indent)
    else:
        print(indent + os.path.basename(root_dir))
        

def read_file_in_target(filename):
    """
    Lit le contenu du fichier situé dans le répertoire 'Target'.
    """
    target_dir = 'Target'
    filepath = os.path.join(target_dir, filename)
    if os.path.isfile(filepath):
        with open(filepath, 'r') as file:
            content = file.read()
        return content
    else:
        return f"The file named '{filename}' dont exist in the folder Target "