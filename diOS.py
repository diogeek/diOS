#check if a module is installed
def check_installed(pkg):
    try:
        __import__(pkg)
        return(True)
    except ModuleNotFoundError:
        return(False)

#install package
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def get_size_screen():
    import ctypes
    user32=ctypes.windll.user32
    return(user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))

#1 character=8 pixels wide, 16 pixels tall
screen_width,screen_height=get_size_screen()
columnslogo=screen_width//8
rows=screen_height//16

import os

#change terminal size (in rows and columns) before putting it in fullscreen mode
os.system("mode con cols={cols} lines={rows}".format(cols=columnslogo, rows=200))

if not check_installed("pynput"):
    install("pynput")

from pynput.keyboard import Key, Listener, Controller
keyboard=Controller()
keyboard.tap(Key.f11) #fullscreen (it's ugly but it does the job)


print("let's ride")

import datetime,webbrowser,sys,subprocess,platform,string,sqlite3,msvcrt,getpass,time

dios_location_path,dios_absolute_path=os.getcwd(),os.getcwd()

if not check_installed("win32com"):
    try : install("pywin32")
    except : install("pypiwin32")

if not check_installed('googlesearch'):
    install('google')

from win32com.client import Dispatch

shell=Dispatch('WScript.shell')
if os.path.isfile(dios_location_path+"\dios.py"): #if you're running the diOS from the file and not from the shortcut
    #creating a shortcut to this file on the desktop, if it doesn't exist
    if not check_installed('winshell'):
        install('winshell')
    import winshell

    desktop = winshell.desktop()
    path=os.path.join(desktop, "diOS.lnk")
    target=os.path.join(os.path.dirname(os.path.abspath(__file__)), "diOS.exe")
    if not os.path.exists(target):
        target=os.path.join(os.path.dirname(os.path.abspath(__file__)), "diOS.py")
    icon=os.path.join(os.path.dirname(os.path.abspath(__file__)), "diOS.ico")

    shortcut=shell.CreateShortCut(path)
    shortcut.Targetpath=target
    shortcut.WorkingDirectory=desktop
    shortcut.IconLocation=icon
    shortcut.save()
    dios_location_path=''
else:
    shortcut = shell.CreateShortCut("diOS.lnk")
    dios_location_path=''.join((shortcut.Targetpath).rsplit('\\', 1)[0])+'\\'
    dios_absolute_path=dios_location_path

#connect to the database (or create it if it doesn't exist)
db=sqlite3.connect(dios_location_path+'.dios_database')
cursor=db.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS dates(
     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
     date TEXT,
     event TEXT,
     desc TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS notes(
     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
     title TEXT,
     text TEXT,
     color TEXT,
     locked TEXT,
     password TEXT
)
""")
db.commit()

available_drives=[]
for d in string.ascii_uppercase:
    if os.path.exists('{}:'.format(d)):
        available_drives.append('{}:'.format(d))

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
    REVERSED = '\u001b[7m'
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

#escaping characters useful to un-print a line in cmd.
CLEAR_DOWN = "\x1b[0J"
SAVE_POSITION = "\u001b[s"
LOAD_POSITION = "\u001b[u"
SET_POSITION_ZERO ="\033[0;0H"
CURSOR_UP = "\033[1A"

#functions for the cursor in cmd
def hide_cursor():
    print('\033[?25l', end="")
def show_cursor():
    print('\033[?25h', end="")

hide_cursor()

def uppercase(text):
    return(text.upper().replace(' ','_'))

colordict={"PURPLE":bcolors.PURPLE,"BLUE":bcolors.BLUE,"CYAN":bcolors.CYAN,"GREEN":bcolors.GREEN,"YELLOW":bcolors.YELLOW,"RED":bcolors.RED,"GOLD":bcolors.GOLD,"WHITE":bcolors.WHITE,"LIGHT_GRAY":bcolors.LIGHT_GRAY,"DARK_GRAY":bcolors.DARK_GRAY,"BLACK":bcolors.BLACK,"BRIGHT_PURPLE":bcolors.BRIGHT_PURPLE,"BRIGHT_BLUE":bcolors.BRIGHT_BLUE,"BRIGHT_CYAN":bcolors.BRIGHT_CYAN,"BRIGHT_GREEN":bcolors.BRIGHT_GREEN,"BRIGHT_YELLOW":bcolors.BRIGHT_YELLOW,"BRIGHT_RED":bcolors.BRIGHT_RED,"BOLD":bcolors.BOLD,"UNDERLINE":bcolors.UNDERLINE,"REVERSED":bcolors.REVERSED,"BACKGROUND_PURPLE":bcolors.BACKGROUND_PURPLE,"BACKGROUND_BLUE":bcolors.BACKGROUND_BLUE,"BACKGROUND_CYAN":bcolors.BACKGROUND_CYAN,"BACKGROUND_GREEN":bcolors.BACKGROUND_GREEN,"BACKGROUND_YELLOW":bcolors.BACKGROUND_YELLOW,"BACKGROUND_RED":bcolors.BACKGROUND_RED,"BACKGROUND_WHITE":bcolors.BACKGROUND_WHITE,"BACKGROUND_BLACK":bcolors.BACKGROUND_BLACK,"BACKGROUND_BRIGHT_PURPLE":bcolors.BACKGROUND_BRIGHT_PURPLE,"BACKGROUND_BRIGHT_BLUE":bcolors.BACKGROUND_BRIGHT_BLUE,"BACKGROUND_BRIGHT_CYAN":bcolors.BACKGROUND_BRIGHT_CYAN,"BACKGROUND_BRIGHT_GREEN":bcolors.BACKGROUND_BRIGHT_GREEN,"BACKGROUND_BRIGHT_YELLOW":bcolors.BACKGROUND_BRIGHT_YELLOW,"BACKGROUND_BRIGHT_RED":bcolors.BACKGROUND_BRIGHT_RED,"BACKGROUND_BRIGHT_WHITE":bcolors.BACKGROUND_BRIGHT_WHITE,"BACKGROUND_BRIGHT_BLACK":bcolors.BACKGROUND_BRIGHT_BLACK}

def changecolor(color):
    return(colordict[color])

#function to handle choices in short menus
keyboard_convertor={b'&':'1',b'1':'1',b'\x82':'2',b'2':'2',b'"':'3',b'3':'3',b"'":'4',b'4':'4',b'(':'5',b'5':'5',b'-':'6',b'6':'6',b'\x8a':'7',b'7':'7',b'_':'8',b'8':'8',b'\x87':'9',b'9':'9',b'\x85':'0',b'0':'0'}

def filternumbers():
    key=msvcrt.getch()
    if key in keyboard_convertor: return keyboard_convertor[key]
    else: return

def filternumbersandmainkeys(limit):
    key=msvcrt.getch()
    if key in keyboard_convertor: return keyboard_convertor[key]
    if key in [bytes(x, 'utf-8') for x in limit if x is not None]+[bytes(x.lower(), 'utf-8') for x in limit if x is not None]: return key.decode('utf-8').upper()
    else: return ''

def filterbykey(filteredkey):
    key=msvcrt.getch()
    key=key.decode('utf-8').upper()
    try:
        if key==filteredkey: return key
    except: return

def filterlargenumbersandmainkeys(limit):
    selected=""
    limit=list(filter(lambda x: x is not None, limit))
    print(f"\t{SAVE_POSITION}[{CLEAR_DOWN}{selected}]{CURSOR_UP}")
    while 1:
        key=msvcrt.getch()
        if key==b'\x08' and selected!="":
            selected=selected[:-1]
        elif key==b'\r' and selected!="":
            return(selected)
        elif key==b'\x1b':
            return("esc")
        elif key in keyboard_convertor:
            selected+=keyboard_convertor[key]
        if key in [bytes(x, 'utf-8') for x in limit]+[bytes(x.lower(), 'utf-8') for x in limit]: return key.decode('utf-8').upper()
        print(f"{LOAD_POSITION}[{CLEAR_DOWN}{selected}]{CURSOR_UP}")
        
#text editing related functions

dictspecialchar={Key.space:" ",Key.tab:"\t"}

def checkchar(key,text,password=False):
    if key==Key.backspace:
        if not text=="":
            return(text[:-1])
        else:
            return("")
    elif key==Key.enter and password==False:
        return(text+"\n")
    elif key in dictspecialchar.keys():
        return text+dictspecialchar[key]
    else :
        try: return text+(str(key.char))
        except: return text

def enter_text(oneline=False):
    text=""
    print(SAVE_POSITION)
    def on_press(key):
        nonlocal text
        try:
            if key==Key.enter and oneline :
                return False
            text=checkchar(key,text)
            print(f"{LOAD_POSITION}{CLEAR_DOWN}{text}|")
        except Exception as e:
            print(e)

    def on_release(key):
        if key == Key.esc and text:
            return False

    with Listener(on_press=on_press, on_release=on_release, suppress=True) as listener:
        listener.join()
    return text

def enter_password():
    password=''
    def on_press(key):
        nonlocal password
        try:
            password=checkchar(key,password,True)
            print(f"{LOAD_POSITION}{CLEAR_DOWN}{'*'*len(password)}|")
        except Exception as e:
            input(e)

    def on_release(key):
        if key == Key.enter and password:
            return False

    with Listener(on_press=on_press, on_release=on_release, suppress=True) as listener:
        listener.join()
    return password

#function to save settings in text file
def save():
    settings_file=open(dios_location_path+'.dios_settings','w')
    settings_file.write(f'background_color=0\n\
barcolor={str(list_settings[1][2])}\n\
color={str(list_settings[2][2])}\n\
sorting={str(list_settings[3][2])}\n\
show_hidden={str(list_settings[4][2])}\n\
type_to_show={str(list_settings[5][2])}\n\
show_file_extensions={str(list_settings[6][2])}\n\
lang_google={str(list_settings[7][1])}\n\
date_format={str(list_settings[8][2])}\n\
logo_color={str(list_settings[9][2])}\n\
')
    settings_file.close()
    
#initial settings setup

def reset():
    path=str(os.path.join("C:\\", os.environ["HOMEPATH"], "Desktop\\"))
    barcolor=bcolors.WHITE
    barbackcolor=bcolors.BACKGROUND_BLACK
    color=bcolors.WHITE
    textbackcolor=bcolors.BACKGROUND_BLACK
    date_format="DD/MM/YYYY"
    list_settings=[
        ["Console Background Color",["Black","Blue","Green","Aqua","Red","Purple","Yellow","White","Grey","Light Blue","Light Green","Cyan","Light Red","Light Purple","Light Yellow","Bright White"],"0"],
        ["Info Bar Style",["Purple","Blue","Cyan","Green","Yellow","Red","Gold","White","Light Gray","Dark Gray","Black","Bright Purple","Bright Blue","Bright Cyan","Bright Green","Bright Yellow","Bright Red","Bright Black","Background Purple","Background Blue","Background Cyan","Background Green","Background Yellow","Background Red","Background White","Background Black","Background Bright Purple","Background Bright Blue","Background Bright Cyan","Background Bright Green","Background Bright Yellow","Background Bright Red","Background Bright White","Background Bright Black","Bold","Underline","Reversed"],"WHITE"],
        ["UI Style",["Purple","Blue","Cyan","Green","Yellow","Red","Gold","White","Light Gray","Dark Gray","Black","Bright Purple","Bright Blue","Bright Cyan","Bright Green","Bright Yellow","Bright Red","Bright Black","Background Purple","Background Blue","Background Cyan","Background Green","Background Yellow","Background Red","Background White","Background Black","Background Bright Purple","Background Bright Blue","Background Bright Cyan","Background Bright Green","Background Bright Yellow","Background Bright Red","Background Bright White","Background Bright Black","Bold","Underline","Reversed"],"WHITE"],
        ["Sorting Files",["By Name","By Type","By Creation Date","Non-Hidden Files First"],"BY_NAME"],
        ["Show Hidden Files in File Explorer",["Yes","No"],"YES"],
        ["Type of Files to Show in File Explorer",["Files Only","Directories Only","Both"],"BOTH"],
        ["Show File extensions in File Explorer",["Yes","No"],"YES"],
        ["Google Search Language","en"],
        ["Date Format",["dd/mm/YYYY","mm/dd/YYYY","YYYY/mm/dd"],"DD/MM/YYYY"],
        ["DiOS Logo Color",["Purple","Blue","Cyan","Green","Yellow","Red","Gold","White","Light Gray","Dark Gray","Bright Purple","Bright Blue","Bright Cyan","Bright Green","Bright Yellow","Bright Red","Reversed"],"CYAN"],
         ]
    return(path,barcolor,color,list_settings,date_format)

path,barcolor,color,list_settings,date_format=reset()

#loading settings from file
if os.path.isfile(dios_location_path+'.dios_settings'):
    settings_file=open(dios_location_path+'.dios_settings','r')
    settings_lines=settings_file.readlines()
    for line in range(0,len(settings_lines)):
        #list_settings[line-{number} WHERE NUMBER IS NUMBER OF NON-SETTINGS LINES IN DIOS_SETTINGS
        if line!=7: #google language line
            list_settings[line][2]=settings_lines[line].split("=",1)[-1].replace('\n','')
        else:
            list_settings[7][1]=settings_lines[7].split("=",1)[-1].replace('\n','')
    os.system('color '+list_settings[0][2]+'f')
    barcolor=changecolor(list_settings[1][2])
    color=changecolor(list_settings[2][2])
    date_format=list_settings[8][2]
    settings_file.close()
else:
    settings_file=open('.dios_settings','w')
    settings_file.write('background_color=0\n\
barcolor=WHITE\n\
color=WHITE\n\
sorting=BY_NAME\n\
show_hidden=YES\n\
type_to_show=BOTH\n\
show_file_extensions=YES\n\
lang_google=en\n\
date_format=DD/MM/YYYY\n\
logo_color=CYAN')
    settings_file.close()

#INITIAL SETUP ^^^^

from shutil import get_terminal_size
columns=get_terminal_size().columns

#SETTINGS, TITLE SCREEN vvvv

def title(logo_color):
    global columnslogo
    os.system('cls')
    print(f"{bcolors.RESET}{bcolors.WHITE}"+"\n"*((rows//2)-16)) #size of logo without escape characters : 92 characters large
    for line in [
f"        ▄██  ███           {bcolors.RESET}{logo_color}▀███████████   ▄{bcolors.RESET}{bcolors.WHITE}                                    ",
f"  ▄███████   ▀▀     {bcolors.RESET}{logo_color}▄████▄▄   ▀█████████  ███▄▄{bcolors.RESET}{bcolors.WHITE}                                ",
f" ▐█▌  ▐██  ███   {bcolors.RESET}{logo_color}▄███████████▄   ▀██████▄  █████▄{bcolors.RESET}{bcolors.WHITE}                              ",
f" ██   ██▌ ███   {bcolors.RESET}{logo_color}████████████▀▀▀▀   ▀▀████  ███████ {bcolors.RESET}{bcolors.WHITE}                            ",
f"▐█▌  ▐██ ▐██   {bcolors.RESET}{logo_color}██▀    ▄▄▄               ▀  ██████  ▄{bcolors.RESET}{bcolors.WHITE}                           ",
f" ▀█████▌ ██   {bcolors.RESET}{logo_color}    ▄▄███▀                   ████▀  ▄██{bcolors.RESET}{bcolors.WHITE}     ▄███████████████████ ",
f"             {bcolors.RESET}{logo_color} ▄███████                      ██▀  ▄████{bcolors.RESET}{bcolors.WHITE}   ████████████████████  ",
f"             {bcolors.RESET}{logo_color}███████▀                           ██████{bcolors.RESET}{bcolors.WHITE}  ████████▀              ",
f"             {bcolors.RESET}{logo_color}██████  ▄                        ████████{bcolors.RESET}{bcolors.WHITE} ▄███████                ",
f"             {bcolors.RESET}{logo_color}████▀  ██                       ████████▀{bcolors.RESET}{bcolors.WHITE} ████████▄▄▄▄▄▄▄▄▄▄▄▄    ",
f"             {bcolors.RESET}{logo_color}███▀ ▄████                     ████▀▀   {bcolors.RESET}{bcolors.WHITE}  █████████████████████   ",
f"              {bcolors.RESET}{logo_color}█▀  ██████                         ▄▄█{bcolors.RESET}{bcolors.WHITE}    ▀███████████████████▌  ",
f"               {bcolors.RESET}{logo_color}  ███████  ▄              ▄█████████{bcolors.RESET}{bcolors.WHITE}                   ██████▌  ",
f"                {bcolors.RESET}{logo_color}▀███████  ▀██▄▄▄▄    ▄████████████{bcolors.RESET}{bcolors.WHITE}                  ▄███████   ",
f"                 {bcolors.RESET}{logo_color}▀███████  ███████▄▄  ▀█████████▀{bcolors.RESET}{bcolors.WHITE}    ▄█████████████████████    ",
f"                   {bcolors.RESET}{logo_color}▀▀████   █████████▄▄  ▀████▀{bcolors.RESET}{bcolors.WHITE}      █████████████████████     ",
f"                       {bcolors.RESET}{logo_color}▀▀▀  ▀███████████▄ {bcolors.RESET}{bcolors.WHITE}           ███████████████████▀      "]:
        print(line.center(columnslogo))
    getpass.getpass("\n\n\n"+"PRESS ENTER".center(columns))
    return("home")
    

def settings():
    global barcolor,color,list_settings,query,lang_google,date_format,events_key
    query=""
    while 1 :
        bar()
        ii=1
        spaces=len(str(len(list_settings)))
        print((" "*(spaces-1))+"0. Reset Settings\n")
        for items in list_settings:
            print((" "*(spaces-len(str(ii))))+str(ii)+". "+str(items[0]))
            ii+=1
        print(("\n"+" "*(spaces-len(str(ii))))+str(len(list_settings)+1)+". Save Settings\n")
        while 1:
            selected=filterlargenumbersandmainkeys([*['H','B','E'],('V' if events_key else None)])
            if selected.isnumeric():
                if selected=="0":
                    path,barcolor,color,list_settings,date_format=reset()
                    bar()
                    return("set")
                elif int(selected)-1<len(list_settings) and int(selected)>=0:
                    bar()
                    ii=1
                    spaces=len(str(len(list_settings)))
                    choice=int(selected)-1
                    #choice = which setting you're changing
                    if choice!=7: #google lang
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
                        selected=filterlargenumbersandmainkeys(['H','B','S','E'])
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
                                elif choice==8:
                                    date_format=list_settings[8][2]
                        elif selected=="B":
                            return("set")
                        elif selected in navigation_dict : return(navigation_dict[selected])
                    else:
                        list_languages=['as','ab','ae','of','ak','am','an','ar','as','av','ay','az','ba','be','bg','bh','bi','bm','bn','bo','br','bs','ca','ce','ch','co','cr','cs','cu','cv','cy','da','de','dv','dz','ee','el','en','eo','es','et','eu','fa','ff','fi','fj','fo','fr','fy','ga','gd','gl','gn','gu','gv','ha','he','hi','ho','hr','ht','hu','hy','hz','is','id','ie','ii','ik','io','is','it','iu','ja','jv','ka','kg','ki','kj','kk','kl','km','kn','ko','kr','ks','ku','kv','kw','ky','la','lb','lg','li','ln','lo','lt','lu','lv','mg','mh','mi','mk','ml','mn','mo','mr','ms','mt','my','na','nb','nd','ne','ng','nl','nn','no','nr','nv','ny','oc','oj','om','or','os','pa','pi','pl','ps','pt','qu','rc','rm','rn','ro','ru','rw','sa','sc','sd','se','sg','sh','si','sk','sl','sm','sn','so','sq','sr','ss','st','su','sv','sw','ta','te','tg','th','ti','tk','tl','tn','to','tr','ts','tt','tw','ty','ug','uk','ur','uz','ve','vi','vo','wa','wo','xh','yi','yo','za','zh','zu']
                        print("Enter Google Search language (Type 'help' for list of languages):")
                        selected=str(input("\n    ")).lower()
                        if selected in list_languages:
                            lang_google=selected
                            return("set")
                        elif selected=="B":
                            return("set")
                        elif selected in navigation_dict : return(navigation_dict[selected])
                        elif selected=="help":
                            print("")
                            for i in [list_languages[i:i+20] for i in range(0,len(list_languages),20)]:
                                print(', '.join(i))
                            getpass.getpass("\nPress Enter")
                            return("set")
                        else:
                            print("Unrecognized Language.")
                            time.sleep(1.5)
                            return("set")
                elif int(selected)-1==len(list_settings):
                    save()
                    continue
            elif selected=="B":
                return("home")
            elif selected in navigation_dict : return(navigation_dict[selected])
            else: continue
            break

#SETTINGS, TITLE SCREEN ^^^^

#file explorer functions vvvv

def sort_by_creation_date(dirpath):
    a = [s for s in os.listdir(dirpath)]
    a.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
    return a

def is_hidden(filepath):
    import stat
    try:
        return bool(os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)
    except FileNotFoundError:
        return(None)

def create_list(path, show_hidden_files):
    liste=[]
    if not "DIRECTORIES_ONLY" in list_settings[5][2]: #if list_settings[5][2]=="FILES_ONLY":
        liste+=([x for x in os.listdir(path) if os.path.isfile(os.path.join(path, x))] if show_hidden_files=="YES" else [x for x in os.listdir(path) if os.path.isfile(os.path.join(path, x)) and not is_hidden(os.path.join(path, x))])
    if not "FILES_ONLY" in list_settings[5][2]: #elif list_settings[5][2]=="DIRECTORIES_ONLY":
        liste+=([x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))] if show_hidden_files=="YES" else [x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x)) and not is_hidden(os.path.join(path, x))])
    return liste#return([f for f in os.listdir(path) if not is_hidden(path+f)])

def sort_by_type(liste):
    listefinal=[f for f in liste if os.path.isfile(path+f)]
    listefinal.append(" ")
    listefinal+=[d for d in liste if os.path.isdir(path+d)]
    return(listefinal)
    
def non_hidden_first(liste):
    listefinal=[f for f in liste if is_hidden(path+f)==False]
    listefinal.append(" ")
    listefinal+=[f for f in liste if is_hidden(path+f)]
    return(listefinal)

#file explorer functions ^^^^

#ALL APPLICATIONS vvvv

def create_file():
    bar()
    print(f"{path}‖\n{'═'*len(path)}╝")
    ii=1
    for items in ["Create A File Here","Create A Directory Here"]:
        print((" "*(spaces-len(str(ii))))+str(ii)+". "+str(items))
        ii+=1
    selected=filterlargenumbersandmainkeys([*['H','B','S','E'],('V' if events_key else None)])
    if selected.isnumeric():
        if int(selected)==1:
            bar()
            print(f"{path}‖\n{'═'*len(path)}╝")
            print("Name the File. A name with no extension will result in a Text file (.txt)")
            try:
                f=open(str(input(f"\n    ")),"w").close()
                return(True)
            except:
                print('Error creating File. Please try again')
                return(False)
        elif int(selected)==2:
            bar()
            print(f"{path}‖\n{'═'*len(path)}╝")
            print("Name the Directory:")
            try:
                os.mkdir(path+str(input(f"\n    ")))
                return(True)
            except:
                print('Error creating Directory. Please try again')
                return(False)
    elif selected=="B":
        return("dir")
    elif selected in navigation_dict : return(navigation_dict[selected])

def target(shortcut):
    return str(shell.CreateShortCut(shortcut).TargetPath)

def directories(path):
    while 1:
        bar()
        #show path
        print(f"{path}‖\n{'═'*len(path)}╝")
        
        ii=1
        try:
            spaces=len(str(len(os.listdir(path))))
        except PermissionError:
            print('Access to this Directory has been Denied.')
            time.sleep(1)
            path=path[:path.rfind('\\')]
            return('dir')
            
        #creating list, deciding on showing hidden files or not, and if there are only directories, files or both.
        liste=create_list(path, list_settings[5][2])
        #sort files by setting
        if list_settings[3][2]=="BY_NAME":
            liste.sort()
        elif list_settings[3][2]=="BY_CREATION_DATE":
            liste=sort_by_creation_date(path)
        elif list_settings[3][2]=="BY_TYPE" and list_settings[5][2]=="BOTH":
            liste=sort_by_type(liste)
        elif list_settings[3][2]=="NON-HIDDEN_FILES_FIRST" and list_settings[4][2]=="YES":
            liste=non_hidden_first(liste)
        #show files
        if not liste or liste==[' ']:
            print("Files are protected, the directory is empty or your settings return no results here.")
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
        print(("\n"+" "*(spaces-len(str(ii))))+str(len(liste)+1)+". Create File or Directory\n")
        while 1:
            selected=filterlargenumbersandmainkeys([*['H','B','S','E'],('V' if events_key else None)])
            if selected.isnumeric():
                if selected=="0":
                    while 1:
                        bar()
                        ii=1
                        spaces=len(str(len(available_drives)))
                        for drive in available_drives:
                            print((" "*(spaces-len(str(ii))))+str(ii)+". "+str(drive))
                            ii+=1
                        selected=filterlargenumbersandmainkeys([*['H','B','S','E'],('V' if events_key else None)])
                        if selected.isnumeric():
                            if int(selected)-1<len(available_drives) and int(selected)>0:
                                path=available_drives[int(selected)-1]+'\\'
                                break
                        elif selected=="B":
                            if path.count("\\")>1:
                                path=path.rsplit('\\',2)[0]+str("\\")
                            else:
                                return("home")
                        elif selected in navigation_dict : return(navigation_dict[selected])
                elif int(selected)-1<len(liste) and int(selected)>0:
                    selected=liste[int(selected)-1]
                    if os.path.isdir(path+selected):
                        path+=selected+"\\"
                    elif selected.endswith(".lnk"):
                        path=target(path+selected)
                    elif os.path.isfile(path+selected):
                        webbrowser.open(path+selected)
                elif int(selected)-1==len(liste):
                    while 1:
                        if not create_file():
                            create_file()
                        else :
                            break
            elif selected=="B":
                if path.count("\\")>1:
                    path=path.rsplit('\\',2)[0]+str("\\")
                else:
                    return("home")
            elif selected in navigation_dict : return(navigation_dict[selected])
            else: continue
            break

list_chatrum=["What Is Chatrum ?","Host a Local Chatrum Server","Join a Local Chatrum Server"]
       
def chatrum():
    while 1:
        bar()
        ii=1
        spaces=len(str(len(list_chatrum)))
        for items in list_chatrum:
            print((" "*(spaces-len(str(ii))))+str(ii)+". "+str(items))
            ii+=1
        selected=filternumbersandmainkeys([*['H','B','S','E'],('V' if events_key else None)])
        if selected.isnumeric():
            if int(selected)>1 and int(selected)<4:
                if selected=="2":
                    webbrowser.open(dios_location_path+'chatrum\server.py')
                webbrowser.open(dios_location_path+'chatrum\client.py')
                webbrowser.open(dios_location_path+'chatrum\client_recv.py')
                bar()
            else:
                bar()
                print("Chatrum is a local (LAN), randomly encrypted chatroom.\n\nIt requires a randomly generated Password, and the Host's IP to connect.\nIf you are the Host, putting 'localhost' as Host's IP works just fine too.\n\n\
All you have to do is either host or join a local Chatrum server and enter required info to connect to a Chatrum server and chat with your friends !\n\nThere are basically three scripts :\n\
 - Server.py : The server. It is only used by the Host and gives you the generated password you need to enter the room.\n - Client.py : The first client script. It sends the messages, and is only used for that.\n\
 - Client-recv.py : The second and last client script. It recieves and shows the messages on screen, and is only used for that.\n\n\
It is recommended to put each of your client scripts on each half of your screen for a better chatting experience.\n\nEnjoy! \u263A\n")
            getpass.getpass("Press Enter to go back to Homepage.")
            return("home")
        elif selected=="B":
            return("home")
        elif selected in navigation_dict : return(navigation_dict[selected])

def show_results(query,page,lang_google):
    import googlesearch
    ii=1
    liste=[]
    try:
        for results in googlesearch.search(query, tld='com', lang=lang_google, tbs="0", safe='off', num=10, start=(page-1)*10-1, stop=10, pause=2.0, country='', extra_params=None, user_agent=None, verify_ssl=True):
            print((" "*(2-len(str(ii))))+str(ii)+". "+str(results))
            ii+=1
            liste.append(results)
    except Exception as e:
        return([f"Search was not successful. Error :'{e}'"])
    return(liste)

google_page=1
query=""
lang_google="en"

def google_search():
    while 1:
        global google_page,query,lang_google
        while query=="":
            bar(UI=False)
            print("Search Google:")
            query =str(input("\n    "))
            google_page=1
        bar()
        print("Results for \""+query+"\" on https://google.com/"+str(lang_google)+":\n")
        liste=show_results(query,google_page,lang_google)
        if google_page>1:
            print("\nPage : "+str(google_page)+" - [P]revious Page - [N]ext Page\n")
        else:
            print("\n[N]ext Page\n")
        selected=filterlargenumbersandmainkeys([*['H','B','S','E','P','N'],('V' if events_key else None)])
        if selected.isnumeric():
            if int(selected)>0 and int(selected)<11:
                webbrowser.open(liste[int(selected)-1])
                return("google")
        elif selected=="P" and google_page>1:
            google_page-=1
            return("google")
        elif selected=="N":
            google_page+=1
            return("google")
        elif selected=="B":
            return("home")
        elif selected in navigation_dict : return(navigation_dict[selected])

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

def create_event(date,cursor):
    event=""
    while event=="":
        bar()
        print("Enter the name of the event on "+deformat_date(date)+".\n\t")
        event=enter_text(oneline=True)
        if event.upper()=="B":
            return("calendar")
        elif event_upper() in navigation_dict : return(navigation_dict[selected])
    bar()
    print("Enter the description of the event. (Leave blank for no description)\n\t")
    desc=enter_text(oneline=True)
    if desc.upper()=="B":
        return("calendar")
    elif desc.upper() in navigation_dict : return(navigation_dict[selected])
    if len(date.split('/')[0])==1:
        date="0"+date
    insert_query = """INSERT INTO dates (date, event, desc) 
                       VALUES 
                       ('"""+date+"""', '"""+event.replace("'","''")+"""', '"""+desc.replace("'","''")+"""') """
    cursor.execute(insert_query)
    db.commit()
    bar(UI=False)
    print("Event '"+event+"' succesfully created on "+date+".\n")
    getpass.getpass("   Press Enter")

def list_events(date,cursor):
    cursor.execute("""SELECT event,desc,id FROM dates WHERE date='"""+date+"""'""")
    events=cursor.fetchall()
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
        bar(no_events=True)
        if events:
            print("All events on "+deformat_date(date)+":\n")
            ii=1
            spaces=len(str(len(list_chatrum)))
            for event in events:
                print((" "*(spaces-len(str(ii))))+str(ii)+". "+str(event))
                ii+=1
            print("\nEnter number of an event to edit or delete it.")
            event_choice=filterlargenumbersandmainkeys(['H','B','S','E'])
            if event_choice.isnumeric():
                if int(event_choice)>0 and int(event_choice)<len(events)+1:
                    bar(no_events=True)
                    print(events[int(event_choice)-1])
                    print("\n1. Edit Event\n2. Delete Event\n")
                    selected=filternumbersandmainkeys(['H','B','S','E'])
                    if selected.isnumeric():
                        if selected=="1":
                            edit_event(events[int(event_choice)-1].split(" - ")[0],events[int(event_choice)-1].split(" - ")[1],ids[int(event_choice)-1],date)
                        elif selected=="2":
                            del_event(events[int(event_choice)-1].split(" - ")[0],date)
                    elif selected=="B":
                        return("events")
                    elif selected in navigation_dict : return(navigation_dict[selected])
            elif event_choice=="B":
                return("calendar")
            elif event_choice in navigation_dict : return(navigation_dict[selected])
        else:
            return("calendar")

def edit_event(event_title,event_desc,event_id,date,cursor):
    bar(UI=False)
    print("Current title of the event: '"+str(event_title)+"'.\n\nEnter the new title of the event or leave blank to skip this step.")
    new=enter_text(oneline=True)
    if new:
        event_title=new
    bar(UI=False)
    print("Current description of the event: '"+str(event_desc)+"'.\n\nEnter the new description of the event or leave blank to skip this step.")
    new=enter_text(oneline=True)
    if new:
        event_desc=new
    cursor.execute("""UPDATE dates SET event='"""+event_title.replace("'","''")+"""', desc='"""+event_desc.replace("'","''")+"""' WHERE id="""+str(event_id))
    db.commit()
    bar(UI=False)
    print("Event '"+event_title+"' edited.\n")
    getpass.getpass("   Press Enter")

def del_event(event,date,cursor):
    selected=0
    bar()
    print("Delete Event ?\n1. Yes\n2. No\n")
    selected=filternumbersandmainkeys([*['H','B','S','E'],('V' if events_key else None)])
    if selected=="1":
        cursor.execute("""SELECT id FROM dates WHERE date='"""+date+"""' AND event='"""+event.replace("'","''")+"""'""")
        id_event=cursor.fetchall()[0][0]
        cursor.execute("""DELETE FROM dates WHERE id='"""+str(id_event)+"""'""")
        db.commit()
        bar(UI=False)
        print("Event '"+event+"' deleted.\n")
        getpass.getpass("   Press Enter")
    elif selected=="B":
        return("home",month,year)
    elif selected in navigation_dict : return(navigation_dict[selected])

def calendar(month,year,cursor):
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
        print("")
        selected=filternumbersandmainkeys([*['H','B','S','E'],('V' if events_key else None)])
        if selected.isnumeric() or selected=="V":
            if selected=="1":
                selected=0
                print("\nEnter Month Number:")
                while 1:
                    selected=filterlargenumbersandmainkeys(['H','B','S','E'])
                    if selected.isnumeric():
                        if (int(selected)<1 or int(selected)>12):
                            print("\nEnter a numeric value between 1 and 12.")
                            time.sleep(1)
                            return("calendar",month,year)
                        return("calendar",int(selected),year)
                    elif selected=="B":
                        return("home",month,year)
                    elif selected in navigation_dict : return(navigation_dict[selected])
                    elif selected=="esc" :
                        return("calendar",month,year)
            elif selected=="2":
                selected=0
                print("Enter Year:")
                while 1:
                    bar(escape=True, change=True)
                    selected=filterlargenumbersandmainkeys(['H','B','S','E'])
                    if selected.isnumeric():
                        if int(selected)<1 or int(selected)>9998:
                            print("\nEnter a numeric value between 1 and 9998.")
                            time.sleep(1.5)
                            return("calendar",month,year)
                        return("calendar",month,int(selected))
                    elif selected=="B":
                        return("home",month,year)
                    elif selected in navigation_dict : return(navigation_dict[selected])
                    elif selected=="esc" :
                        return("calendar",month,year)
                    print("\nEnter a numeric value between 1 and 9998.")
                    time.sleep(1.5)
                    return("calendar",month,year)
            elif selected=="3":
                selected=0
                while selected<1 or selected>how_many_days:
                    bar(escape=True, change=True)
                    print("Enter the day of "+str(list_months[month-1]).split(" - ")[0]+" of "+str(year)+" you want to create an event for.\n")
                    selected=filterlargenumbersandmainkeys(['H','B','S','E'])
                    if selected.isnumeric() and int(selected)>0 and int(selected)<how_many_days+1:
                        break
                    elif selected=="B":
                        return("home",month,year)
                    elif selected in navigation_dict : return(navigation_dict[selected])
                    elif selected=="esc" :
                        return("calendar",month,year)
                create_event(str(selected)+"/"+str(month)+"/"+str(year))
            try:
                while selected=="4" or (events_key==True and selected=="V"):
                    cursor.execute("""SELECT date FROM dates""")
                    dates=cursor.fetchall()
                    db.commit()
                    if dates:
                        dates=list(dict.fromkeys(dates))
                        date_selected=0
                        while int(date_selected)<1 or int(date_selected)>len(dates):
                            date_selected=0
                            bar()
                            print("You have events on the following dates :\n")
                            ii=1
                            spaces=len(str(len(dates)))
                            for date in dates:
                                print((" "*(spaces-len(str(ii))))+str(ii)+". "+deformat_date(date[0]))
                                ii+=1
                            print("\nSelect date you want to see, edit or delete the events of.\n")
                            date_selected=filterlargenumbersandmainkeys(['H','B','S','E'])
                            if date_selected.isnumeric() and int(date_selected)>0 and int(date_selected)<len(dates)+1:
                                return_value=show_events(dates[int(date_selected)-1][0])
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
                        print("There are no events.\n")
                        getpass.getpass("   Press Enter")
                        return("calendar",month,year)
            except Exception as e:
                input(e)
        elif selected=="B":
            return("home",month,year)
        elif selected in navigation_dict : return(navigation_dict[selected])


def create_note():
    title=""
    while not title:
        bar(UI=False)
        print("Enter the Title of the Note.\n\t")
        title=enter_text(oneline=True).replace("'","''")
    bar(UI=False)
    print("Write your Note, and press Escape when Done.\n")
    text=enter_text()
    
    color=0
    colors=["Purple","Blue","Cyan","Green","Yellow","Red","Gold","White","Light Gray","Dark Gray","Bright Purple","Bright Blue","Bright Cyan","Bright Green","Bright Yellow","Bright Red"]
    while not (int(color)>0 and int(color)<len(colors)+1):
        bar()
        print("Choose a Color for your Note :\n")
        ii=1
        spaces=len(str(len(colors)))
        for color in colors:
            print((" "*(spaces-len(str(ii))))+str(ii)+". "+color)
            ii+=1
        color=filterlargenumbersandmainkeys([*['H','B','S','E'],('V' if events_key else None)])
        if color.isnumeric():
            if int(color)>0 and int(color)<len(colors)+1:
                break
        elif color=="B": return("home")
        elif color in navigation_dict : return(navigation_dict[selected])
        else: color=0
    color=uppercase(colors[int(color)-1])
    locked=0
    while not locked in ("1","2"):
        bar(UI=False)
        print("Lock this Note?\n\n1. YES\n2. NO")
        locked=filternumbers()
        if locked in ["1","2"]:
            if ["YES","NO"][int(locked)-1]=="YES":
                bar(UI=False)
                print("Enter a password for your Note.\n\n     "+SAVE_POSITION)
                password=enter_password()
    
    cursor.execute(f"""INSERT INTO notes (title, text, color, locked, password)
               VALUES 
               ('{title}', '{text}', '{color}', '{lockedlist[int(locked)-1]}', '{password}')""")
    db.commit()

def edit_note(note,cursor):
    note_id=note[0]
    title=note[1]
    text=note[2]
    color=note[3]
    locked=note[4]
    password=note[5]
    bar(UI=False)
    print(f"Current title of the Note: '{str(title)}'.\n\nEnter the new title of the Note or leave blank to skip this step.")
    title=(enter_text() or title)
    """
    new=enter_text(oneline=True)
    if new:
        title=new"""
    bar(UI=False)
    print("Enter new text to write in the Note or leave blank to skip this step. Press Escape to proceed when finished.\n\n     "+SAVE_POSITION)
    text=(enter_text() or text)
    #text=new if new:=enter_text() else text
    colors=["Purple","Blue","Cyan","Green","Yellow","Red","Gold","White","Light Gray","Dark Gray","Bright Purple","Bright Blue","Bright Cyan","Bright Green","Bright Yellow","Bright Red"]
    spaces=len(str(len(colors)))
    while 1:
        bar()
        print(f"Current color of the Note: '{str(color)}'.\n\nChoose a new color or leave blank to skip this step.")
        ii=1
        for color in colors:
            print((" "*(spaces-len(str(ii))))+str(ii)+". "+color)
            ii+=1
        new=filterlargenumbersandmainkeys([*['H','B','S','E'],('V' if events_key else None)])
        if new:
            if new.isnumeric():
                if int(new)>0 and int(new)<len(colors)+1: break
            elif new=="B":
                return("notes")
            elif new in navigation_dict : return(navigation_dict[selected])
                
        else: break
        
        print("Please Enter a numeric value between 1 and "+str(len(colors)+1)+".")
        time.sleep(1.5)
    color=(colors[int(new)-1] or color)
    new=3
    while not new in ["1","2"]:
        bar(UI=False)
        print("Note is currently {'not ' if locked=='NO' else ''}locked.\n\nLock it?\n\n1. YES\n2. NO")
        new=filternumbers()
    locked=['YES','NO'][int(new)-1]
    if locked=="YES":
        bar(UI=False)
        print("Enter a password for your Note.\n\n     "+SAVE_POSITION)
        password=enter_password()
        
    
    cursor.execute("""UPDATE notes SET title='"""+title.replace("'","''")+"""', text='"""+text.replace("'","''")+"""', color='"""+uppercase(color)+"""', locked='"""+locked+"""', password='"""+password+"""' WHERE id="""+str(note_id))
    db.commit()
    bar(UI=False)
    print(f"Note '{title}' edited.\n")
    getpass.getpass("   Press Enter")
    return(title,text,changecolor(uppercase(color)),locked,password)

def delete_note(note_id,title,cursor):
    selected=0
    while not selected in ['1','2']:
        bar()
        print("Delete Note ?\n1. Yes\n2. No\n")
        selected=filternumbers()
    if selected=='1':
        cursor.execute("""DELETE FROM notes WHERE id='"""+str(note_id)+"""'""")
        db.commit()
        bar(UI=False)
        print("Note '"+title+"' deleted.\n")
        getpass.getpass("   Press Enter")
        return("notes")
    else:
        return(None)
    

def read_note(note,cursor):
    if note[4]=="YES":
        trypass=""
        while trypass=="":
            bar()
            print("Enter the password for this Note.\n\n     "+SAVE_POSITION)
            trypass=enter_password()
            
        if trypass!=note[5]:
            bar(UI=False)
            print("Wrong Password.\n\nPress [D] to force delete the note or Enter to proceed.")
            selected=filterbykey("D")
            if selected=="D": delete_note(note[0],note[1],cursor)
            return("notes")
    if note[4]=="NO" or trypass==note[5]:
        global color
        note_color=changecolor(note[3])
        while 1:
            bar()
            print(f"{note_color}████████████████████ "+note[1]+f"{bcolors.RESET}{color}\n")
            print(note[2].replace("''","'"))
            print("1. Edit Note\n2. Delete Note\n")
            selected=filternumbersandmainkeys([*['H','B','S','E'],('V' if events_key else None)])
            if selected=="1": title,text,note_color,locked,password=edit_note(note,cursor)
            elif selected=="2":
                returnvalue=delete_note(note[0],note[1],cursor)
                if returnvalue: return(returnvalue)
            elif selected=="B": return("notes")
            elif selected in navigation_dict : return(navigation_dict[selected])
def notes():
    global color
    while 1:
        bar()
        db=sqlite3.connect(dios_location_path+'.dios_database')
        cursor=db.cursor()
        cursor.execute("""SELECT id,title,text,color,locked,password FROM notes""")
        notes=cursor.fetchall()
        cursor.close()
        db.commit()
        db.close()
        print("Your Notes :\n\n0. Create a Note\n")
        if notes:
            notes_graph = [notes[x:x+3] for x in range(0, len(notes),3)]
            ii=1
            for line in notes_graph:
                text=[
                    "    ",
                    "    ",
                    "    ",
                    "    ",
                    "    ",
                    "    ",
                    "    ",
                    "    ",
                    ]
                for note in line:
                    title=note[1]
                    if len(title)>11: title=title[:8]+"..."
                    if note[4]=="YES":
                        locked="locked"
                        preview="///////////"
                    else:
                        locked="unlocked"
                        preview=note[2].replace("\n","  ")
                        if len(preview)>1: preview=preview[:8]+"..."
                    text[0]+=str(ii)+"."+" "*(17-len(str(ii)))
                    text[1]+=f"{changecolor(note[3])}█████████████"+f"{bcolors.RESET}{color}     "
                    text[2]+=f"{changecolor(note[3])}█"+title+"█"*(12-len(title))+f"{bcolors.RESET}{color}     "
                    text[3]+=f"{changecolor(note[3])}█████████████"+f"{bcolors.RESET}{color}     "
                    text[4]+=f"{changecolor(note[3])}█"+preview+"█"*(12-len(preview))+f"{bcolors.RESET}{color}     "
                    text[5]+=f"{changecolor(note[3])}█████████████"+f"{bcolors.RESET}{color}     "
                    text[6]+=f"{changecolor(note[3])}█"+locked+"█"*(12-len(locked))+f"{bcolors.RESET}{color}     "
                    text[7]+=f"{changecolor(note[3])}█████████████"+f"{bcolors.RESET}{color}     "
                    ii+=1
                for line in text: print(line)
                print("")
            print("\nSelect a Note to read, edit or delete it.")
        else: print("You haven't wrote any Note yet.\n")
        selected=filterlargenumbersandmainkeys([*['H','B','S','E'],('V' if events_key else None)])
        if selected=="0":
            returnvalue=create_note()
            if returnvalue: return(returnvalue)
        elif selected.isnumeric():
            if int(selected)>0 and int(selected)<len(notes)+1: return(read_note(notes[int(selected)-1],cursor))
        elif selected=="B": return("home")
        elif selected in navigation_dict : return(navigation_dict[selected])

def cmd():
    os.system("cls")
    os.system("cmd /k echo Type 'exit' to go back to diOS.")
    return("home")

def starwars():
    os.system("cls")
    print("\nPress escape and type 'exit' to go back to diOS.")
    time.sleep(1)
    os.system("cmd /k telnet towel.blinkenlights.nl")
    return("home")

#ALL APPLICATIONS ^^^^

#HOME, BAR, LOOP vvvv

def home(logo_color,homepage):
    global query,events_key
    query=""
    list_home=[["title","dir","set","notes","chat","google","calendar","cmd"],["starwars"]]
    max_homepage=2
    #home page, with colored icons (all icons are 11 lines tall and 30 characters wide)
    bar(homepages=True)
    if homepage==1:
        print(f"{bcolors.RESET}\n\n\n\n\
    {bcolors.RESET}{logo_color}       ▄▄  ▀███████▄ ▐██▄          {bcolors.RESET}{bcolors.BRIGHT_YELLOW}                                {bcolors.RESET}{bcolors.DARK_GRAY}               ▄███▄            {bcolors.RESET}{bcolors.YELLOW}                                 \n\
    {bcolors.RESET}{logo_color}     ▄█████▄  ▀█████▌ ████▄        {bcolors.RESET}{bcolors.BRIGHT_YELLOW}    ▄█████████████████████      {bcolors.RESET}{bcolors.DARK_GRAY}        ▄██▄  ███████  ▄██▄     {bcolors.RESET}{bcolors.YELLOW}         ████████████████████▄   \n\
    {bcolors.RESET}{logo_color}   ▄████████▀▀   ▀▀▀█ █████        {bcolors.RESET}{bcolors.BRIGHT_YELLOW}    █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄      {bcolors.RESET}{bcolors.DARK_GRAY}       █████████████████████    {bcolors.RESET}{bcolors.YELLOW}        ████▀▀▀▀▀▀▀▀▀▀▀▀▀███ █   \n\
    {bcolors.RESET}{logo_color}      ▄▄▄▄            ████  █      {bcolors.RESET}{bcolors.BRIGHT_YELLOW}    ██████████████████████      {bcolors.RESET}{bcolors.DARK_GRAY}        ▀█████▀▀   ▀▀█████▀     {bcolors.RESET}{bcolors.YELLOW}        █████████████████████    \n\
    {bcolors.RESET}{logo_color}  ▄████▀               █▀  ███     {bcolors.RESET}{bcolors.BRIGHT_YELLOW}    ██████████████████████      {bcolors.RESET}{bcolors.DARK_GRAY}     ▄███████         ███████▄  {bcolors.RESET}{bcolors.YELLOW}        ███▀▀▀▀▀▀▀▀▀▀▀▀▀████     \n\
    {bcolors.RESET}{logo_color}  ███▀  ▄                ▄████     {bcolors.RESET}{bcolors.BRIGHT_YELLOW}    ██████████████████████      {bcolors.RESET}{bcolors.DARK_GRAY}    ████████           ████████ {bcolors.RESET}{bcolors.YELLOW}        ████████████████████     \n\
    {bcolors.RESET}{logo_color}  ██▀ ▄██              ▄████▀▀     {bcolors.RESET}{bcolors.BRIGHT_YELLOW}    ██████████████████████      {bcolors.RESET}{bcolors.DARK_GRAY}     ▀███████         ███████▀  {bcolors.RESET}{bcolors.YELLOW}        ███▀▀▀▀▀▀▀▀▀▀▀▀▀████     \n\
    {bcolors.RESET}{logo_color}  █▀ ▄███▌            ▄█▀▀  ▄      {bcolors.RESET}{bcolors.BRIGHT_YELLOW}    ██████████████████████      {bcolors.RESET}{bcolors.DARK_GRAY}        ▄█████▄▄   ▄▄█████▄     {bcolors.RESET}{bcolors.YELLOW}        ████████████████████     \n\
    {bcolors.RESET}{logo_color}    ▄████▌ █▄▄▄   ▄▄▄▄▄▄▄▄███      {bcolors.RESET}{bcolors.BRIGHT_YELLOW}    ██████████████████████      {bcolors.RESET}{bcolors.DARK_GRAY}       █████████████████████    {bcolors.RESET}{bcolors.YELLOW}        ██▀▀▀▀▀▀▀▀▀▀▀▀▀█████     \n\
    {bcolors.RESET}{logo_color}    ▀█████ ▐████▄  ▀███████▀       {bcolors.RESET}{bcolors.BRIGHT_YELLOW}    █████████████████████▀      {bcolors.RESET}{bcolors.DARK_GRAY}        ▀██▀  ███████  ▀██▀     {bcolors.RESET}{bcolors.YELLOW}       ████████████████████▀     \n\
    {bcolors.RESET}{logo_color}      ▀▀██▌ ▐█████▄▄ ▀██▀▀         {bcolors.RESET}{bcolors.BRIGHT_YELLOW}                                {bcolors.RESET}{bcolors.DARK_GRAY}               ▀███▀            {bcolors.RESET}{bcolors.YELLOW}      ████████████████████▀      \n\
    \n\
    {bcolors.RESET}{bcolors.WHITE}        1.TITLE SCREEN                    2.FILE EXPLORER                      3.SETTINGS                       4.NOTES\n\
    \n\
    {bcolors.RESET}{bcolors.BRIGHT_GREEN}                                  {bcolors.RESET}{bcolors.RED}         ██████████████              {bcolors.RESET}{bcolors.WHITE}                              {bcolors.RESET}{bcolors.DARK_GRAY}                                \n\
    {bcolors.RESET}{bcolors.BRIGHT_GREEN}        ▄▄███████████▄▄           {bcolors.RESET}{bcolors.RED}       ██████████████████▄           {bcolors.RESET}{bcolors.WHITE}    ║║  ║║  ║║  ║║  ║║        {bcolors.RESET}{bcolors.DARK_GRAY}   ████████████████████████     \n\
    {bcolors.RESET}{bcolors.BRIGHT_GREEN}      ▄█████████▀███████▄         {bcolors.RESET}{bcolors.RED}     ███████▀      ▀██████           {bcolors.RESET}{bcolors.RED}  ██{bcolors.RESET}{bcolors.WHITE}║║{bcolors.RESET}{bcolors.RED}██{bcolors.RESET}{bcolors.WHITE}║║{bcolors.RESET}{bcolors.RED}██{bcolors.RESET}{bcolors.WHITE}║║{bcolors.RESET}{bcolors.RED}██{bcolors.RESET}{bcolors.WHITE}║║{bcolors.RESET}{bcolors.RED}██{bcolors.RESET}{bcolors.WHITE}║║{bcolors.RESET}{bcolors.RED}██      {bcolors.RESET}{bcolors.DARK_GRAY}   █{bcolors.RESET}{bcolors.BLACK}██████████████████████{bcolors.RESET}{bcolors.DARK_GRAY}█       \n\
    {bcolors.RESET}{bcolors.BRIGHT_GREEN}     ████████████ ███████▄        {bcolors.RESET}{bcolors.BRIGHT_YELLOW}    ██{bcolors.RESET}{bcolors.RED}████                          {bcolors.RESET}{bcolors.RED}   ██████████████████████      {bcolors.RESET}{bcolors.DARK_GRAY}   █{bcolors.RESET}{bcolors.BLACK}█{bcolors.RESET}{bcolors.DARK_GRAY}█████{bcolors.RESET}{bcolors.BLACK}████████████████{bcolors.RESET}{bcolors.DARK_GRAY}█       \n\
    {bcolors.RESET}{bcolors.BRIGHT_GREEN}    █████████  ███ ███████        {bcolors.RESET}{bcolors.BRIGHT_YELLOW}   ██████       {bcolors.RESET}{bcolors.BRIGHT_BLUE}▄▄▄▄▄▄▄▄▄▄▄▄▄       {bcolors.RESET}{bcolors.WHITE}   ███████▀▀█▀▀█▀▀█▀▀█▀▀█      {bcolors.RESET}{bcolors.DARK_GRAY}   █{bcolors.RESET}{bcolors.BLACK}██████████████████████{bcolors.RESET}{bcolors.DARK_GRAY}█     \n\
    {bcolors.RESET}{bcolors.BRIGHT_GREEN}    ██████████████ ███████        {bcolors.RESET}{bcolors.BRIGHT_YELLOW}   █████        {bcolors.RESET}{bcolors.BRIGHT_BLUE}██████████████      {bcolors.RESET}{bcolors.WHITE}   ██████████████████████      {bcolors.RESET}{bcolors.DARK_GRAY}   █{bcolors.RESET}{bcolors.BLACK}██████████████████████{bcolors.RESET}{bcolors.DARK_GRAY}█     \n\
    {bcolors.RESET}{bcolors.BRIGHT_GREEN}    █████████  ██ ████████        {bcolors.RESET}{bcolors.BRIGHT_YELLOW}   ██████       {bcolors.RESET}{bcolors.BRIGHT_BLUE}▀████████████       {bcolors.RESET}{bcolors.WHITE}   █▀▀█▀▀█▀▀█▀▀█▀▀█▀▀█▀▀█      {bcolors.RESET}{bcolors.DARK_GRAY}   █{bcolors.RESET}{bcolors.BLACK}██████████████████████{bcolors.RESET}{bcolors.DARK_GRAY}█     \n\
    {bcolors.RESET}{bcolors.BRIGHT_GREEN}     ███████████▄████████▀        {bcolors.RESET}{bcolors.BRIGHT_YELLOW}    ████{bcolors.RESET}{bcolors.GREEN}██             {bcolors.RESET}{bcolors.BRIGHT_BLUE}██████       {bcolors.RESET}{bcolors.WHITE}   ██████████████████████      {bcolors.RESET}{bcolors.DARK_GRAY}   █{bcolors.RESET}{bcolors.BLACK}██████████████████████{bcolors.RESET}{bcolors.DARK_GRAY}█      \n\
    {bcolors.RESET}{bcolors.BRIGHT_GREEN}      █████████████████▀          {bcolors.RESET}{bcolors.BRIGHT_YELLOW}    ▀{bcolors.RESET}{bcolors.GREEN}███████▄      ▄█{bcolors.RESET}{bcolors.BRIGHT_BLUE}██████         {bcolors.RESET}{bcolors.WHITE}   █▀▀█▀▀█▀▀█▀▀█▀▀█▀▀████      {bcolors.RESET}{bcolors.DARK_GRAY}   █{bcolors.RESET}{bcolors.BLACK}██████████████████████{bcolors.RESET}{bcolors.DARK_GRAY}█      \n\
    {bcolors.RESET}{bcolors.BRIGHT_GREEN}     ████▀▀█████████▀▀            {bcolors.RESET}{bcolors.GREEN}       ██████████████████{bcolors.RESET}{bcolors.BRIGHT_BLUE}█          {bcolors.RESET}{bcolors.WHITE}   ██████████████████████      {bcolors.RESET}{bcolors.DARK_GRAY}   █{bcolors.RESET}{bcolors.BLACK}██████████████████████{bcolors.RESET}{bcolors.DARK_GRAY}█       \n\
    {bcolors.RESET}{bcolors.BRIGHT_GREEN}    ██▀▀                          {bcolors.RESET}{bcolors.GREEN}           ███████████              {bcolors.RESET}{bcolors.WHITE}   ██████████████████████      {bcolors.RESET}{bcolors.DARK_GRAY}   ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀       \n\
    \n\
    {bcolors.RESET}{bcolors.WHITE}          5.CHATRUM                       6.GOOGLE SEARCH                      7.CALENDAR                    8.COMMAND LINE\n\
    \n\
    ")
    elif homepage==2:
        print(f"{bcolors.RESET}\n\n\n\n\
    {bcolors.RESET}{bcolors.WHITE}      ████████████  ███    ███████{bcolors.RESET}        \n\
    {bcolors.RESET}{bcolors.WHITE}     ██       ██   ██ ██   ██    ██{bcolors.RESET}       \n\
    {bcolors.RESET}{bcolors.WHITE}      ██████  ██  ██   ██  ███████{bcolors.RESET}        \n\
    {bcolors.RESET}{bcolors.WHITE}           ██ ██ █████████ ██    ██{bcolors.RESET}       \n\
    {bcolors.RESET}{bcolors.WHITE} ███████████  ██ ██     ██ ██     ██████{bcolors.RESET}  \n\
    {bcolors.RESET}{bcolors.WHITE}                                          {bcolors.RESET}\n\
    {bcolors.RESET}{bcolors.WHITE} ██  ██  ██   ███    ███████    ████████{bcolors.RESET}  \n\
    {bcolors.RESET}{bcolors.WHITE} ██  ██  ██  ██ ██   ██    ██  ██    {bcolors.RESET}     \n\
    {bcolors.RESET}{bcolors.WHITE} ██ ████ ██ ██   ██  ███████    ██████{bcolors.RESET}    \n\
    {bcolors.RESET}{bcolors.WHITE}  ███  ███ █████████ ██    ██        ██{bcolors.RESET}   \n\
    {bcolors.RESET}{bcolors.WHITE}   ██  ██  ██     ██ ██     ██████████{bcolors.RESET}    \n\
    \n\
    {bcolors.RESET}{bcolors.WHITE}             1.STAR WARS \n\
    \n\
    ")
    while 1:
        selected=filternumbersandmainkeys([*['H','B','S','E'],('P' if homepage>1 else None),('N' if homepage<max_homepage else None),('V' if events_key else None)])
        if selected.isnumeric():
            return(list_home[homepage-1][int(selected)-1], homepage)
        elif selected=="H": return("home",1)
        elif selected in navigation_dict : return(navigation_dict[selected],homepage)
        elif selected=="B": return("title", homepage)
        elif selected=="P": return("home",homepage-1)
        elif selected=="N": return("home",homepage+1)

events_key=False
def bar(UI=True, escape=False, homepages=False, no_events=False, change=False):
    global currentpage,query,events_key
    if change==True:
        bartext=(SAVE_POSITION+SET_POSITION_ZERO)
    else:
        os.system("cls")
        #BACKGROUND COLOR
        os.system('color '+list_settings[0][2]+'f')
        bartext=""

    #show info
    bartext+=f"{bcolors.RESET}\u018A\u0131\u0298\u054F\n{barcolor}    "+deformat_date(datetime.date.today().strftime("%d/%m/%Y"))+" "+datetime.datetime.now().strftime("%H:%M")
    db=sqlite3.connect(dios_location_path+'.dios_database')
    cursor=db.cursor()
    cursor.execute("""SELECT id FROM dates WHERE date='"""+datetime.date.today().strftime("%d/%m/%Y")+"""'""")
    dates=cursor.fetchall()
    cursor.close()
    db.commit()
    db.close()
    if UI:
        bartext+=f" - [H]ome - [B]ack - [S]ettings - [E]xit diOS"
        if escape: bartext+=f" - [ESC] : Cancel"
        if homepages: bartext+=f" - [P]revious page - [N]ext page"
        events_key=False
        if dates and no_events==False:
            events_key=True
            if "RED" in list_settings[1][2].upper(): notification_color=f"{bcolors.BRIGHT_BLUE}"
            else: notification_color=f"{bcolors.BRIGHT_RED}"
            bartext+=" - [V]iew your ("+notification_color+str(len(dates))+f"{barcolor}) Event{'s' if len(dates)>1 else ''} Today"
    print(bartext.center(columns)+bcolors.RESET)
    
    print("\u2501"*os.get_terminal_size()[0]+f"{color}") #separator (COMMENT THIS LINE OUT IF YOU WANT TO RUN IN YOU IDE, OTHERWISE YOU'LL NEED TO OPEN IN TERMINAL)
    if change==True: print(LOAD_POSITION)

#setting initial page
currentpage="title"
homepage=1
navigation_dict={"H":"home","S":"set","E":"exit","V":"events"}

while 1:
    #page 1
    if currentpage=="title": currentpage=title(changecolor(list_settings[9][2]))
    elif currentpage.startswith("home"): currentpage,homepage=home(changecolor(list_settings[9][2]),homepage)
    elif currentpage=="dir": currentpage=directories(path)
    elif currentpage=="set": currentpage=settings()
    elif currentpage=="chat": currentpage=chatrum()
    elif currentpage=="google": currentpage=google_search()
    elif currentpage=="calendar": currentpage,month,year=calendar(month,year,cursor)
    elif currentpage=="events": currentpage=show_events(datetime.date.today().strftime("%d/%m/%Y"))
    elif currentpage=="notes": currentpage=notes()
    elif currentpage=="cmd": currentpage=cmd()
    #page 2
    elif currentpage=="starwars": currentpage=starwars()
    elif currentpage=="exit":
        os.system('color')
        exit()

#calculator
#snake
#tetris
# configparser
# systeme de pages comme le programme créé pour la CGT
# recentrer le titre en prenant les charactères ansi en compte
# animation de chargement du logo comme en mode aperture science en surprintant
