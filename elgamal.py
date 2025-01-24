#importation des modules pour la cryptographie
import hashlib
import mmap

from random import randrange
from os import path
import pickle
import rabinMiller
from confElGamal import tailleClef, nomClef



# importation des differents modules de PyQt5
from PyQt5 import QtCore, QtWidgets, QtGui, uic, Qt
from PyQt5.uic import loadUi
from PyQt5.QtGui import QTextCursor, QFontMetrics, QFont, QIcon
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QSize
from functools import partial  # pour envoyer un parametre à une fonction avec connect()

# importation des differents modules de communication, parallelisme
import sys,os
from datetime import *
import random

class ELGAMAL_main(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        loadUi("elgmal.ui", self)

        self.pushButton_generer_cle.clicked.connect(self.generate_keys)

        self.p = None
        self.g = None
        self.private_key = None
        self.public_key = None

        self.private_key_recu = None
        self.modulus_recu = None

        self.pushButton_chiffrer.clicked.connect(self.afficher_le_cryptogramme)

        self.pushButton_ouvrir_fichier_clair.clicked.connect(self.ouvrir_l_explorateur)
        self.fichier_selectionne = ""

        # dechiffrage
        self.pushButton_ouvrir_fichier_chiffre.clicked.connect(self.ouvrir_fichier_chiffre)
        self.pushButton_ouvrir_fichier_modulus.clicked.connect(self.ouvrir_fichier_modulus)
        self.pushButton_ouvrir_fichie_cle_privee.clicked.connect(self.ouvrir_fichie_cle_privee)
        self.pushButton_dechiffrer.clicked.connect(self.afficher_le_texte_clair)


    # using the lagrange theoreme, i.e. listing all the possible divisors
    def lagrange(self, n):
        clef = int(n)
        sousClef = clef - 1
        result = []

        # listing all divisor of sousClef
        # for all number below (clef/2)
        for i in range(2, int((sousClef / 2) + 1)):

            # check if the divides sousClef
            if ((sousClef / i) % 1) == 0:
                # building a list of all divisors
                result.append(i)

        # adding sousClef as a divisor of sousClef to the list
        result.append(sousClef)

        return (result)

    # calculating one generator element for Z/nZ
    def calcGene(self, n):
        clef = int(n)
        # getting the list of divisors for n
        diviseur = self.lagrange(clef)
        # and the size of this list
        nbDiviseur = len(diviseur)
        sousClef = clef - 1

        # for each number between 2 and clef
        for i in range(2, clef):
            j = 0

            # do while j doesn't equal the number of divisor (we don't have tested all the divisor for this i)
            while j < nbDiviseur:
                # calculating the order of this i
                tmp = (i ** diviseur[j]) % clef

                # when we find it's order
                if tmp == 1:
                    # we check if it's order is equal to sousClef (i.e. every elements of the group has been generated)
                    if diviseur[j] == sousClef:
                        # if so i is a generator
                        return (i)

                    # if not we change j to go on with the next i
                    else:
                        j = nbDiviseur

                j = j + 1

    # generate and store in several files the differents component of the keys
    def generate_keys(self):
        print("Generating keys, this could take a while...")
        try:
            clef = randrange(0, 2 ** tailleClef)

            while not rabinMiller.isPrime(clef):
                clef = randrange(2, 2 ** tailleClef)

            generator = self.calcGene(clef)
            secret = randrange(1, clef)


            self.p = clef  # le modulus
            self.g = generator
            self.private_key = secret
            self.public_key = (generator ** secret) % clef


            # creation des dossiers
            if not os.path.exists("ELGAMAL data"):
                os.makedirs("ELGAMAL data")
            if not os.path.exists("ELGAMAL data/data encrypt"):
                os.makedirs("ELGAMAL data/data encrypt")
            if not os.path.exists("ELGAMAL data/data decrypt"):
                os.makedirs("ELGAMAL data/data decrypt")

            if not os.path.exists("ELGAMAL data/data encrypt/public key"):
                os.makedirs("ELGAMAL data/data encrypt/public key")
            if not os.path.exists("ELGAMAL data/data encrypt/private key"):
                os.makedirs("ELGAMAL data/data encrypt/private key")
            if not os.path.exists("ELGAMAL data/data encrypt/modulus"):
                os.makedirs("ELGAMAL data/data encrypt/modulus")
            if not os.path.exists("ELGAMAL data/data encrypt/generateur"):
                os.makedirs("ELGAMAL data/data encrypt/generateur")
            if not os.path.exists("ELGAMAL data/data encrypt/cryptogramme"):
                os.makedirs("ELGAMAL data/data encrypt/cryptogramme")

            file_path = "ELGAMAL data/data encrypt/modulus/modulus " + str(datetime.now()) + ".txt"
            file_path = file_path.replace("-", "_")
            file_path = file_path.replace(":", "_")
            file = open(file_path, "w+")
            file.write(str(self.p))
            file.close()

            file_path = "ELGAMAL data/data encrypt/generateur/generateur " + str(datetime.now()) + ".txt"
            file_path = file_path.replace("-", "_")
            file_path = file_path.replace(":", "_")
            file = open(file_path, "w+")
            file.write(str(self.g))
            file.close()

            file_path = "ELGAMAL data/data encrypt/public key/public_key " + str(datetime.now()) + ".txt"
            file_path = file_path.replace("-", "_")
            file_path = file_path.replace(":", "_")
            file = open(file_path, "w+")
            file.write(str(self.public_key))
            file.close()

            file_path = "ELGAMAL data/data encrypt/private key/private_key " + str(datetime.now()) + ".txt"
            file_path = file_path.replace("-", "_")
            file_path = file_path.replace(":", "_")
            file = open(file_path, "w+")
            file.write(str(self.private_key))
            file.close()

            self.notification("Clés générées avec succès", "Modulus: "+str(self.p) + "\nGénérateur: "+str(self.g) +"\nCle publique: "+str(self.public_key) +"\nCle privée: "+str(self.private_key))
        except:
            self.notification("Erreur", "une erreur s'est produite lors de la génération")

    def encrypt(self, message, p, g, public_key):
        clefQ = self.p
        clefH = self.public_key
        clefG = self.g
        byteArr = list(message.encode('utf-8'))
        c1c2 = []
        # encrypting each byte of the file
        for byte in byteArr:
            # random Y for each byte(block)
            clefY = randrange(1, clefQ)
            # first we happen c1
            c1c2.append((clefG ** clefY) % clefQ)

            secret = (clefH ** clefY) % clefQ

            # then c2
            c1c2.append((byte * secret))

        encrypted_message = c1c2

        if not os.path.exists("ELGAMAL data/data encrypt/cryptogramme"):
            os.makedirs("ELGAMAL data/data encrypt/cryptogramme")

        file_path = "ELGAMAL data/data encrypt/cryptogramme/cryptogramme " + str(datetime.now()) + ".txt"
        file_path = file_path.replace("-", "_")
        file_path = file_path.replace(":", "_")
        file = open(file_path, "w+")
        file.write(str(encrypted_message))
        file.close()

        return encrypted_message

    def decrypt(self, encrypted_message, p, private_key):
        secret = int(private_key)
        clefQ = int(p)
        print(encrypted_message)
        crypt = encrypted_message

        i = 0
        clair = []

        while i < len(crypt):
            # decrypting
            clair.append(int(crypt[i + 1] / ((crypt[i] ** secret) % clefQ)))
            i = i + 2


        clair = bytes(clair)

        if not os.path.exists("ELGAMAL data/data decrypt/clair"):
            os.makedirs("ELGAMAL data/data decrypt/clair")

        file_path = "ELGAMAL data/data decrypt/clair/clair " + str(datetime.now()) + ".txt"
        file_path = file_path.replace("-", "_")
        file_path = file_path.replace(":", "_")
        file = open(file_path, "wb+")
        file.write(clair)
        file.close()


        return clair.decode()

    def afficher_le_cryptogramme(self):
        try:
            self.plaintext_chiff = self.textEdit_entrer_texte.toPlainText()
            self.ciphertext = self.encrypt(self.plaintext_chiff, int(self.p), int(self.g), int(self.public_key))
            self.textBrowser_cryptogramme.setText(str(self.ciphertext))
            self.notification("Opération reussie", "Chiffrement éffectué avec succès")
            # self.textBrowser_cryptogramme.setStyleSheet(self.style_base)
        except:
            self.notification("Erreur", "Veuillez entre d'abord générer les clés")

    def afficher_le_texte_clair(self):
        try:
            self.text_clair = self.decrypt(self.cryptogramme_recu, self.modulus_recu, self.private_key_recu)
            #self.textBrowser_texte_clair.setStyleSheet(self.style_base)
            self.textBrowser_texte_clair.setText(str(self.text_clair))
        except:
            a = QtWidgets.QLabel("")
            a.setStyleSheet("color:red;")
            a.styleSheet()
            self.textBrowser_texte_clair.setText("Clé ou format de clé non valide")
            self.textBrowser_texte_clair.setStyleSheet(self.style_base+ " color:rgba(255, 25, 12,255);")

    def ouvrir_l_explorateur(self):
        # Explorateur de fichier
        self.fileDialog = QtWidgets.QFileDialog()

        self.fileDialog.setFileMode(self.fileDialog.AnyFile)
        self.fileDialog.setNameFilter("[Text files (*.txt)]")

        if self.fileDialog.exec_():
            filepath = self.fileDialog.selectedFiles()
            self.fichier_selectionne = filepath[0]

            with open(self.fichier_selectionne, 'r', encoding='utf-8') as f:  # Recup de la clé
                self.plaintext_chiff = f.read()
                self.textEdit_entrer_texte.setText(self.plaintext_chiff)

    def ouvrir_fichier_modulus(self):
        # Explorateur de fichier
        self.fileDialog = QtWidgets.QFileDialog()

        self.fileDialog.setFileMode(self.fileDialog.AnyFile)
        self.fileDialog.setNameFilter("[Text files (*.txt)]")

        if self.fileDialog.exec_():
            filepath = self.fileDialog.selectedFiles()
            self.fichier_selectionne_ = filepath[0]

            with open(self.fichier_selectionne_, 'r') as f:  # Recup de la clé
                self.modulus_recu = f.read()
                self.lineEdit_fichier_a_dechiffre.setText(self.modulus_recu)
    def ouvrir_fichie_cle_privee(self):
        # Explorateur de fichier
        self.fileDialog = QtWidgets.QFileDialog()

        self.fileDialog.setFileMode(self.fileDialog.AnyFile)
        self.fileDialog.setNameFilter("[Text files (*.txt)]")

        if self.fileDialog.exec_():
            filepath = self.fileDialog.selectedFiles()
            self.fichier_selectionne_ = filepath[0]

            with open(self.fichier_selectionne_, 'r') as f:  # Recup de la clé
                self.private_key_recu = f.read()
                self.lineEdit_password_dechiff.setText(self.private_key_recu)

    def ouvrir_fichier_chiffre(self):
        # Explorateur de fichier
        self.fileDialog = QtWidgets.QFileDialog()

        self.fileDialog.setFileMode(self.fileDialog.AnyFile)
        self.fileDialog.setNameFilter("[Text files (*.txt)]")

        if self.fileDialog.exec_():
            filepath = self.fileDialog.selectedFiles()
            self.fichier_selectionne_ = filepath[0]

            with open(self.fichier_selectionne_, 'r') as f:  # Recup de la clé
                self.cryptogramme_recu = eval(f.read())
                self.textEdit_fichier_a_dechiffre.setText(str(self.cryptogramme_recu))

    # message de notification:
    def notification(self, type, msg):
        self.fenetre_notification = QtWidgets.QMainWindow()
        self.fenetre_notification.setGeometry(
            QtCore.QRect(self.x() + int(self.width() / 2) - 130 - 15-60, self.y() + int(self.height() / 2) -80, 200, 147))
        loadUi("notification.ui", self.fenetre_notification)
        # definir une icon au logiciel
        pixmap = QtGui.QPixmap("img/logo3.png")
        icon = QtGui.QIcon(pixmap)
        self.fenetre_notification.setWindowIcon(icon)
        # rend modale la 2ème fenêtre (la 1ère fenêtre sera inactive)
        self.fenetre_notification.setWindowModality(QtCore.Qt.ApplicationModal)
        self.fenetre_notification.line_edit_type_erreur.setText(type)
        self.fenetre_notification.label_erreur.setText(msg)

        # affiche la 2ème fenêtre
        self.fenetre_notification.show()



# """
app = QtWidgets.QApplication(sys.argv)
mainWindow = ELGAMAL_main()
mainWindow.show()
sys.exit(app.exec_())
# """
