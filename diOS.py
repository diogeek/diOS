import os,datetime,webbrowser,sys,subprocess,platform,string

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
    WHITE = '\033[0m'
    BLACK = '\u001b[30m'
    BRIGHT_PURPLE = '\u001b[35;1m'
    BRIGHT_BLUE = '\u001b[34;1m'
    BRIGHT_CYAN = '\u001b[36;1m'
    BRIGHT_GREEN = '\u001b[32;1m'
    BRIGHT_YELLOW = '\u001b[33;1m'
    BRIGHT_RED = '\u001b[31;1m'
    BRIGHT_WHITE = '\u001b[37;1m'
    BRIGHT_BLACK = '\u001b[30;1m'
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
    elif color=="WHITE":
        return bcolors.WHITE
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
    elif color=="BRIGHT_WHITE":
        return bcolors.BRIGHT_WHITE
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
type_to_show='+str(list_settings[5][2])+'')
    settings_file.close()
    
#initial settings setup

def reset():
    path="C:\\"
    barcolor=bcolors.WHITE
    barbackcolor=bcolors.BACKGROUND_BLACK
    color=bcolors.WHITE
    textbackcolor=bcolors.BACKGROUND_BLACK
    list_settings=[
        ["Console Background Color",["Black","Blue","Green","Aqua","Red","Purple","Yellow","White","Grey","Light Blue","Light Green","Cyan","Light Red","Light Purple","Light Yellow","Bright White"],"0"],
        ["Info Bar Style",["Purple","Blue","Cyan","Green","Yellow","Red","White","Black","Bright Purple","Bright Blue","Bright Cyan","Bright Green","Bright Yellow","Bright Red","Bright White","Bright Black","Background Purple","Background Blue","Background Cyan","Background Green","Background Yellow","Background Red","Background White","Background Black","Background Bright Purple","Background Bright Blue","Background Bright Cyan","Background Bright Green","Background Bright Yellow","Background Bright Red","Background Bright White","Background Bright Black","Bold","Italic","Underline"],"WHITE"],
        ["UI Style",["Purple","Blue","Cyan","Green","Yellow","Red","White","Black","Bright Purple","Bright Blue","Bright Cyan","Bright Green","Bright Yellow","Bright Red","Bright White","Bright Black","Background Purple","Background Blue","Background Cyan","Background Green","Background Yellow","Background Red","Background White","Background Black","Background Bright Purple","Background Bright Blue","Background Bright Cyan","Background Bright Green","Background Bright Yellow","Background Bright Red","Background Bright White","Background Bright Black","Bold","Italic","Underline"],"WHITE"],
        ["Sorting Files",["By Name","By Type","By Creation Date","Non-Hidden Files First"],"BY_NAME"],
        ["Show Hidden Files",["Yes","No"],"YES"],
        ["Type to Show",["Files Only","Directories Only","Both"],"BOTH"]
         ]
    return(path,barcolor,color,list_settings)

path,barcolor,color,list_settings=reset()

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
        list_settings[line][2]=settings_lines[line].split("=",1)[-1].replace('\n','')
    os.system('color '+list_settings[0][2]+'f')
    barcolor=changecolor(list_settings[1][2])
    color=changecolor(list_settings[2][2])
    settings_file.close()
else:
    settings_file=open('dios_settings.txt','w')
    settings_file.write('background_color=0\n\
barcolor=WHITE\n\
color=WHITE\n\
sorting=BY_NAME\n\
show_hidden=YES\n\
type_to_show=BOTH')
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
"+" "*((cols//2)-shift)+"        @@@  @@@            "+f"{bcolors.CYAN}"+".,,,,,,,,,,,,, ."+f"{bcolors.WHITE}"+"                                    \n\
"+" "*((cols//2)-shift)+"   @@@@@@@  ' .       "+f"{bcolors.CYAN}"+",,,,,,   ,,,,,,,,,,  ,,,,"+f"{bcolors.WHITE}"+"                                 \n\
"+" "*((cols//2)-shift)+" .@@  /@@  @@@     "+f"{bcolors.CYAN}"+",,,,,,,,,,,,    ,,,,,,, ,,,,,,"+f"{bcolors.WHITE}"+",                              \n\
"+" "*((cols//2)-shift)+" @@   @@  @@@    "+f"{bcolors.CYAN}"+",,,,,,,,,,,,,,,,     ,,,,  ,,,,,,,*"+f"{bcolors.WHITE}"+"                            \n\
"+" "*((cols//2)-shift)+"@@#  @@* (@@    "+f"{bcolors.CYAN}"+",,,,                        ,,,,,,,,"+f"{bcolors.WHITE}"+"                            \n\
"+" "*((cols//2)-shift)+" @@@@@@  @@       "+f"{bcolors.CYAN}"+",,,,,,,                    ,,,,,  ,,"+f"{bcolors.WHITE}"+"     @@@@@@@@@@@@@@@@@@@@,\n\
"+" "*((cols//2)-shift)+"              "+f"{bcolors.CYAN}"+",,,,,,,,,                      ,,,.  ,,,,"+f"{bcolors.WHITE}"+"   @@@@@@@@@@@@@@@@@@@@@ \n\
"+" "*((cols//2)-shift)+"              "+f"{bcolors.CYAN}"+",,,,,,,,                        ,  ,,,,,,"+f"{bcolors.WHITE}"+"  @@@@@@@@               \n\
"+" "*((cols//2)-shift)+"              "+f"{bcolors.CYAN}"+",,,,,,  ,                        ,,,,,,,,"+f"{bcolors.WHITE}"+"  @@@@@@@                \n\
"+" "*((cols//2)-shift)+"              "+f"{bcolors.CYAN}"+",,,,,  ,,,                      ,,,,,,,,,"+f"{bcolors.WHITE}"+" /@@@@@@@************    \n\
"+" "*((cols//2)-shift)+"              "+f"{bcolors.CYAN}"+".,,  ,,,,,                    ,,,,,,,,,,"+f"{bcolors.WHITE}"+"  @@@@@@@@@@@@@@@@@@@@@.  \n\
"+" "*((cols//2)-shift)+"                 "+f"{bcolors.CYAN}"+"*,,,,,,                            ,"+f"{bcolors.WHITE}"+"    (@@@@@@@@@@@@@@@@@@@   \n\
"+" "*((cols//2)-shift)+"                 "+f"{bcolors.CYAN}"+",,,,,,,,  ,,/         /,,,,,,,,,,,,"+f"{bcolors.WHITE}"+"                  #@@@@@@   \n\
"+" "*((cols//2)-shift)+"                  "+f"{bcolors.CYAN}"+",,,,,,,  ,,,,,,   .,,,,,,,,,,,,,"+f"{bcolors.WHITE}"+"                    @@@@@@    \n\
"+" "*((cols//2)-shift)+"                     "+f"{bcolors.CYAN}"+",,,,,  ,,,,,,,,,   ,,,,,,,,"+f"{bcolors.WHITE}"+"      .@@@@@@@@@@@@@@@@@@@@@    \n\
"+" "*((cols//2)-shift)+"                        "+f"{bcolors.CYAN}"+",,  ,,,,,,,,,,,,    ."+f"{bcolors.WHITE}"+"         @@@@@@@@@@@@@@@@@@@@@     \n\
"+" "*((cols//2)-shift)+"                               "+f"{bcolors.CYAN}"+",,,,,,."+f"{bcolors.WHITE}"+"                @@@@@@@@@@@@@@@@@@@       \n\
"+"\n"*(rows-((rows//2)+1)-10)+"\
"+" "*((cols//2)-7)+"PRESS ENTER")
    return("home")
    

def settings():
    global barcolor,color,list_settings,query
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
                path,barcolor,color,list_settings=reset()
                save()
                bar()
                return("set")
            elif int(selected)-1<len(list_settings) and int(selected)>=0:
                bar()
                ii=1
                spaces=len(str(len(list_settings)))
                choice=int(selected)-1
                #choice = which setting you're changing
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
                elif selected=="H":
                    return("home")
                elif selected=="B":
                    return("set")
                elif selected=="E":
                    os.system('color')
                    exit()
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
                bar()
                ii=1
                spaces=len(str(len(available_drives)))
                for drive in available_drives:
                    print((" "*(spaces-len(str(ii))))+str(ii)+". "+str(drive))
                    ii+=1
                selected=str(input(f"\n    ")).upper()
                if int(selected)-1<len(available_drives) and int(selected)>0:
                    path=available_drives[int(selected)-1]+'\\'
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

list_chatrum=["Host a Local Chatrum Server","Join a Local Chatrum Server"]
       
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
            if selected=="1":
                webbrowser.open('chatrum\server.py')
            webbrowser.open('chatrum\client.py')
            webbrowser.open('chatrum\client_recv.py')
            input()
            return("home")
        elif selected=="H" or selected=="B":
            return("home")
        elif selected=="S":
            return("set")
        elif selected=="E":
            os.system('color')
            exit()

def show_results(query,page):
    import googlesearch
    ii=1
    liste=[]
    for results in googlesearch.search(query, tld='com', lang='en', tbs="0", safe='off', num=10, start=(page-1)*10-1, stop=10, pause=2.0, country='', extra_params=None, user_agent=None, verify_ssl=True):
        print((" "*(2-len(str(ii))))+str(ii)+". "+str(results))
        ii+=1
        liste.append(results)
    return(liste)

google_page=1
query=""

def google_search():
    while 1:
        global google_page,query
        while query=="":
            bar()
            print("Search Google:")
            query =str(input("\n    "))
            google_page=1
        bar()
        print("Results For \""+query+"\" On https://google.com/en/ :\n")
        liste=show_results(query,google_page)
        if google_page>1:
            print("\nPage : "+str(google_page)+" - [P]revious Page - [N]ext Page\n")
        else:
            print("\n[N]ext Page\n")
        selected=str(input("\n    ")).upper()
        if selected.isnumeric():
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

def create_event(date):
    import sqlite3
    db=sqlite3.connect('dios_events.db')
    cursor=db.cursor()
    cursor.execute("""
CREATE TABLE IF NOT EXISTS dates(
     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
     date TEXT,
)
""")
    db.commit()
    db.close()

def calendar(month,year):
    from math import floor
    list_months=["January","February","March","April","May","June","July","August","September","October","November","December"]
    list_weekdays=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
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
        list_choices=["Change Month","Change Year"]
        
        #show calendar
        print(f"\n    {bcolors.BRIGHT_RED}\u250F"+"\u2501"*41+"\u2513\n\
    \u2503 "+f"{bcolors.RESET}"+str(list_months[month-1])+" ("+str(month)+")"+" "*(40-len(str(list_months[month-1])+" ("+str(month)+")"+" "+str(year)))+str(year)+" "+f"{bcolors.BRIGHT_RED}"+"\u2503\n\
    \u2521"+("\u2501"*5+"\u252F")*6+"\u2501"*5+"\u2529"+f"{bcolors.RESET}"+"\n\
    \u2502"+week)
        next_month=month+1
        next_year=year
        if month==12:
            next_month=1
            next_year=year+1
        days_in_month=[i for i in range(day_count,(datetime.date(next_year, next_month, 1) - datetime.date(year, month, 1)).days+1)]
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
                while selected>12 or selected<1:
                    try :
                        selected=int(input("\n    "))
                    except ValueError:
                        print("\nEnter A Numeric Value Between 1 And 12.")
                        time.sleep(1.5)
                        return("calendar",month,year)
                return("calendar",selected,year)
            elif selected==2:
                selected=0
                print("Enter Year:")
                while selected<1 or selected>9999:
                    try:
                        selected=int(input("\n    "))
                    except ValueError :
                        print("\nEnter A Numeric Value Between 1 and 9999.")
                        time.sleep(1.5)
                        return("calendar",month,year)
                return("calendar",month,selected)
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
        print(f"{bcolors.RESET}"+"\n\n\n\n\
    "+f"{bcolors.CYAN}"+"        #.  #######, ##            "+f"{bcolors.BRIGHT_YELLOW}"+"                                "+f"{bcolors.PURPLE}"+"               ,@@@@@,           \n\
    "+f"{bcolors.CYAN}"+"     ######,   (####  ####         "+f"{bcolors.BRIGHT_YELLOW}"+"    *//////*                    "+f"{bcolors.PURPLE}"+"       @@@,,, (@@@@@@@  ,@@@@,   \n\
    "+f"{bcolors.CYAN}"+"   #########       ## ######       "+f"{bcolors.BRIGHT_YELLOW}"+"    /,,,,,,,,,,,,,,,,,,,,,.     "+f"{bcolors.PURPLE}"+"     @@@@@@@@@@@@@@@@@@@@@@@@@@/ \n\
    "+f"{bcolors.CYAN}"+"      ,,               ###  ,      "+f"{bcolors.BRIGHT_YELLOW}"+"    //////////////////////.     "+f"{bcolors.PURPLE}"+"      *@@@@@@@@@@@@( @@@@@@@@@@@ \n\
    "+f"{bcolors.CYAN}"+" #######               #'  ###     "+f"{bcolors.BRIGHT_YELLOW}"+"    //////////////////////.     "+f"{bcolors.PURPLE}"+"      .@@@@@@@         @@@@@@@   \n\
    "+f"{bcolors.CYAN}"+" ####                    #####     "+f"{bcolors.BRIGHT_YELLOW}"+"    //////////////////////.     "+f"{bcolors.PURPLE}"+"        &@@@@          @@@@@*    \n\
    "+f"{bcolors.CYAN}"+" ##   ##                ######     "+f"{bcolors.BRIGHT_YELLOW}"+"    //////////////////////.     "+f"{bcolors.PURPLE}"+"      #@@@@@@@         @@@@@@@,  \n\
    "+f"{bcolors.CYAN}"+"    ####              #.,,         "+f"{bcolors.BRIGHT_YELLOW}"+"    //////////////////////.     "+f"{bcolors.PURPLE}"+"    %@@@@@@@@@@@@@@@@@@@@@@@@@@@ \n\
    "+f"{bcolors.CYAN}"+"   #####  #          .######       "+f"{bcolors.BRIGHT_YELLOW}"+"    //////////////////////.     "+f"{bcolors.PURPLE}"+"     *@@@@@@@@@@@@@@@@@@@@@@@@@/ \n\
    "+f"{bcolors.CYAN}"+"    ##### #####    #######(        "+f"{bcolors.BRIGHT_YELLOW}"+"    ,/////////////////////      "+f"{bcolors.PURPLE}"+"       '@@@@' .@@@@@@@'  @@@@'   \n\
    "+f"{bcolors.CYAN}"+"       ##  #######.  ###           "+f"{bcolors.BRIGHT_YELLOW}"+"                                "+f"{bcolors.PURPLE}"+"               '@@@@@'           \n\
    \n\
    "+f"{bcolors.WHITE}"+"       1.TITLE SCREEN                      2.FILE SYSTEM                       3.SETTINGS           \n\
    \n\
    "+f"{bcolors.GREEN}"+"                                  "+f"{bcolors.RED}"+"          ,(((((((((((                 "                                                           +f"{bcolors.RED}"+"                              \n\
    "+f"{bcolors.GREEN}"+"         @@@@@@@@@@@@@            "+f"{bcolors.RED}"+"       ((((((((((((((((((           "                                                              +f"{bcolors.RED}"+"        *###       (##        \n\
    "+f"{bcolors.GREEN}"+"      @@@@@@@@@@@@@@@@@@/         "+f"{bcolors.RED}"+"     ((((((((       ((/             "                                                              +f"{bcolors.RED}"+"     #(#*############# ###    \n\
    "+f"{bcolors.GREEN}"+"    .@@@@@@@@@@@@@@@@@@@@@        "+f"{bcolors.BRIGHT_YELLOW}"+"    //"+f"{bcolors.RED}"+"((((                          "                                +f"{bcolors.RED}"+"     ##(##(##########(####    \n\
    "+f"{bcolors.GREEN}"+"    @@@@@@@@@@@@@@@@@@@@@@@       "+f"{bcolors.BRIGHT_YELLOW}"+"   //////       "+f"{bcolors.BRIGHT_BLUE}"+",************       "                      +f"{bcolors.WHITE}"+"     #######  ###  ##(  ##    \n\
    "+f"{bcolors.GREEN}"+"    @@@@@@@@@@@@@@@@@@@@@@@       "+f"{bcolors.BRIGHT_YELLOW}"+"   /////        "+f"{bcolors.BRIGHT_BLUE}"+"*/////////////      "                      +f"{bcolors.WHITE}"+"     #######  ###  (##  ##    \n\
    "+f"{bcolors.GREEN}"+"    @@@@@@@@@@@@@@@@@@@@@@@       "+f"{bcolors.BRIGHT_YELLOW}"+"   //////       "+f"{bcolors.BRIGHT_BLUE}"+"*////////////       "                      +f"{bcolors.WHITE}"+"     #*  ###  ###  ###  ##    \n\
    "+f"{bcolors.GREEN}"+"     @@@@@@@@@@@@@@@@@@@@@        "+f"{bcolors.BRIGHT_YELLOW}"+"    /"+f"{bcolors.GREEN}"+"#####             "+f"{bcolors.BRIGHT_BLUE}"+"//////       "+f"{bcolors.WHITE}"+"     #####################    \n\
    "+f"{bcolors.GREEN}"+"      @@@@@@@@@@@@@@@@@@          "+f"{bcolors.GREEN}"+"    ########,      ##"+f"{bcolors.BRIGHT_BLUE}"+"//////         "                              +f"{bcolors.WHITE}"+"     #*  ###  ###  #######    \n\
    "+f"{bcolors.GREEN}"+"     @@@@*@@@@@@@@@@*             "+f"{bcolors.GREEN}"+"       ##################"+f"{bcolors.BRIGHT_BLUE}"+"/          "                              +f"{bcolors.WHITE}"+"     ####################(    \n\
    "+f"{bcolors.GREEN}"+"    @@                            "+f"{bcolors.GREEN}"+"           ###########              "                                                          +f"{bcolors.WHITE}"+"                              \n\
    \n\
    "+f"{bcolors.WHITE}"+"          4.CHATRUM                       5.GOOGLE SEARCH              "                                                                          +"         6.CALENDAR\n\
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

def bar():
    global currentpage,query
    os.system("cls")
    #BACKGROUND COLOR
    os.system('color '+list_settings[0][2]+'f')
    
    #show info
    if currentpage=="google" and query=="":
        print(f"{bcolors.RESET}\u018A\u0131\u0298\u054F"+f"\n{barcolor}    "+datetime.date.today().strftime("%d/%m/%Y")+
          " "+datetime.datetime.now().strftime("%H:%M")+
          f"{bcolors.RESET}")
    else:
        print(f"{bcolors.RESET}\u018A\u0131\u0298\u054F"+f"\n{barcolor}    "+datetime.date.today().strftime("%d/%m/%Y")+
          " "+datetime.datetime.now().strftime("%H:%M")+
          " - [H]ome - [B]ack - [S]ettings - [E]xit diOS"+
          f"{bcolors.RESET}")
    
    #separator (COMMENT THIS LINE OUT IF YOU WANT TO RUN IN YOU IDE, OTHERWISE YOU'LL NEED TO OPEN IN TERMINAL)
    print("\u2501"*os.get_terminal_size()[0]+f"{color}")

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

#calendar
#calculator
#snake
#tetris
