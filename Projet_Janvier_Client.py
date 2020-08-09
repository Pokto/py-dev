import sys, os
import socket
import subprocess
import Crypto.Cipher
from Crypto.Cipher import AES


class Connect:
    def __init__(self, port=9999, host="", s=socket.socket()):
        self.port = port
        self.host = host
        self.s = s

############################### Socket client################################################
    def socket_create(self):
        self.host = input("IP hos : ")                                            # Permet de recuperer l'info du entry (IP donnée dans l'interface graphique)

############### Connexion a distance ############################################
    def socket_connect(self):
        try:
            self.s.connect((self.host, self.port))
        except socket.error as msg:
            print("Socket connection error: " + str(msg))

    def kep(self):
        key = open("/key/key.txt", "rb")
        self.key_aes = key.read()
        key.close()
        iv = open("/key/iv.txt", "rb")
        self.iv_aes = iv.read()
        iv.close()
        self.key = AES.new(self.key_aes, AES.MODE_CFB, self.iv_aes)

        key2 = open("/key/key2.txt", "rb")
        self.key_aes2 = key2.read()
        key2.close()
        iv2 = open("/key/iv2.txt", "rb")
        self.iv_aes2 = iv2.read()
        iv2.close()
        self.key2 = AES.new(self.key_aes2, AES.MODE_CFB, self.iv_aes2)


############### Envoie de la reponse des commandes################################
    def send_commands(self):

        msg = input('=>')
        while msg != 'q':
            Connect.kep(self)

            msg = msg.encode('utf-8')
            msg = self.key.encrypt(msg)
            self.s.send(msg)                                 # envoie la commande exit
            data = self.s.recv(1024)
            data = self.key2.decrypt(data)
            data = data.decode('utf-8', 'ignore')
            print(str(data))
            msg = input('=>')


c = Connect()
c.socket_create()
c.socket_connect()
c.send_commands()

###################################################### SOURCES #########################################################
#https://github.com/buckyroberts/Turtle/blob/master/Single_Client/client.py
#https://www.youtube.com/watch?v=YGeRTVaBPoc
#https://www.youtube.com/watch?v=jGnGnro2vsk
#https://www.youtube.com/watch?v=gjU3Lx8XMS8
#https://stackoverflow.com/questions/31756166/python-3-socket-chat-encryption-with-pycrypto-gives-unicodedecodeerror