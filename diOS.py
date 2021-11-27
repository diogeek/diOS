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
    color=bcolors.WHITE
    list_settings=[
        ["Background Color",["Black","Blue","Green","Aqua","Red","Purple","Yellow","White","Grey","Light Blue","Light Green","Cyan","Light Red","Light Purple","Light Yellow","Bright White"],"0"],
        ["Info Bar Color",["Purple","Blue","Cyan","Green","Yellow","Red","White","Bold","Underline"],"WHITE"],
        ["Text Color",["Purple","Blue","Cyan","Green","Yellow","Red","White","Bold","Underline"],"WHITE"],
        ["Sorting Files",["By Name","By Type","By Creation Date","Non-Hidden Files First"],"BY_NAME"],
        ["Show Hidden Files",["Yes","No"],"YES"],
        ["Type to Show",["Files Only","Directories Only","Both"],"BOTH"]
         ]
    return(path,barcolor,color,list_settings)

path,barcolor,color,list_settings=reset()

if not check_installed('keyboard'):
    install('keyboard')

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
    global barcolor,color,list_settings
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
            elif int(selected)-1==len(list_settings):
                save()
        elif selected=="H" or selected=="B":
            return("home")
        elif selected=="F":
            return("dir")
        elif selected=="C":
            return("chat")
        elif selected=="E":
            os.system('color')
            exit()

def sort_by_creation_date(dirpath):
    a = [s for s in os.listdir(dirpath)]
    a.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
    return a

def folder_is_hidden(filepath):
    import stat
    return bool(os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)

def listdir_nohidden(path):
    return([f for f in os.listdir(path) if not folder_is_hidden(path+f)])

def sort_by_type(liste):
    listefinal=[f for f in liste if os.path.isfile(path+f)]
    listefinal.append(" ")
    listefinal+=[d for d in liste if os.path.isdir(path+d)]
    return(listefinal)
    
def non_hidden_first(liste):
    listefinal=[f for f in liste if not folder_is_hidden(path+f)]
    listefinal.append(" ")
    listefinal+=[f for f in liste if folder_is_hidden(path+f)]
    return(listefinal)

def directories(path):
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
            liste=[f for f in liste if os.path.isfile(path+f)]
        elif list_settings[5][2]=="DIRECTORIES_ONLY":
            liste=[d for d in liste if os.path.isdir(path+d)]
        #show files
        print((" "*(spaces-1))+"0. Switch Drive\n")
        print(list_settings[3][2])
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
            elif int(selected)-1<len(os.listdir(path)) and int(selected)>0:
                selected=os.listdir(path)[int(selected)-1]
                if os.path.isdir(path+selected):
                    path+=selected+"\\"
                elif os.path.isfile(path+selected):
                    webbrowser.open(path+selected)
        elif selected=="H":
            return("home")
        elif selected=="S":
            return("set")
        elif selected=="B":
            if path.count("\\")>1:
                path=path.rsplit('\\',2)[0]+str("\\")
            else:
                return("home")
        elif selected=="C":
            return("chat")
        elif selected=="E":
            os.system('color')
            exit()

list_chatrum=["Host a Chatrum Server","Join a Chatrum Server"]
       
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
        elif selected=="F":
            return("dir")
        elif selected=="E":
            os.system('color')
            exit()

def home():
    #home page, with colored icons
    while 1:
        list_home=["title","dir","set","chat"]
        bar()
        print("\n\n\n\n\
    "+f"{bcolors.CYAN}"+"        ,   ,,,,,,,, ,,            "+f"{bcolors.BLUE}"+"                                "+f"{bcolors.PURPLE}"+"               ,@@@@@,           \n\
    "+f"{bcolors.CYAN}"+"     ,,,,,,,,  ,,,,,  ,,,,         "+f"{bcolors.BLUE}"+"    *//////*                    "+f"{bcolors.PURPLE}"+"       @@@,,, (@@@@@@@  ,@@@@,   \n\
    "+f"{bcolors.CYAN}"+"   ,,,,,,,,        ,, ,,,,,,       "+f"{bcolors.BLUE}"+"    /,,,,,,,,,,,,,,,,,,,,,.     "+f"{bcolors.PURPLE}"+"     @@@@@@@@@@@@@@@@@@@@@@@@@@/ \n\
    "+f"{bcolors.CYAN}"+"     ,,,,             ,,,,  ,      "+f"{bcolors.BLUE}"+"    //////////////////////.     "+f"{bcolors.PURPLE}"+"      *@@@@@@@@@@@@( @@@@@@@@@@@ \n\
    "+f"{bcolors.CYAN}"+" ,,,,,,                ,, ,,,      "+f"{bcolors.BLUE}"+"    //////////////////////.     "+f"{bcolors.PURPLE}"+"      .@@@@@@@         @@@@@@@   \n\
    "+f"{bcolors.CYAN}"+" ,,,,,                   ,,,,,     "+f"{bcolors.BLUE}"+"    //////////////////////.     "+f"{bcolors.PURPLE}"+"        &@@@@          @@@@@*    \n\
    "+f"{bcolors.CYAN}"+" ,,, .,,               ,,,,,,      "+f"{bcolors.BLUE}"+"    //////////////////////.     "+f"{bcolors.PURPLE}"+"      #@@@@@@@         @@@@@@@,  \n\
    "+f"{bcolors.CYAN}"+"    ,,,,             ,,,           "+f"{bcolors.BLUE}"+"    //////////////////////.     "+f"{bcolors.PURPLE}"+"    %@@@@@@@@@@@@@@@@@@@@@@@@@@@ \n\
    "+f"{bcolors.CYAN}"+"   ,,,,,, ,,     .,,,,,,,,,        "+f"{bcolors.BLUE}"+"    //////////////////////.     "+f"{bcolors.PURPLE}"+"     *@@@@@@@@@@@@@@@@@@@@@@@@@/ \n\
    "+f"{bcolors.CYAN}"+"     ,,,, ,,,,,,  ,,,,,,,,         "+f"{bcolors.BLUE}"+"    ,/////////////////////      "+f"{bcolors.PURPLE}"+"       '@@@@' .@@@@@@@'  @@@@'   \n\
    "+f"{bcolors.CYAN}"+"        ,, ,,,,,,,,.               "+f"{bcolors.BLUE}"+"                                "+f"{bcolors.PURPLE}"+"               '@@@@@'           \n\
    \n\
    "+f"{bcolors.WHITE}"+"       1.TITLE SCREEN                      2.FILE SYSTEM                       3.SETTINGS           \n\
    \n\
    "+f"{bcolors.GREEN}"+"                              \n\
    "+f"{bcolors.GREEN}"+"         @@@@@@@@@@@@@        \n\
    "+f"{bcolors.GREEN}"+"      @@@@@@@@@@@@@@@@@@/     \n\
    "+f"{bcolors.GREEN}"+"    .@@@@@@@@@@@@@@@@@@@@@    \n\
    "+f"{bcolors.GREEN}"+"    @@@@@@@@@@@@@@@@@@@@@@@   \n\
    "+f"{bcolors.GREEN}"+"    @@@@@@@@@@@@@@@@@@@@@@@   \n\
    "+f"{bcolors.GREEN}"+"    @@@@@@@@@@@@@@@@@@@@@@@   \n\
    "+f"{bcolors.GREEN}"+"     @@@@@@@@@@@@@@@@@@@@@    \n\
    "+f"{bcolors.GREEN}"+"      @@@@@@@@@@@@@@@@@@      \n\
    "+f"{bcolors.GREEN}"+"     @@@@*@@@@@@@@@@*         \n\
    "+f"{bcolors.GREEN}"+"    @@                        \n\
    \n\
    "+f"{bcolors.WHITE}"+"          4.CHATRUM           \n\
    ")
        selected=str(input("\n    ")).upper()
        if selected.isnumeric():
            return(list_home[int(selected)-1])
        elif selected=="B":
            return("title")
        elif selected=="S":
            return("set")
        elif selected=="F":
            return("dir")
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
          " - [H]ome - [B]ack - [S]ettings - [F]ile System - [C]hatrum - [E]xit diOS"+
          f"{bcolors.WHITE}")
    
    #separator (COMMENT THIS LINE OUT IF YOU WANT TO RUN IN YOU IDE, OTHERWISE YOU'LL NEED TO OPEN IN TERMINAL)
    print("_"*os.get_terminal_size()[0]+f"{color}") 

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

