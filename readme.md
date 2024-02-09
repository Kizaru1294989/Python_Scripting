# Spyware

### Avant de lancer le programme il faut creer les certificats et clefs néccéssaires pour la socket TLS 

#### note : ci vous changez d'ip coté serveur vous devez recreer le certificat donc supprimer le dossier SSL et relancer le programme key_gen.py

```
python3 key_gen.py

```

voici l'arborescence et format généré par le script :


### CA = Certificate Authority
Organisme responsable de signer un certificat
    
Cert = Certificat
Certificat individuel

### -- CA GENERATION -- 

```
openssl genrsa -aes256 -out ca-key.pem 4096
openssl req -new -x509 -sha256 -days 365 -key ca-key.pem -out ca.pem
```


###    -- CERT GENERAT. --
openssl genrsa -out cert-key.pem 4096
openssl req -new -sha256 -subj "/CN=<CN NAME>" -key cert-key.pem -out cert.csr
echo "subjectAltName=IP:<IP SERVER>" >> extfile.cnf
openssl x509 -req -sha256 -days 365 -in cert.csr -CA ca.pem -CAkey ca-key.pem -out cert.pem -extfile extfile.cnf -CAcreateserial
    -------------------

    (( Outfile ))
    ______
    I-- CA
        I-- ca-key.pem    (private key to CA)
        I-- ca.pem        (authority certificate)
    I-- CERT
        I-- cert-key.pem  (private key to cert)
        I-- cert.pem      (certificate)
    ______


    (( Way of working ))
    ______
    I-- Server
        I-- cert.pem      (Public key + Authentication)                                 || cert-server.pem ||
        I-- cert-key.pem  (Private key lik to cert.pem public key)                      || cert-key.pem    ||
    I-- Client
        I-- ca.pem        (To check out the cert.pem authentication provide by server)  || ca-cert.pem     ||
    ______
