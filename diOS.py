import os,datetime,webbrowser,sys,subprocess,time,string

#change terminal size (in rows and columns) before putting it in fullscreen mode
sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=50, cols=170))

#install package, here for keyboard package
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

#text colors
class bcolors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def uppercase(text):
    return(text.upper().replace(' ','_'))

def changecolor(color):
    if color=="PURPLE":
        return bcolors.PURPLE
    elif color=="BLUE":
        return bcolors.BLUE
    elif color=="CYAN":
        return bcolors.CYAN
    elif color=="GREEN":
        return bcolors.GREEN
    elif color=="YELLOW":
        return bcolors.YELLOW
    elif color=="RED":
        return bcolors.RED
    elif color=="WHITE":
        return bcolors.WHITE
    elif color=="BOLD":
        return bcolors.BOLD
    elif color=="UNDERLINE":
        return bcolors.UNDERLINE

#initial settings setup
def reset():
    path="C:\\"
    barcolor=bcolors.WHITE
    color=bcolors.WHITE
    list_settings=[
        ["Background Color",["Black","Blue","Green","Aqua","Red","Purple","Yellow","White","Grey","Light Blue","Light Green","Cyan","Light Red","Light Purple","Light Yellow","Bright White"],"0"],
        ["Info Bar Color",["Purple","Blue","Cyan","Green","Yellow","Red","White","Bold","Underline"],"WHITE"],
        ["Text Color",["Purple","Blue","Cyan","Green","Yellow","Red","White","Bold","Underline"],"WHITE"],
        ["Sorting",["By Name","By Type","By Editing Date","Non-Hidden Files First"],"BY_NAME"],
        ["Show Hidden Files",["Yes","No"],"YES"],
         ]
    return(path,barcolor,color,list_settings)

path,barcolor,color,list_settings=reset()

if os.path.isfile('dios_settings.txt'):
    settings_file=open('dios_settings.txt','r')
    settings_lines=settings_file.readlines()    
    if settings_lines[0].startswith('keyboard_installed=') and not settings_lines[0].endswith('YES\n'):
        install('keyboard')
    for line in range(1,len(settings_lines)):
        list_settings[line-1][2]=settings_lines[line].split("=",1)[-1].replace('\n','')
    os.system('color '+list_settings[0][2]+'f')
    barcolor=changecolor(list_settings[1][2])
    color=changecolor(list_settings[2][2])
    settings_file.close()
else:
    install('keyboard')
    settings_file=open('dios_settings.txt','w')
    settings_file.write('background_color=BLACK\n\
keyboard_installed=YES\n\
barcolor=WHITE\n\
color=WHITE\n\
sorting=BY_NAME\n\
show_hidden=YES')
    settings_file.close()

#fullscreen (it's ugly but it does the job), plus blocks the fullscreen key combinations
import keyboard
keyboard.press('f11')
keyboard.release('f11')
keyboard.block_key('f11')
keyboard.add_hotkey("alt + enter", lambda: None, suppress =True)

#block multiple other commands (e.g force exit commands)
keyboard.add_hotkey("alt + f4", lambda: None, suppress =True)
keyboard.add_hotkey("alt + tab", lambda: None, suppress =True)
keyboard.add_hotkey("ctrl + c", lambda: None, suppress =True)
#pages (home, directories, settings)
currentpage="dir"

#logo
print("                                                                                \n\
         @@@  @@            "+f"{bcolors.CYAN}"+".,,,,,,,,,,,,, ."+f"{bcolors.WHITE}"+"                                     \n\
    @@@@@@@  @@.       "+f"{bcolors.CYAN}"+",,,,,,   ,,,,,,,,,,  ,,,,"+f"{bcolors.WHITE}"+"                                 \n\
  .@@  /@@  @@@     "+f"{bcolors.CYAN}"+",,,,,,,,,,,,    ,,,,,,, ,,,,,,"+f"{bcolors.WHITE}"+",                              \n\
  @@   @@  @@@    "+f"{bcolors.CYAN}"+",,,,,,,,,,,,,,,,     ,,,,  ,,,,,,,*"+f"{bcolors.WHITE}"+"                            \n\
 @@#  @@* (@@    "+f"{bcolors.CYAN}"+",,,,                        ,,,,,,,,"+f"{bcolors.WHITE}"+"                            \n\
  @@@@@@  @@       "+f"{bcolors.CYAN}"+",,,,,,,                    ,,,,,  ,,"+f"{bcolors.WHITE}"+"     @@@@@@@@@@@@@@@@@@@@,\n\
               "+f"{bcolors.CYAN}"+",,,,,,,,,                      ,,,.  ,,,,"+f"{bcolors.WHITE}"+"   @@@@@@@@@@@@@@@@@@@@@ \n\
               "+f"{bcolors.CYAN}"+",,,,,,,,                        ,  ,,,,,,"+f"{bcolors.WHITE}"+"  @@@@@@@@               \n\
               "+f"{bcolors.CYAN}"+",,,,,,  ,                        ,,,,,,,,"+f"{bcolors.WHITE}"+"  @@@@@@@                \n\
               "+f"{bcolors.CYAN}"+",,,,,  ,,,                      ,,,,,,,,,"+f"{bcolors.WHITE}"+" /@@@@@@@************    \n\
               "+f"{bcolors.CYAN}"+".,,  ,,,,,                    ,,,,,,,,,,"+f"{bcolors.WHITE}"+"  @@@@@@@@@@@@@@@@@@@@@.  \n\
                  "+f"{bcolors.CYAN}"+"*,,,,,,                            ,"+f"{bcolors.WHITE}"+"    (@@@@@@@@@@@@@@@@@@@   \n\
                  "+f"{bcolors.CYAN}"+",,,,,,,,  ,,/         /,,,,,,,,,,,,"+f"{bcolors.WHITE}"+"                  #@@@@@@   \n\
                   "+f"{bcolors.CYAN}"+",,,,,,,  ,,,,,,   .,,,,,,,,,,,,,"+f"{bcolors.WHITE}"+"                    @@@@@@    \n\
                      "+f"{bcolors.CYAN}"+",,,,,  ,,,,,,,,,   ,,,,,,,,"+f"{bcolors.WHITE}"+"      .@@@@@@@@@@@@@@@@@@@@@    \n\
                         "+f"{bcolors.CYAN}"+",,  ,,,,,,,,,,,,    ."+f"{bcolors.WHITE}"+"         @@@@@@@@@@@@@@@@@@@@@     \n\
                                "+f"{bcolors.CYAN}"+",,,,,,."+f"{bcolors.WHITE}"+"                @@@@@@@@@@@@@@@@@@@       \n\
")

def settings(currentpage):
    global barcolor,color,list_settings
    while 1:
        bar()
        ii=1
        spaces=len(str(len(list_settings)))
        print((" "*(spaces-1))+"0. Reset Settings\n")
        for items in list_settings:
            print((" "*(spaces-len(str(ii))))+str(ii)+". "+str(items[0]))
            ii+=1
        selected=str(input("\n    ")).upper()
        if selected.isnumeric():
            if selected=="0":
                path,barcolor,color,list_settings=reset()
                bar()
                print("Settings have been reset.")
                time.sleep(1)
                return("set")
            if int(selected)-1<len(list_settings) and int(selected)>=0:
                bar()
                ii=1
                spaces=len(str(len(list_settings)))
                choice=int(selected)-1
                #choice = which setting you're changing
                for items in list_settings[choice][1]:
                    print((" "*(spaces-len(str(ii))))+str(ii)+". "+str(items))
                    ii+=1
                selected=str(input("\n    ")).upper()
                if selected.isnumeric():
                    if int(selected)-1<len(list_settings[choice][1]) and int(selected)>=0:
                        if choice>0:
                            list_settings[choice][2]=uppercase(list_settings[choice][1][int(selected)-1])
                        if choice==0:
                            os.system('color '+str(int(selected)-1)+'f')
                            list_settings[0][2]=hex(int(selected)-1).replace('0x','')
                        elif choice==1:
                            print(f"{bcolors.WHITE}")
                            barcolor=changecolor(list_settings[1][2])
                        elif choice==2:
                            print(f"{bcolors.WHITE}")
                            color=changecolor(list_settings[2][2])
                elif selected=="F":
                    return("dir")
                elif selected=="B":
                    return("set")
                elif selected=="E":
                    os.system('color')
                    exit()
                
        elif selected=="F":
            return("dir")
        elif selected=="B":
            return("set")
        elif selected=="E":
            os.system('color')
            exit()

def directories(currentpage,path):
    while 1:
        bar()
        #show path
        print(path+"‖\n"+"═"*len(path)+"╝")
        
        ii=1
        spaces=len(str(len(os.listdir(path))))
        #show hidden files or not
        if list_settings[4][2]=="YES":
            liste=os.listdir(path)
        elif list_settings[4][2]=="NO":
            liste=[f for f in os.listdir(path) if not f.startswith('.')]
        #sort files by setting
        if list_settings[3][2]==["BY_NAME"]:
            liste=liste.sort()
        #show files
        print((" "*(spaces-1))+"0. Switch Drive\n")
        for items in liste:
                print((" "*(spaces-len(str(ii))))+str(ii)+". "+str(items))
                ii+=1
        selected=str(input(f"\n    ")).upper()
        if selected.isnumeric():
            if selected=="0":
                bar()
                ii=1
                available_drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
                spaces=len(str(len(available_drives)))
                for drive in available_drives:
                    print((" "*(spaces-len(str(ii))))+str(ii)+". "+str(drive))
                    ii+=1
                selected=str(input(f"\n    ")).upper()
                if int(selected)-1<len(available_drives) and int(selected)>0:
                    path=available_drives[int(selected)-1]+'\\'
            elif int(selected)-1<len(os.listdir(path)) and int(selected)>0:
                selected=os.listdir(path)[int(selected)-1]
                if os.path.isdir(path+selected):
                    path+=selected+"\\"
                elif os.path.isfile(path+selected):
                    webbrowser.open(path+selected)
        elif selected=="S":
            return("set")
        elif selected=="B" and path.count("\\")>1:
            path=path.rsplit('\\',2)[0]+str("\\")
        elif selected=="E":
            os.system('color')
            exit()
            

def bar():
    os.system("cls")
    #BACKGROUND COLOR
    os.system('color '+list_settings[0][2]+'f')
    #show info

    print(f"{bcolors.WHITE}\u018A\u0131\u0298\u054F"+f"\n    {barcolor}"+datetime.date.today().strftime("%d/%m/%Y")+
          " "+datetime.datetime.now().strftime("%H:%M")+
          " - [B]ack - [S]ettings - [F]ile System - [E]xit"+
          f"{bcolors.WHITE}")
    
    #separator (COMMENT THIS LINE OUT IF YOU WANT TO RUN IN YOU IDE, OTHERWISE YOU'LL NEED TO OPEN IN TERMINAL)
    print("_"*os.get_terminal_size()[0]+f"{color}")

#main loop, sleep for logo
time.sleep(3)
while 1:
    #show page
    if currentpage=="dir":
        currentpage=directories(currentpage,path)
    elif currentpage=="set":
        currentpage=settings(currentpage)
        
#home page
#trier différent (type, nom, date de modif)
#montrer fichiers cachés ou pas
#changer couleur texte, et couleur Barre d'Info
