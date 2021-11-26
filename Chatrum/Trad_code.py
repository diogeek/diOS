alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz,.?' éèçêëàâîïôù^ùü-(!&)#\=~{[`\@}]°+<>;:/§¨£$¤%µ*"+'"'
#print(alphabet)
Dicochiffrage={}
Dicodechiffrage={}
"""
Dicochiffragedeux={}
Dicodechiffragedeux={}
"""
import random

nombresrandom=0
def initialisation(seed):
    global nombresrandom
    nombresrandom=random.sample(range(100,999),len(alphabet))
    #print("les nombres random"+str(nombresrandom))
    for i in range(len(alphabet)):
        Dicodechiffrage[nombresrandom[i]]=alphabet[i]
    #print(len(list(Dicodechiffrage.keys())))
    #print(list(Dicodechiffrage.keys()))
    #print(Dicodechiffrage)
    for i in range(len(alphabet)):
        Dicochiffrage[alphabet[i]]=nombresrandom[i]


def simplification(mot):
    mot = mot.replace("ξ","Ξ")
    mot = mot.replace("ω","Ω")
    mot = mot.replace("Æ","AE")
    mot = mot.replace("Œ","OE")
    mot = mot.replace("æ","ae")
    mot = mot.replace("œ","oe")
    return mot

def dechiffrage(mot):
    #print("avant dechiffrage ",mot)
    resultat = ""
    liste=str(mot).replace("Ξ","").replace("ξ","").split("|")
    #liste=list(filter(None,liste))
    #print(liste)
    for traductible in range(len(liste)):
        liste[traductible]=liste[traductible].replace("Ξ","").replace("ξ","")
    liste=list(filter(None,liste))
    #print(liste)
    for traductible in range(len(liste)):
        if not any(char.isdigit()==False for char in str(liste[traductible])):
                listepartie=[liste[traductible][i:i+3] for i in range(0, len(liste[traductible]), 3)]
                #print(listepartie)
                for lettre in listepartie:
                    #print(lettre)
                    try:
                        #print(Dicodechiffrage.get(int(lettre)))
                        #print(list(Dicodechiffrage.values()))
                        trad=str(Dicodechiffrage.get(int(lettre)))
                        """
                        if trad=="none":
                            trad=str(Dicodechiffragedeux.get(int(lettre)))
                        """
                        #print(lettre)
                        #lettre=Alpha[int(lettre[0])-1][int(lettre[1])-1]
                        resultat += (trad)
                    except:None
        else:
            resultat += liste[traductible]
        if traductible==0 or traductible==1:
            resultat+="Ξ"
    resultat=simplification(resultat)
    #print(resultat)
    return(resultat)

def chiffrage(phrase):
    resultat = ""
    liste=str(phrase).split("|")
    for traductible in range(len(liste)):
        if not any(char.isdigit() for char in str(liste[traductible])):
            liste[traductible]=str(simplification(liste[traductible]))
            import re
            listetrad=re.split('(\s)',str(liste[traductible]))
            for mot in listetrad:
                for lettre in mot:
                    try:
                        lettre=str(__main__.Dicochiffrage.get(lettre))
                    except: None
                    resultat += (lettre)
        else:
            resultat += "|"+liste[traductible]+"|"
    resultat=str(resultat.replace("None",""))
    resultat=str(resultat.replace("  "," "))
    #print(resultat)
    return(str(resultat))

def detect_chiffres(phrase):
    import re
    liste=re.split('Ξ', phrase)
    for traductible in liste:
        if str(traductible).isdecimal():
            liste[liste.index(traductible)]=("|"+str(traductible)+"|")
    phrase=("").join(liste)
    return(chiffrage(str(phrase)))


if __name__ == '__main__':
    initialisation(None)
    while 1:
        try:
            choix=str(input("traduire?\n1-texte vers chiffre\n2-chiffre vers texte\n\n"))
            if choix=="1":
                try:
                    print(detect_chiffres(str(input(">>"))))
                    #chiffrage(str(input(">>")))
                except: None
            elif choix=="2":
                try:
                    print(dechiffrage(str(input(">>"))))
                except: None
        except: None
        print("")
