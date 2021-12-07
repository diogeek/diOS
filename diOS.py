import os,datetime,webbrowser,sys,subprocess,platform,string,sqlite3

db=sqlite3.connect('dios_events.db')
cursor=db.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS dates(
     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
     date TEXT,
     event TEXT,
     desc TEXT
)
""")
cursor.close()
db.commit()
db.close()

def get_size_screen():
    import ctypes
    user32=ctypes.windll.user32
    return(user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))

def check_installed(pkg):
    try:
        __import__(pkg)
        return(True)
    except ModuleNotFoundError:
        return(False)

#1 character=8 pixels wide, 16 pixels tall
screen_width,screen_height=get_size_screen()
cols=screen_width//8
rows=screen_height//16

available_drives=[]
for d in string.ascii_uppercase:
    if os.path.exists('{}:'.format(d)):
        available_drives.append('{}:'.format(d))

#change terminal size (in rows and columns) before putting it in fullscreen mode
os.system("mode con cols={cols} lines={rows}".format(cols=screen_width//8, rows=200))

#install package, here for keyboard package
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

#text colors
class bcolors:
    #text
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    GOLD = '\033[0;33m'
    WHITE = '\033[1;37m'
    LIGHT_GRAY = '\033[0m'
    DARK_GRAY = '\u001b[1;30m'
    BLACK = '\u001b[30m'
    BRIGHT_PURPLE = '\u001b[1;35m'
    BRIGHT_BLUE = '\u001b[1;34m'
    BRIGHT_CYAN = '\u001b[1;36m'
    BRIGHT_GREEN = '\u001b[1;32m'
    BRIGHT_YELLOW = '\u001b[1;33m'
    BRIGHT_RED = '\u001b[1;31m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    #text background
    BACKGROUND_BLACK = '\u001b[40m'
    BACKGROUND_RED = '\u001b[41m'
    BACKGROUND_GREEN = '\u001b[42m'
    BACKGROUND_YELLOW = '\u001b[43m'
    BACKGROUND_BLUE = '\u001b[44m'
    BACKGROUND_PURPLE = '\u001b[45m'
    BACKGROUND_CYAN = '\u001b[46m'
    BACKGROUND_WHITE = '\u001b[47m'
    BACKGROUND_BRIGHT_BLACK = '\u001b[40;1m'
    BACKGROUND_BRIGHT_RED = '\u001b[41;1m'
    BACKGROUND_BRIGHT_GREEN = '\u001b[42;1m'
    BACKGROUND_BRIGHT_YELLOW = '\u001b[43;1m'
    BACKGROUND_BRIGHT_BLUE = '\u001b[44;1m'
    BACKGROUND_BRIGHT_PURPLE = '\u001b[45;1m'
    BACKGROUND_BRIGHT_CYAN = '\u001b[46;1m'
    BACKGROUND_BRIGHT_WHITE = '\u001b[47;1m'
    #reset
    RESET='\u001b[0m'

def uppercase(text):
    return(text.upper().replace(' ','_'))

def changecolor(color):
    #text
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
    elif color=="GOLD":
        return bcolors.GOLD
    elif color=="WHITE":
        return bcolors.WHITE
    elif color=="LIGHT_GRAY":
        return bcolors.LIGHT_GRAY
    elif color=="DARK_GRAY":
        return bcolors.DARK_GRAY
    elif color=="BLACK":
        return bcolors.BLACK
    elif color=="BRIGHT_PURPLE":
        return bcolors.BRIGHT_PURPLE
    elif color=="BRIGHT_BLUE":
        return bcolors.BRIGHT_BLUE
    elif color=="BRIGHT_CYAN":
        return bcolors.BRIGHT_CYAN
    elif color=="BRIGHT_GREEN":
        return bcolors.BRIGHT_GREEN
    elif color=="BRIGHT_YELLOW":
        return bcolors.BRIGHT_YELLOW
    elif color=="BRIGHT_RED":
        return bcolors.BRIGHT_RED
    elif color=="BRIGHT_BLACK":
        return bcolors.BRIGHT_BLACK
    elif color=="BOLD":
        return bcolors.BOLD
    elif color=="UNDERLINE":
        return bcolors.UNDERLINE

    #text background
    elif color=="BACKGROUND_PURPLE":
        return bcolors.BACKGROUND_PURPLE
    elif color=="BACKGROUND_BLUE":
        return bcolors.BACKGROUND_BLUE
    elif color=="BACKGROUND_CYAN":
        return bcolors.BACKGROUND_CYAN
    elif color=="BACKGROUND_GREEN":
        return bcolors.BACKGROUND_GREEN
    elif color=="BACKGROUND_YELLOW":
        return bcolors.BACKGROUND_YELLOW
    elif color=="BACKGROUND_RED":
        return bcolors.BACKGROUND_RED
    elif color=="BACKGROUND_WHITE":
        return bcolors.BACKGROUND_WHITE
    elif color=="BACKGROUND_BLACK":
        return bcolors.BACKGROUND_BLACK
    elif color=="BACKGROUND_BRIGHT_PURPLE":
        return bcolors.BACKGROUND_BRIGHT_PURPLE
    elif color=="BACKGROUND_BRIGHT_BLUE":
        return bcolors.BACKGROUND_BRIGHT_BLUE
    elif color=="BACKGROUND_BRIGHT_CYAN":
        return bcolors.BACKGROUND_BRIGHT_CYAN
    elif color=="BACKGROUND_BRIGHT_GREEN":
        return bcolors.BACKGROUND_BRIGHT_GREEN
    elif color=="BACKGROUND_BRIGHT_YELLOW":
        return bcolors.BACKGROUND_BRIGHT_YELLOW
    elif color=="BACKGROUND_BRIGHT_RED":
        return bcolors.BACKGROUND_BRIGHT_RED
    elif color=="BACKGROUND_BRIGHT_WHITE":
        return bcolors.BACKGROUND_BRIGHT_WHITE
    elif color=="BACKGROUND_BRIGHT_BLACK":
        return bcolors.BACKGROUND_BRIGHT_BLACK

#function to save settings in text file
def save():
    settings_file=open('dios_settings.txt','w')
    settings_file.write('background_color=0\n\
barcolor='+str(list_settings[1][2])+'\n\
color='+str(list_settings[2][2])+'\n\
sorting='+str(list_settings[3][2])+'\n\
show_hidden='+str(list_settings[4][2])+'\n\
type_to_show='+str(list_settings[5][2])+'\n\
lang_google='+str(list_settings[6][1])+'\n\
date_format='+str(list_settings[7][2])+'')
    settings_file.close()
    
#initial settings setup

def reset():
    path="C:\\"
    barcolor=bcolors.WHITE
    barbackcolor=bcolors.BACKGROUND_BLACK
    color=bcolors.WHITE
    textbackcolor=bcolors.BACKGROUND_BLACK
    date_format="DD/MM/YYYY"
    list_settings=[
        ["Console Background Color",["Black","Blue","Green","Aqua","Red","Purple","Yellow","White","Grey","Light Blue","Light Green","Cyan","Light Red","Light Purple","Light Yellow","Bright White"],"0"],
        ["Info Bar Style",["Purple","Blue","Cyan","Green","Yellow","Red","Gold","White","Light Gray","Dark Gray","Black","Bright Purple","Bright Blue","Bright Cyan","Bright Green","Bright Yellow","Bright Red","Bright Black","Background Purple","Background Blue","Background Cyan","Background Green","Background Yellow","Background Red","Background White","Background Black","Background Bright Purple","Background Bright Blue","Background Bright Cyan","Background Bright Green","Background Bright Yellow","Background Bright Red","Background Bright White","Background Bright Black","Bold","Italic","Underline"],"WHITE"],
        ["UI Style",["Purple","Blue","Cyan","Green","Yellow","Red","Gold","White","Light Gray","Dark Gray","Black","Bright Purple","Bright Blue","Bright Cyan","Bright Green","Bright Yellow","Bright Red","Bright Black","Background Purple","Background Blue","Background Cyan","Background Green","Background Yellow","Background Red","Background White","Background Black","Background Bright Purple","Background Bright Blue","Background Bright Cyan","Background Bright Green","Background Bright Yellow","Background Bright Red","Background Bright White","Background Bright Black","Bold","Italic","Underline"],"WHITE"],
        ["Sorting Files",["By Name","By Type","By Creation Date","Non-Hidden Files First"],"BY_NAME"],
        ["Show Hidden Files",["Yes","No"],"YES"],
        ["Type to Show",["Files Only","Directories Only","Both"],"BOTH"],
        ["Google Search Language","en"],
        ["Date Format",["dd/mm/YYYY","mm/dd/YYYY","YYYY/mm/dd"],"DD/MM/YYYY"]
         ]
    return(path,barcolor,color,list_settings,date_format)

path,barcolor,color,list_settings,date_format=reset()

if not check_installed('keyboard'):
    install('keyboard')
if not check_installed('googlesearch'):
    install('google')

#loading settings from file
if os.path.isfile('dios_settings.txt'):
    settings_file=open('dios_settings.txt','r')
    settings_lines=settings_file.readlines()
    for line in range(0,len(settings_lines)):
        #list_settings[line-{number} WHERE NUMBER IS NUMBER OF NON-SETTINGS LINES IN DIOS_SETTINGS
        if line!=6:
            list_settings[line][2]=settings_lines[line].split("=",1)[-1].replace('\n','')
        else:
            list_settings[6][1]=settings_lines[6].split("=",1)[-1].replace('\n','')
    os.system('color '+list_settings[0][2]+'f')
    barcolor=changecolor(list_settings[1][2])
    color=changecolor(list_settings[2][2])
    date_format=list_settings[7][2]
    settings_file.close()
else:
    settings_file=open('dios_settings.txt','w')
    settings_file.write('background_color=0\n\
barcolor=WHITE\n\
color=WHITE\n\
sorting=BY_NAME\n\
show_hidden=YES\n\
type_to_show=BOTH\n\
lang_google=en\n\
date_format=DD/MM/YYYY')
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

#title screen
def title():
    shift=40
    import getpass
    os.system('cls')
    getpass.getpass("\n"*((rows//2)-16)+"\
"+" "*((cols//2)-shift)+"        @@@  @@@            "+f"{bcolors.CYAN}.,,,,,,,,,,,,, .{bcolors.RESET}                                    \n\
"+" "*((cols//2)-shift)+"   @@@@@@@  ' .       "+f"{bcolors.CYAN},,,,,,   ,,,,,,,,,,  ,,,,{bcolors.RESET}                                 \n\
"+" "*((cols//2)-shift)+" .@@  /@@  @@@     "+f"{bcolors.CYAN},,,,,,,,,,,,    ,,,,,,, ,,,,,,{bcolors.RESET},                              \n\
"+" "*((cols//2)-shift)+" @@   @@  @@@    "+f"{bcolors.CYAN},,,,,,,,,,,,,,,,     ,,,,  ,,,,,,,*{bcolors.RESET}                            \n\
"+" "*((cols//2)-shift)+"@@#  @@* (@@    "+f"{bcolors.CYAN},,,,                        ,,,,,,,,{bcolors.RESET}                            \n\
"+" "*((cols//2)-shift)+" @@@@@@  @@       "+f"{bcolors.CYAN},,,,,,,                    ,,,,,  ,,{bcolors.RESET}     @@@@@@@@@@@@@@@@@@@@,\n\
"+" "*((cols//2)-shift)+"              "+f"{bcolors.CYAN},,,,,,,,,                      ,,,.  ,,,,{bcolors.RESET}   @@@@@@@@@@@@@@@@@@@@@ \n\
"+" "*((cols//2)-shift)+"              "+f"{bcolors.CYAN},,,,,,,,                        ,  ,,,,,,{bcolors.RESET}  @@@@@@@@               \n\
"+" "*((cols//2)-shift)+"              "+f"{bcolors.CYAN},,,,,,  ,                        ,,,,,,,,{bcolors.RESET}  @@@@@@@                \n\
"+" "*((cols//2)-shift)+"              "+f"{bcolors.CYAN},,,,,  ,,,                      ,,,,,,,,,{bcolors.RESET} /@@@@@@@************    \n\
"+" "*((cols//2)-shift)+"              "+f"{bcolors.CYAN}.,,  ,,,,,                    ,,,,,,,,,,{bcolors.RESET}  @@@@@@@@@@@@@@@@@@@@@.  \n\
"+" "*((cols//2)-shift)+"                 "+f"{bcolors.CYAN}*,,,,,,                            ,{bcolors.RESET}    (@@@@@@@@@@@@@@@@@@@   \n\
"+" "*((cols//2)-shift)+"                 "+f"{bcolors.CYAN},,,,,,,,  ,,/         /,,,,,,,,,,,,{bcolors.RESET}                  #@@@@@@   \n\
"+" "*((cols//2)-shift)+"                  "+f"{bcolors.CYAN},,,,,,,  ,,,,,,   .,,,,,,,,,,,,,{bcolors.RESET}                    @@@@@@    \n\
"+" "*((cols//2)-shift)+"                     "+f"{bcolors.CYAN},,,,,  ,,,,,,,,,   ,,,,,,,,{bcolors.RESET}      .@@@@@@@@@@@@@@@@@@@@@    \n\
"+" "*((cols//2)-shift)+"                        "+f"{bcolors.CYAN},,  ,,,,,,,,,,,,    .{bcolors.RESET}         @@@@@@@@@@@@@@@@@@@@@     \n\
"+" "*((cols//2)-shift)+"                               "+f"{bcolors.CYAN},,,,,,.{bcolors.RESET}                @@@@@@@@@@@@@@@@@@@       \n\
"+"\n"*(rows-((rows//2)+1)-10)+"\
"+" "*((cols//2)-7)+"PRESS ENTER")
    return("home")
    

def settings():
    global barcolor,color,list_settings,query,lang_google,date_format
    query=""
    while 1:
        bar()
        ii=1
        spaces=len(str(len(list_settings)))
        print((" "*(spaces-1))+"0. Reset Settings\n")
        for items in list_settings:
            print((" "*(spaces-len(str(ii))))+str(ii)+". "+str(items[0]))
            ii+=1
        print(("\n"+" "*(spaces-1))+str(len(list_settings)+1)+". Save Settings\n")
        selected=str(input("\n    ")).upper()
        if selected.isnumeric():
            if selected=="0":
                path,barcolor,color,list_settings,date_format=reset()
                save()
                bar()
                return("set")
            elif int(selected)-1<len(list_settings) and int(selected)>=0:
                bar()
                ii=1
                spaces=len(str(len(list_settings)))
                choice=int(selected)-1
                #choice = which setting you're changing
                if choice!=6:
                    for items in list_settings[choice][1]:
                        if (choice==2 or choice==3) and items=="Purple":
                            print("- TEXT COLORS\n")
                        elif (choice==2 or choice==3) and items=="Bright Purple":
                            print("\n- BRIGHT TEXT COLORS\n")
                        elif (choice==2 or choice==3) and items=="Background Purple":
                            print("\n- TEXT BACKGROUND COLORS\n")
                        elif (choice==2 or choice==3) and items=="Background Bright Purple":
                            print("\n- BRIGHT TEXT BACKGROUND COLORS\n")
                        elif (choice==2 or choice==3) and items=="Bold":
                            print("\n- TEXT STYLE\n")
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
                                print(f"{bcolors.RESET}")
                                barcolor=changecolor(list_settings[1][2])
                            elif choice==2:
                                print(f"{bcolors.RESET}")
                                color=changecolor(list_settings[2][2])
                            elif choice==7:
                                date_format=list_settings[7][2]
                    elif selected=="H":
                        return("home")
                    elif selected=="B" or selected=="S":
                        return("set")
                    elif selected=="E":
                        os.system('color')
                        exit()
                else:
                    list_languages=['as','ab','ae','of','ak','am','an','ar','as','av','ay','az','ba','be','bg','bh','bi','bm','bn','bo','br','bs','ca','ce','ch','co','cr','cs','cu','cv','cy','da','de','dv','dz','ee','el','en','eo','es','et','eu','fa','ff','fi','fj','fo','fr','fy','ga','gd','gl','gn','gu','gv','ha','he','hi','ho','hr','ht','hu','hy','hz','is','id','ie','ii','ik','io','is','it','iu','ja','jv','ka','kg','ki','kj','kk','kl','km','kn','ko','kr','ks','ku','kv','kw','ky','la','lb','lg','li','ln','lo','lt','lu','lv','mg','mh','mi','mk','ml','mn','mo','mr','ms','mt','my','na','nb','nd','ne','ng','nl','nn','no','nr','nv','ny','oc','oj','om','or','os','pa','pi','pl','ps','pt','qu','rc','rm','rn','ro','ru','rw','sa','sc','sd','se','sg','sh','si','sk','sl','sm','sn','so','sq','sr','ss','st','su','sv','sw','ta','te','tg','th','ti','tk','tl','tn','to','tr','ts','tt','tw','ty','ug','uk','ur','uz','ve','vi','vo','wa','wo','xh','yi','yo','za','zh','zu']
                    print("Enter Google Search Language (Type 'help' for list of languages):")
                    selected=str(input("\n    ")).lower()
                    if selected in list_languages:
                        lang_google=selected
                        return("set")
                    elif selected=="H":
                        return("home")
                    elif selected=="B" or selected=="S":
                        return("set")
                    elif selected=="E":
                        os.system('color')
                        exit()
                    elif selected=="help":
                        print("")
                        for i in [list_languages[i:i+20] for i in range(0,len(list_languages),20)]:
                            print(', '.join(i))
                        import getpass
                        getpass.getpass("\nPress Enter")
                        return("set")
                    else:
                        import time
                        print("Unrecognized Language.")
                        time.sleep(1.5)
                        return("set")
            elif int(selected)-1==len(list_settings):
                save()
        elif selected=="H" or selected=="B":
            return("home")
        elif selected=="F":
            return("dir")
        elif selected=="E":
            os.system('color')
            exit()

def sort_by_creation_date(dirpath):
    a = [s for s in os.listdir(dirpath)]
    a.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
    return a

def folder_is_hidden(filepath):
    import stat
    try:
        return bool(os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)
    except FileNotFoundError:
        return(None)

def listdir_nohidden(path):
    return([f for f in os.listdir(path) if not folder_is_hidden(path+f)])

def sort_by_type(liste):
    listefinal=[f for f in liste if os.path.isfile(path+f)]
    listefinal.append(" ")
    listefinal+=[d for d in liste if os.path.isdir(path+d)]
    return(listefinal)
    
def non_hidden_first(liste):
    listefinal=[f for f in liste if folder_is_hidden(path+f)==False]
    listefinal.append(" ")
    listefinal+=[f for f in liste if folder_is_hidden(path+f)]
    return(listefinal)

def create_file():
    bar()
    print(path+"‖\n"+"═"*len(path)+"╝")
    ii=1
    for items in ["Create A File Here","Create A Directory Here"]:
        print((" "*(spaces-len(str(ii))))+str(ii)+". "+str(items))
        ii+=1
    selected=str(input(f"\n    ")).upper()
    if selected.isnumeric():
        if int(selected)==1:
            bar()
            print(path+"‖\n"+"═"*len(path)+"╝")
            print("Name The File. A Name With No Extension Will Result In A Text File (.txt)")
            try:
                f=open(str(input(f"\n    ")),"w").close()
                return(True)
            except:
                print('Error Creating File. Please Try Again')
                return(False)
        elif int(selected)==2:
            bar()
            print(path+"‖\n"+"═"*len(path)+"╝")
            print("Name The Directory:")
            try:
                os.mkdir(path+str(input(f"\n    ")))
                return(True)
            except:
                print('Error Creating Directory. Please Try Again')
                return(False)
    elif selected=="H":
        return("home")
    elif selected=="S":
        return("set")
    elif selected=="B":
        return("dir")
    elif selected=="E":
        os.system('color')
        exit()

def directories(path):
    while 1:
        bar()
        #show path
        print(path+"‖\n"+"═"*len(path)+"╝")
        
        ii=1
        try:
            spaces=len(str(len(os.listdir(path))))
        except PermissionError:
            import time
            print('Access To This Directory Has Been Denied.')
            time.sleep(1)
            path=path[:path.rfind('\\')]
            return('dir')
            
        #show hidden files or not
        if list_settings[4][2]=="YES":
            liste=os.listdir(path)
        elif list_settings[4][2]=="NO":
            liste=listdir_nohidden(path)
        #sort files by setting
        if list_settings[3][2]=="BY_NAME":
            liste.sort()
        elif list_settings[3][2]=="BY_CREATION_DATE":
            liste=sort_by_creation_date(path)
        elif list_settings[3][2]=="BY_TYPE" and list_settings[5][2]=="BOTH":
            liste=sort_by_type(liste)
        elif list_settings[3][2]=="NON-HIDDEN_FILES_FIRST" and list_settings[4][2]=="YES":
            liste=non_hidden_first(liste)
        #show only wanted type
        if list_settings[5][2]=="FILES_ONLY":
            liste=list(filter(os.path.isfile, os.listdir(path)))
        elif list_settings[5][2]=="DIRECTORIES_ONLY":
            liste=list(filter(os.path.isdir, os.listdir(path)))
        #show files
        if not liste or liste==[' ']:
            print("Files Are Protected Or The Directory Is Empty.")
            liste=[]
        else:
            print((" "*(spaces-1))+"0. Switch Drive\n")
            if list_settings[3][2]=="BY_TYPE":
                print("- FILES:\n")
                for items in liste:
                    if items==" ":
                        print("\n- DIRECTORIES:\n")
                    else:
                        print((" "*(spaces-len(str(ii))))+str(ii)+". "+str(items))
                        ii+=1
            elif list_settings[3][2]=="NON-HIDDEN_FILES_FIRST":
                print("- VISIBLE:\n")
                for items in liste:
                    if items==" ":
                        print("\n- HIDDEN:\n")
                    else:
                        print((" "*(spaces-len(str(ii))))+str(ii)+". "+str(items))
                        ii+=1
            else:
                for items in liste:
                    print((" "*(spaces-len(str(ii))))+str(ii)+". "+str(items))
                    ii+=1
        try:
            liste.pop(liste.index(' '))
        except:None
        print(("\n"+" "*(spaces-len(str(ii))))+str(len(liste)+1)+". Create File Or Directory\n")
        selected=str(input(f"\n    ")).upper()
        if selected.isnumeric():
            if selected=="0":
                while 1:
                    bar()
                    ii=1
                    spaces=len(str(len(available_drives)))
                    for drive in available_drives:
                        print((" "*(spaces-len(str(ii))))+str(ii)+". "+str(drive))
                        ii+=1
                    selected=str(input(f"\n    ")).upper()
                    if selected.isnumeric():
                        if int(selected)-1<len(available_drives) and int(selected)>0:
                            path=available_drives[int(selected)-1]+'\\'
                            break
                    elif selected=="H":
                        return("home")
                    elif selected=="S":
                        return("set")
                    elif selected=="B":
                        if path.count("\\")>1:
                            path=path.rsplit('\\',2)[0]+str("\\")
                        else:
                            return("home")
                    elif selected=="E":
                        os.system('color')
                        exit()
            elif int(selected)-1<len(liste) and int(selected)>0:
                selected=liste[int(selected)-1]
                if os.path.isdir(path+selected):
                    path+=selected+"\\"
                elif os.path.isfile(path+selected):
                    webbrowser.open(path+selected)
            elif int(selected)-1==len(liste):
                while 1:
                    if not create_file():
                        create_file()
                    else :
                        break
        elif selected=="H":
            return("home")
        elif selected=="S":
            return("set")
        elif selected=="B":
            if path.count("\\")>1:
                path=path.rsplit('\\',2)[0]+str("\\")
            else:
                return("home")
        elif selected=="E":
            os.system('color')
            exit()

list_chatrum=["What Is Chatrum ?","Host a Local Chatrum Server","Join a Local Chatrum Server"]
       
def chatrum():
    while 1:
        bar()
        ii=1
        spaces=len(str(len(list_chatrum)))
        for items in list_chatrum:
            print((" "*(spaces-len(str(ii))))+str(ii)+". "+str(items))
            ii+=1
        selected=str(input("\n    ")).upper()
        if selected.isnumeric():
            if int(selected)>1 and int(selected)<4:
                if selected=="2":
                    webbrowser.open('chatrum\server.py')
                webbrowser.open('chatrum\client.py')
                webbrowser.open('chatrum\client_recv.py')
                bar()
            else:
                bar()
                print("Chatrum is a local (LAN), randomly encrypted chatroom.\n\nIt requires a randomly generated Password, and the Host's IP to connect.\nIf you are the Host, putting 'localhost' as Host's IP works just fine too.\n\n\
All you have to do is either host or join a local Chatrum server and enter required info to connect to a Chatrum server and chat with your friends !\n\nThere are basically three scripts :\n\
 - Server.py : The server. It is only used by the Host and gives you the generated password you need to enter the room.\n - Client.py : The first client script. It sends the messages, and is only used for that.\n\
 - Client-recv.py : The second and last client script. It recieves and shows the messages on screen, and is only used for that.\n\n\
It is recommended to put each of your client scripts on each half of your screen for a better chatting experience.\n\nEnjoy! \u263A\n")
            import getpass
            getpass.getpass("Press Enter To Go Back To Homepage.")
            return("home")
        elif selected=="H" or selected=="B":
            return("home")
        elif selected=="S":
            return("set")
        elif selected=="E":
            os.system('color')
            exit()

def show_results(query,page,lang_google):
    import googlesearch
    ii=1
    liste=[]
    for results in googlesearch.search(query, tld='com', lang=lang_google, tbs="0", safe='off', num=10, start=(page-1)*10-1, stop=10, pause=2.0, country='', extra_params=None, user_agent=None, verify_ssl=True):
        print((" "*(2-len(str(ii))))+str(ii)+". "+str(results))
        ii+=1
        liste.append(results)
    return(liste)

google_page=1
query=""
lang_google="en"

def google_search():
    while 1:
        global google_page,query,lang_google
        while query=="":
            bar(True)
            print("Search Google:")
            query =str(input("\n    "))
            google_page=1
        bar()
        print("Results For \""+query+"\" On https://google.com/"+str(lang_google)+":\n")
        liste=show_results(query,google_page,lang_google)
        if google_page>1:
            print("\nPage : "+str(google_page)+" - [P]revious Page - [N]ext Page\n")
        else:
            print("\n[N]ext Page\n")
        selected=str(input("\n    ")).upper()
        if selected.isnumeric():
            if selected>0 and selected <11:
                webbrowser.open(liste[int(selected)-1])
                return("google")
        elif selected=="P" and google_page>1:
            google_page-=1
            return("google")
        elif selected=="N":
            google_page+=1
            return("google")
        elif selected=="H" or selected=="B":
            return("home")
        elif selected=="S":
            return("set")
        elif selected=="E":
            os.system('color')
            exit()

month=int(datetime.date.today().strftime("%m/%Y").split("/")[0])
year=int(datetime.date.today().strftime("%m/%Y").split("/")[1])

def format_date(date):
    global date_format
    date=date.split('/')
    if date_format=="DD/MM/YYYY":
        day=date[0]
        month=date[1]
        year=date[2]
    elif date_format=="MM/DD/YYYY":
        day=date[1]
        month=date[0]
        year=date[2]
    elif date_format=="YYYY/MM/DD":
        day=date[2]
        month=date[1]
        year=date[0]
    return(day+"/"+month+"/"+year)

def deformat_date(date):
    date=date.split('/')
    day=date[0]
    month=date[1]
    year=date[2]
    global date_format
    if date_format=="DD/MM/YYYY":
        return(day+"/"+month+"/"+year)
    elif date_format=="MM/DD/YYYY":
        return(month+"/"+day+"/"+year)
    elif date_format=="YYYY/MM/DD":
        return(year+"/"+month+"/"+day)

def create_event(date):
    db=sqlite3.connect('dios_events.db')
    cursor=db.cursor()
    event=""
    while event=="":
        bar()
        print("Enter The Title Of The Event On "+deformat_date(date)+".\n")
        event=str(input("\n    "))
        if event=="B":
            return("calendar")
        elif event=="H":
            return("home")
        elif event=="S":
            return("set")
        elif event=="E":
            os.system('color')
            exit()
    bar()
    print("Enter The Description Of The Event. (Leave Blank For No Description)")
    desc=str(input("\n    "))
    if desc=="B":
        return("calendar")
    elif desc=="H":
        return("home")
    elif desc=="S":
        return("set")
    elif desc=="E":
        os.system('color')
        exit()
    if len(date.split('/')[0])==1:
        date="0"+date
    insert_query = """INSERT INTO dates (date, event, desc) 
                       VALUES 
                       ('"""+date+"""', '"""+event.replace("'","''")+"""', '"""+desc.replace("'","''")+"""') """
    cursor.execute(insert_query)
    cursor.close()
    db.commit()
    db.close()
    import getpass
    bar(True)
    print("Event '"+event+"' Succesfully Created On "+date+".\n")
    getpass.getpass("   Press Enter")

def list_events(date):
    db=sqlite3.connect('dios_events.db')
    cursor=db.cursor()
    cursor.execute("""SELECT event,desc,id FROM dates WHERE date='"""+date+"""'""")
    events=cursor.fetchall()
    cursor.close()
    db.commit()
    db.close()
    if events:
        events_final=[]
        ids=[]
        for event in events:
            ids.append(event[2])
            if event[1]=="":
                event=str(event[0])
            else:
                event=str(event[0]+" - "+event[1])
            events_final.append(event)
        return(events_final,ids)
    else:
        return(None,None)

def show_events(date):
    while 1:
        events,ids=list_events(date)
        bar()
        if events:
            print("All Events On "+deformat_date(date)+":\n")
            ii=1
            spaces=len(str(len(list_chatrum)))
            for event in events:
                print((" "*(spaces-len(str(ii))))+str(ii)+". "+str(event))
                ii+=1
            print("\nEnter Number Of An Event To Edit Or Delete It.")
            event_choosed=str(input("\n    ")).upper()
            if event_choosed.isnumeric():
                if int(event_choosed)>0 and int(event_choosed)<len(events)+1:
                    bar()
                    print(events[int(event_choosed)-1])
                    print("\n1. Edit Event\n2. Delete Event")
                    selected=str(input("\n    ")).upper()
                    if selected.isnumeric():
                        if selected=="1":
                            edit_event(events[int(event_choosed)-1].split(" - ")[0],events[int(event_choosed)-1].split(" - ")[1],ids[int(event_choosed)-1],date)
                            return(None)
                        elif selected=="2":
                            del_event(events[int(event_choosed)-1].split(" - ")[0],date)
                            return(None)
                    elif selected=="B":
                        return("calendar")
                    elif selected=="H":
                        return("home")
                    elif selected=="S":
                        return("set")
                    elif selected=="E":
                        os.system('color')
                        exit()
            elif selected=="B":
                return("calendar")
            elif selected=="H":
                return("home")
            elif selected=="S":
                return("set")
            elif selected=="E":
                os.system('color')
                exit()
        else:
            return("calendar")

def edit_event(event_title,event_desc,event_id,date):
    import getpass
    db=sqlite3.connect('dios_events.db')
    cursor=db.cursor()
    bar(True)
    print("Current Title Of The Event: '"+str(event_title)+"'.\n\nEnter The New Title Of The Event Or Leave Blank To Skip This Step.")
    new=str(input("\n    "))
    if new:
        event_title=new
    bar(True)
    print("Current Description Of The Event: '"+str(event_desc)+"'.\n\nEnter The New Description Of The Event Or Leave Blank To Skip This Step.")
    new=str(input("\n    "))
    if new:
        event_desc=new
    cursor.execute("""UPDATE dates SET event='"""+event_title+"""', desc='"""+event_desc+"""' WHERE id="""+str(event_id))
    cursor.close()
    db.commit()
    db.close()
    bar(True)
    print("Event '"+event_title+"' Edited.\n")
    getpass.getpass("   Press Enter")

def del_event(event,date):
    import getpass
    db=sqlite3.connect('dios_events.db')
    cursor=db.cursor()
    cursor.execute("""SELECT id FROM dates WHERE date='"""+date+"""' AND event='"""+event.replace("'","''")+"""'""")
    id_event=cursor.fetchall()[0][0]
    cursor.execute("""DELETE FROM dates WHERE id='"""+str(id_event)+"""'""")
    cursor.close()
    db.commit()
    db.close()
    bar(True)
    print("Event '"+event+"' Deleted.\n")
    getpass.getpass("   Press Enter")

def calendar(month,year):
    list_months=["January - Winter","February - Winter","March - ","April - Spring","May - Spring","June - ","July - Summer","August - Summer","September - ","October - Autumn","November - Autumn","December - "]
    list_weekdays=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    day=int(datetime.date.today().strftime("%d"))
    season=""
    if month==3:
        if day<20:
            season="Winter"
        elif day>19:
            season="Spring"
    elif month==6:
        if day<21:
            season="Spring"
        elif day>20:
            season="Summer"
    elif month==9:
        if day<23:
            season="Summer"
        elif day>22:
            season="Autumn"
    elif month==12:
        if day<21:
            season="Autumn"
        elif day>20:
            season="Winter"
    weekdays=f"{bcolors.RESET}\n    \u2502"
    for day in list_weekdays:
        weekdays+=" "+day+" \u2502"
    while 1:
        bar()
        #math for dates
        first_day=datetime.date(year, month, 1).weekday()
        week="     \u2502"*first_day
        day_count=1
        while day_count<8-first_day:
            week+=("  "+str(day_count)+"  \u2502")
            day_count+=1
        #choices
        list_choices=["Change Month","Change Year","Create An Event","See, Edit And Delete Events"]
        
        #show calendar
        print(f"\n    {bcolors.RESET}{bcolors.BRIGHT_RED}\u250F"+"\u2501"*41+"\u2513\n\
    \u2503 "+f"{bcolors.RESET}"+str(list_months[month-1])+season+" ("+str(month)+")"+" "*(40-len(str(list_months[month-1])+season+" ("+str(month)+")"+" "+str(year)))+str(year)+" "+f"{bcolors.BRIGHT_RED}\u2503\n\
    \u2521"+("\u2501"*5+"\u252F")*6+"\u2501"*5+"\u2529"+weekdays+"\n\
    \u251C"+("\u2500"*5+"\u253C")*6+"\u2500"*5+"\u2524\n\
    \u2502"+week)
        next_month=month+1
        next_year=year
        if month==12:
            next_month=1
            next_year=year+1
        how_many_days=(datetime.date(next_year, next_month, 1) - datetime.date(year, month, 1)).days
        days_in_month=[i for i in range(day_count,how_many_days+1)]
        days_in_month=[days_in_month[i:i+7] for i in range(0,len(days_in_month),7)]
        for lines in days_in_month:
            print("    \u251C"+("\u2500"*5+"\u253C")*6+"\u2500"*5+"\u2524")
            if len(lines)<7:
                lines.extend([" " for i in range(7-len(lines))])
            week=""
            for day in lines:
                day=str(day)
                if len(day)==2:
                    day=day[0]+" "+day[1]
                else:
                    day=" "+day+" "
                week+=" "+day+" \u2502"
            print("    \u2502"+week)
        print("    \u2570"+("\u2500"*5+"\u2534")*6+"\u2500"*5+"\u256F\n")
        #selection
        ii=1
        for items in list_choices:
            print((" "*(2-len(str(ii))))+str(ii)+". "+str(items))
            ii+=1
        selected=str(input("\n    ")).upper()
        if selected.isnumeric():
            import time
            selected=int(selected)
            if selected==1:
                selected=0
                print("Enter Month Number:")
                while 1:
                    selected=str(input("\n    "))
                    if selected.isnumeric():
                        if (int(selected)<1 or int(selected)>12):
                            print("\nEnter A Numeric Value Between 1 And 12.")
                            time.sleep(1.5)
                            return("calendar",month,year)
                        return("calendar",int(selected),year)
                    print("\nEnter A Numeric Value Between 1 And 12.")
                    time.sleep(1.5)
                    return("calendar",month,year)
            elif selected==2:
                selected=0
                print("Enter Year:")
                while 1:
                    selected=str(input("\n    "))
                    if selected.isnumeric():
                        if (int(selected)<1 or int(selected)>9998):
                            print("\nEnter A Numeric Value Between 1 And 9998.")
                            time.sleep(1.5)
                            return("calendar",month,year)
                        return("calendar",month,int(selected))
                    print("\nEnter A Numeric Value Between 1 And 9998.")
                    time.sleep(1.5)
                    return("calendar",month,year)
            elif selected==3:
                selected=0
                while selected<1 or selected>how_many_days:
                    print("\nEnter Day Of "+str(list_months[month-1])+" Of "+str(year)+" You Want To Create An Event for.")
                    selected=str(input("\n    "))
                    if selected.isnumeric() and int(selected)>0 and int(selected)<how_many_days+1:
                        break
                    else :
                        print("\nEnter A Numeric Value Between 1 And "+str(how_many_days)+".")
                        time.sleep(1.5)
                        return("calendar",month,year)
                create_event(str(selected)+"/"+str(month)+"/"+str(year))
            while selected==4:
                db=sqlite3.connect('dios_events.db')
                cursor=db.cursor()
                cursor.execute("""SELECT date FROM dates""")
                dates=cursor.fetchall()
                cursor.close()
                db.commit()
                db.close()
                if dates:
                    dates=list(dict.fromkeys(dates))
                    date_selected=0
                    while int(date_selected)<1 or int(date_selected)>len(dates):
                        bar()
                        print("You Have Events On The Following Dates :\n")
                        ii=1
                        spaces=len(str(len(dates)))
                        for date in dates:
                            print((" "*(spaces-len(str(ii))))+str(ii)+". "+deformat_date(date[0]))
                            ii+=1
                        print("\nSelect Date You Want To See, Edit Or Delete The Events Of.")
                        date_selected=str(input("\n    "))
                        if date_selected.isnumeric() and int(date_selected)>0 and int(date_selected)<len(dates)+1:
                            return_value=show_events(dates[int(date_selected)-1][0])
                            if return_value:
                                return(return_value,month,year)
                        elif date_selected=="B":
                            return("calendar",month,year)
                        elif date_selected=="H":
                            return("home",month,year)
                        elif date_selected=="S":
                            return("set",month,year)
                        elif date_selected=="E":
                            os.system('color')
                            exit()
                else:
                    bar()
                    import getpass
                    print("There Are No Events.\n")
                    getpass.getpass("   Press Enter")
                    return("calendar",month,year)
        elif selected=="H" or selected=="B":
            return("home",month,year)
        elif selected=="S":
            return("set",month,year)
        elif selected=="E":
            os.system('color')
            exit()
    
def home():
    global query
    query=""
    #home page, with colored icons (all icons are 11 lines tall and 30 charactrs wide)
    while 1:
        list_home=["title","dir","set","chat","google","calendar"]
        bar()
        print(f"{bcolors.RESET}\n\n\n\n\
    {bcolors.CYAN}        #.  #######, ##            {bcolors.BRIGHT_YELLOW}                                {bcolors.DARK_GRAY}               @@@@@            \n\
    {bcolors.CYAN}     ######,   (####  ####         {bcolors.BRIGHT_YELLOW}    *//////*                    {bcolors.DARK_GRAY}        @@@@  @@@@@@@  @@@@     \n\
    {bcolors.CYAN}   #########       ## ######       {bcolors.BRIGHT_YELLOW}    /,,,,,,,,,,,,,,,,,,,,,.     {bcolors.DARK_GRAY}       @@@@@@@@@@@@@@@@@@@@@    \n\
    {bcolors.CYAN}      ,,               ###  ,      {bcolors.BRIGHT_YELLOW}    //////////////////////.     {bcolors.DARK_GRAY}        @@@@@@@@   @@@@@@@@     \n\
    {bcolors.CYAN} #######               #'  ###     {bcolors.BRIGHT_YELLOW}    //////////////////////.     {bcolors.DARK_GRAY}    @@@@@@@@@@       @@@@@@@@@@ \n\
    {bcolors.CYAN} ####                    #####     {bcolors.BRIGHT_YELLOW}    //////////////////////.     {bcolors.DARK_GRAY}    @@@@@@@@@         @@@@@@@@@ \n\
    {bcolors.CYAN} ##   ##                ######     {bcolors.BRIGHT_YELLOW}    //////////////////////.     {bcolors.DARK_GRAY}    @@@@@@@@@@       @@@@@@@@@@ \n\
    {bcolors.CYAN}    ####              #.,,         {bcolors.BRIGHT_YELLOW}    //////////////////////.     {bcolors.DARK_GRAY}        @@@@@@@@   @@@@@@@@     \n\
    {bcolors.CYAN}   #####  #          .######       {bcolors.BRIGHT_YELLOW}    //////////////////////.     {bcolors.DARK_GRAY}       @@@@@@@@@@@@@@@@@@@@@    \n\
    {bcolors.CYAN}    ##### #####    #######(        {bcolors.BRIGHT_YELLOW}    ,/////////////////////      {bcolors.DARK_GRAY}        @@@@  @@@@@@@  @@@@     \n\
    {bcolors.CYAN}       ##  #######.  ###           {bcolors.BRIGHT_YELLOW}                                {bcolors.DARK_GRAY}               @@@@@            \n\
    \n\
    {bcolors.WHITE}       1.TITLE SCREEN                      2.FILE SYSTEM                       3.SETTINGS\n\
    \n\
    {bcolors.GREEN}                                  {bcolors.RED}          ,(((((((((((                 {bcolors.RED}                             \n\
    {bcolors.GREEN}         @@@@@@@@@@@@@            {bcolors.RED}       ((((((((((((((((((           {bcolors.RED}       ####       ####       \n\
    {bcolors.GREEN}      @@@@@@@@@@@@@@@@@@/         {bcolors.RED}     ((((((((       ((/             {bcolors.RED}    #####################    \n\
    {bcolors.GREEN}    .@@@@@@@@@@@@@@@@@@@@@        {bcolors.BRIGHT_YELLOW}    //{bcolors.RED}((((                          {bcolors.RED}    #####################    \n\
    {bcolors.GREEN}    @@@@@@@@@@@@@@@@@@@@@@@       {bcolors.BRIGHT_YELLOW}   //////       {bcolors.BRIGHT_BLUE},************       {bcolors.WHITE}    #####################    \n\
    {bcolors.GREEN}    @@@@@@@@@@@@@@@@@@@@@@@       {bcolors.BRIGHT_YELLOW}   /////        {bcolors.BRIGHT_BLUE}*/////////////      {bcolors.WHITE}    #######  ###  ###  ##    \n\
    {bcolors.GREEN}    @@@@@@@@@@@@@@@@@@@@@@@       {bcolors.BRIGHT_YELLOW}   //////       {bcolors.BRIGHT_BLUE}*////////////       {bcolors.WHITE}    #####################    \n\
    {bcolors.GREEN}     @@@@@@@@@@@@@@@@@@@@@        {bcolors.BRIGHT_YELLOW}    /{bcolors.GREEN}#####             {bcolors.BRIGHT_BLUE}//////       {bcolors.WHITE}    ##  ###  ###  ###  ##    \n\
    {bcolors.GREEN}      @@@@@@@@@@@@@@@@@@          {bcolors.GREEN}    ########,      ##{bcolors.BRIGHT_BLUE}//////         {bcolors.WHITE}    #####################    \n\
    {bcolors.GREEN}     @@@@*@@@@@@@@@@*             {bcolors.GREEN}       ##################{bcolors.BRIGHT_BLUE}/          {bcolors.WHITE}    ##  ###  ###  #######    \n\
    {bcolors.GREEN}    @@                            {bcolors.GREEN}           ###########              {bcolors.WHITE}    #####################    \n\
    \n\
    {bcolors.WHITE}          4.CHATRUM                       5.GOOGLE SEARCH                      6.CALENDAR\n\
    ")
        selected=str(input("\n    ")).upper()
        if selected.isnumeric():
            return(list_home[int(selected)-1])
        elif selected=="B":
            return("title")
        elif selected=="S":
            return("set")
        elif selected=="E":
            os.system('color')
            exit()

def bar(no_UI=False):
    global currentpage,query
    os.system("cls")
    #BACKGROUND COLOR
    os.system('color '+list_settings[0][2]+'f')

    #show info
    bartext=f"{bcolors.RESET}\u018A\u0131\u0298\u054F\n{barcolor}    "+deformat_date(datetime.date.today().strftime("%d/%m/%Y"))+" "+datetime.datetime.now().strftime("%H:%M")
    db=sqlite3.connect('dios_events.db')
    cursor=db.cursor()
    cursor.execute("""SELECT id FROM dates WHERE date='"""+datetime.date.today().strftime("%d/%m/%Y")+"""'""")
    dates=cursor.fetchall()
    cursor.close()
    db.commit()
    db.close()
    if dates:
        s=""
        if len(dates)>1:
            s="s"
        if "RED" in list_settings[1][2].upper():
            notification_color=f"{bcolors.BRIGHT_BLUE}"
        else:
            notification_color=f"{bcolors.BRIGHT_RED}"
        bartext+=" - ["+notification_color+str(len(dates))+f"{barcolor}] Event"+s+" Today"
    if no_UI==True:
        bartext+=f"{bcolors.RESET}"
    else:
        bartext+=f" - [H]ome - [B]ack - [S]ettings - [E]xit diOS{bcolors.RESET}"
    print(bartext)
    
    #separator (COMMENT THIS LINE OUT IF YOU WANT TO RUN IN YOU IDE, OTHERWISE YOU'LL NEED TO OPEN IN TERMINAL)
    #print("\u2501"*os.get_terminal_size()[0]+f"{color}")

#setting initial page (SET THIS ONE TO "home" IF YOU WANT TO RUN IN YOUR IDE, OTHERWISE YOU'LL NEED TO OPEN IN TERMINAL)
currentpage="title"

while 1:
    #show page
    if currentpage=="title":
        currentpage=title()
    elif currentpage=="home":
        currentpage=home()
    elif currentpage=="dir":
        currentpage=directories(path)
    elif currentpage=="set":
        currentpage=settings()
    elif currentpage=="chat":
        currentpage=chatrum()
    elif currentpage=="google":
        currentpage=google_search()
    elif currentpage=="calendar":
        currentpage,month,year=calendar(month,year)

#notif évènements + mettre plusieurs évènements par jour
#calculator
#snake
#tetris
