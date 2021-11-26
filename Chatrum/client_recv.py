import socket
import threading
import time
import sys
from random import randint

hostname = socket.gethostname()
ip_client = socket.gethostbyname(hostname)
print('Ton Adresse IP : {}'.format(ip_client))

ClientMultiSocket = socket.socket()

pseudo=str(randint(111111,999999))+"Ω"
ip=input("IP de l'hôte : ")
password=str(input("Mot de passe : "))
if ip == "":
    ip="localhost"
    ip_client="localhost"
elif ip == "dev":
    ip="localhost"
    ip_client=input("IP du client : ")
score=0
pseudo_avant=""

#print(pseudo,ip)

host = ip
port = 2004

try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))

res = ClientMultiSocket.recv(2048)

message = (str(pseudo)+"Ξ|"+(str(ip_client))+"|Ξconnexion|"+(password)+"|")
#print(message)
ClientMultiSocket.send(str.encode(message))
res = ClientMultiSocket.recv(2048)
if res.decode('utf-8')==("wrong_password"):
    sys.exit("mot de passe incorrect.")
elif res.decode('utf-8').startswith("passed"):
    res=res.decode('utf-8').split("#")
    nombresrandom=res[1]
    res = ClientMultiSocket.recv(2048)
    res=res.decode('utf-8')
    alphabet=res
    print('connecté.')

from Trad_code import detect_chiffres,chiffrage,dechiffrage
Dicochiffrage={}
Dicodechiffrage={}

for i in range(len(alphabet)):
    Dicodechiffrage[nombresrandom[i]]=alphabet[i]
    #print(len(list(Dicodechiffrage.keys())))
    #print(list(Dicodechiffrage.keys()))
for i in range(len(alphabet)):
    Dicochiffrage[alphabet[i]]=nombresrandom[i]

while True:
    res = ClientMultiSocket.recv(2048)
    res=dechiffrage(res.decode('utf-8'))
    data=(res.split("Ξ"))
    #print(data)
    try:
        if data[1]==ip_client:
            data[0]="Vous"
        if str(data[0])!=pseudo_avant:
            print("\n"+data[0]+": "+data[2])
        else:
            print(data[0]+": "+data[2])
    except:
        print(res)
    pseudo_avant=str(data[0])

ClientMultiSocket.close()
