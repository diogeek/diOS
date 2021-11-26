import socket
import os
from _thread import *
from random import choices,randint
seed=randint(1,9999999)
#from Trad_code import detect_chiffres,dechiffrage,initialisation
import Trad_code
Trad_code.initialisation(seed)
from string import ascii_lowercase,digits

os.system("mode con: cols=30 lines=50")

class joueur:
    def __init__(self,pseudo,ip,client):
        self.pseudo=pseudo
        self.ip=ip
        self.score=0
        self.client=client

password=str(''.join(choices(ascii_lowercase + digits*2, k = 10)))

ServerSideSocket = socket.socket()
host = ''
port = 2004
ThreadCount = 0
try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Socket is listening.\nPassword : {}'.format(password))
ServerSideSocket.listen(5)

client_recu=0
liste_joueurs=[]

def message_a_tous(message):
    for joueurs in liste_joueurs:
        joueurs.client.sendall(str.encode(message))

def multi_threaded_client(connection):
    global client_recu
    connection.send(str.encode('Server is working:'))
    while True:
        try:
            data = connection.recv(2048)
            #print("avant dechiffrage",data.decode('utf-8'))
        except:
            print("someone quit")
            break
        #print(dechiffrage(data.decode('utf-8')))
        data=Trad_code.dechiffrage(data.decode('utf-8')).split("Ξ")
        #print(data)
        if data[-1]=="connexion"+password:
            connection.sendall(str.encode("passed#"+str(Trad_code.nombresrandom)))
            connection.sendall(str.encode(str(Trad_code.alphabet)))
            reco=False
            for joueurs in liste_joueurs:
                if joueurs.pseudo==data[0]:
                    if joueurs.ip==data[1]:
                        reco=True
                    else:
                        if data[0][-3]=="(" and data[0][-1]==")":
                            try:
                                data[0][-2]=str(int(data[0][-2])+1)
                            except : None
                        else:
                            data[0]+="(1)"
                            #print(data[0])
                            connection.sendall(str.encode(str("pseudo_update,"+data[0])))
            if reco==False:
                joueur1=joueur(data[0],data[1],client_recu)
                liste_joueurs.append(joueur1)
            if "Ω" in data[0]:
                for joueurs in liste_joueurs:
                    if joueurs.ip == data[1]:
                        data[0]=joueurs.pseudo
                        print(str(joueurs.pseudo)+" is listening.")
                        break
            else:
                print(str(data[0])+" connected.")
                message_a_tous(Trad_code.detect_chiffres(str(data[0])+" connected."))
            print("\nConnected :")
            for joueurs in liste_joueurs:
                #if not "Ω" in joueurs.pseudo:
                    print(str(joueurs.pseudo)+" - "+str(joueurs.ip))
        elif data[-1].startswith("connexion"):
            connection.sendall(str.encode("wrong_password"))
        else:
            response = str(Trad_code.detect_chiffres(data[0]))+"Ξ"+str(Trad_code.detect_chiffres(data[1]))+"Ξ"+str(Trad_code.detect_chiffres(data[2]))
            #print(response)
            message_a_tous(response)
        if not data:
            break
    connection.close()

while True:
    Client, address = ServerSideSocket.accept()
    client_recu=Client
    #print('\nConnected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    ThreadCount += 1
    #print('Thread Number: ' + str(ThreadCount) + '\n')
ServerSideSocket.close()
