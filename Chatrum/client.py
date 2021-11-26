import socket
import threading
import time
import sys

hostname = socket.gethostname()
ip_client = socket.gethostbyname(hostname)
print('Ton Adresse IP : {}'.format(ip_client))

ClientMultiSocket = socket.socket()

pseudo=0
while any(char.isdigit() for char in str(pseudo)):
    pseudo=str(input("\nPseudo : "))
    if any(char.isdigit() for char in str(pseudo)):
        print("pas de nombres")
ip=input("IP de l'hôte : ")
password=str(input("Mot de passe : "))
if ip == "":
    ip="localhost"
    ip_client="localhost"
elif ip == "dev":
    ip="localhost"
    ip_client=input("IP du client : ")
score=0

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
if res.decode('utf-8').startswith('pseudo_update,'):
    pseudo=res.decode('utf-8').replace('pseudo_update,','')
    print("votre pseudo est maintenant {}".format(pseudo))
elif res.decode('utf-8')==("wrong_password"):
    sys.exit("mot de passe incorrect.")
elif res.decode('utf-8').startswith("passed"):
    res=res.decode('utf-8').split("#")
    nombresrandom=res[1]
    res = ClientMultiSocket.recv(2048)
    res=res.decode('utf-8')
    alphabet=res
    print('connecté.')


from Trad_code import detect_chiffres,chiffrage
Dicochiffrage={}
Dicodechiffrage={}

#print(nombresrandom,alphabet)

for i in range(len(alphabet)):
    Dicodechiffrage[nombresrandom[i]]=alphabet[i]
    #print(len(list(Dicodechiffrage.keys())))
    #print(list(Dicodechiffrage.keys()))
for i in range(len(alphabet)):
    Dicochiffrage[alphabet[i]]=nombresrandom[i]

while True:
    score = str(input(">"))
    message = (detect_chiffres(str(pseudo))+"Ξ"+chiffrage(str(ip_client))+"Ξ"+detect_chiffres(str(score)))
    ClientMultiSocket.send(str.encode(message))

ClientMultiSocket.close()
