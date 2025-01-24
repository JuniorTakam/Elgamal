# Projet ElGamal avec PyQt5

Ce projet implémente le système de cryptographie ElGamal en utilisant PyQt5 pour fournir une interface graphique permettant de générer des clés, chiffrer et déchiffrer des messages, tout en facilitant la gestion des fichiers de clés et des fichiers chiffrés.
Fonctionnalités principales

### Génération des clés :
  - Génération des clés publiques et privées.
  - Sauvegarde automatique des clés dans des fichiers séparés.

### Chiffrement :
  - Chiffrement des messages à l'aide de la clé publique générée.
  - Enregistrement du cryptogramme (message chiffré) dans un fichier.

### Déchiffrement :
  - Déchiffrement des messages à l'aide de la clé privée.
  - Affichage du message clair dans l'interface.

### Gestion des fichiers :
  - Sélection de fichiers texte à chiffrer ou à déchiffrer via un explorateur de fichiers.
  - Chargement des clés publiques, privées et du modulus depuis des fichiers externes.

## Prérequis

Avant d'exécuter ce projet, vous devez vous assurer que les modules suivants sont installés :

- PyQt5 : pour l'interface graphique.

Pour installer les modules nécessaires, exécutez :

    pip install PyQt5

## Installation

Clonez le projet depuis GitHub :

    git clone https://github.com/votre-utilisateur/votre-repository.git
    cd votre-repository

Installez les dépendances Python nécessaires comme mentionné ci-dessus.

Ouvrez le fichier elgmal.ui avec Qt Designer si vous souhaitez personnaliser l'interface graphique.

Lancez l'application :

    python main.py

## Utilisation

### Génération des clés :
  - Cliquez sur le bouton "Générer les clés" pour créer un nouveau couple de clés publique/privée et un générateur.
  - Les clés seront sauvegardées automatiquement dans le répertoire ELGAMAL data.

### Chiffrement :
  - Entrez un message dans le champ de texte.*
  - Cliquez sur le bouton "Chiffrer" pour obtenir le cryptogramme.
  - Le message chiffré sera affiché dans la fenêtre de l'interface et sera également enregistré dans un fichier texte.

### Déchiffrement :
  - Sélectionnez un fichier chiffré à l'aide de l'explorateur de fichiers.
  - Chargez les clés nécessaires et cliquez sur "Déchiffrer" pour récupérer le message original.

## Fichiers générés

Lors de l'exécution des différentes opérations, les fichiers suivants seront générés ou mis à jour dans le répertoire ELGAMAL data :

  - Clé publique : public_key_YYYY-MM-DD_HH-MM-SS.txt
  - Clé privée : private_key_YYYY-MM-DD_HH-MM-SS.txt
  - Modulus : modulus_YYYY-MM-DD_HH-MM-SS.txt
  - Générateur : generateur_YYYY-MM-DD_HH-MM-SS.txt
  - Cryptogramme : cryptogramme_YYYY-MM-DD_HH-MM-SS.txt

## Architecture du projet

  - elgamal.py : Contient l'application PyQt5 et la logique principale pour la gestion des clés, du chiffrement, et du déchiffrement.
  - rabinMiller.py : Module pour vérifier la primalité des nombres.
  - confElGamal.py : Contient les paramètres de configuration tels que la taille des clés et les noms des fichiers.
  - elgmal.ui : Interface graphique conçue avec Qt Designer pour interagir avec l'application.

## Contributions

Les contributions sont les bienvenues ! Si vous avez des suggestions ou des améliorations à apporter, n'hésitez pas à ouvrir une pull request ou à soumettre un issue.

## Licence

Ce projet est sous licence MIT.
