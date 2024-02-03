Pour créer des certificats auto-signés avec OpenSSL, vous pouvez suivre les étapes ci-dessous. Assurez-vous que vous avez OpenSSL installé sur votre système.

    Création d'une clé privée pour le serveur (server.key):

    bash

openssl genpkey -algorithm RSA -out server.key

Création d'une demande de signature de certificat (server.csr):

bash

openssl req -new -key server.key -out server.csr

Vous serez invité à fournir des informations sur le certificat, telles que le nom commun (Common Name) qui est généralement l'adresse IP ou le nom de domaine du serveur.

Auto-signer le certificat (server.crt):

bash

    openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

    Cela crée un certificat auto-signé valide pour 365 jours. Vous pouvez ajuster la durée de validité selon vos besoins.

Maintenant, vous pouvez utiliser ces fichiers (server.key et server.crt) dans le serveur sécurisé (secure_server.py). Assurez-vous que le client (secure_client.py) a le fichier server.crt pour la vérification du certificat.

N'oubliez pas que dans un environnement de production, il est recommandé d'obtenir un certificat signé par une autorité de certification (CA) plutôt que d'utiliser des certificats auto-signés. Les certificats auto-signés sont principalement destinés à des fins de développement et de test.