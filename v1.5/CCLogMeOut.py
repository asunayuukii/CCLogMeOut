import time, os, datetime, pathlib, sys, threading, platform
from cc_controller import cc_controller
from configparser import ConfigParser as config

#Global VARS
global debug
global controller
global thread
global appcd
global data

def getconf(conpath: str) -> config:
    if os.path.isfile(conpath) == False: return 0

    con = config()
    con.read(conpath)

    return con

def checkconf(conf:config) -> bool:
    if conf.has_section('default') == False: return False
    
    if conf.has_option('default', 'CC_Name') == False: return False
    if conf.has_option('default', 'CC_Password') == False: return False

    if len(conf['default']['CC_Name']) <= 3: return False
    if len(conf['default']['CC_Password']) <= 3: return False

    x = conf.get('default', 'Stoptime', fallback='1800')
    if len(x) < 4: return False
    if x[:2].isnumeric() == False: return False
    if x[-2:].isnumeric() == False: return False
    if int(x[:2]) > 23 or int(x[:2]) < 1: return False
    if int(x[-2:]) > 59 or int(x[-2:]) < 0 : return False

    x = conf.get('default', 'Starttime', fallback='1330')
    if len(x) < 4: return False
    if x[:2].isnumeric() == False: return False
    if x[-2:].isnumeric() == False: return False
    if int(x[:2]) > 23 or int(x[:2]) < 1: return False
    if int(x[-2:]) > 59 or int(x[-2:]) < 0 : return False

    if conf.get('default', 'Random', fallback='5').isnumeric() == False: return False
    if int(conf.get('default', 'Random', fallback='5')) > 30: return False
    if int(conf.get('default', 'Random', fallback='5')) < 0: return False

    if conf.get('settings', 'OnlineLOG', fallback='0').isnumeric() == False: return False
    if conf.get('settings', 'OnlineCTRL', fallback='0').isnumeric() == False: return False
    if conf.get('settings', 'OnlineID', fallback='0').isnumeric() == False: return False
    if conf.get('settings', 'LogMeIn', fallback='0').isnumeric() == False: return False
    if conf.get('settings', 'Firefox', fallback='0').isnumeric() == False: return False
    if conf.get('settings', 'NoBrowserWindow', fallback='0').isnumeric() == False: return False
    if conf.get('settings', 'ShutdownAfterStop', fallback='0').isnumeric() == False: return False

    del(x)

    return True

def updateconf(section:str, option:str, value:str) -> bool:
    data.set(section, option, value)

    with open(appcd + '/config.ini', 'w') as configfile:
        data.write(configfile)

def writeconf():
    default = """# Bitte Editiere die Konfigurationsdatei aber entferne keine Angaben
# 0 == OFF und 1 == ON
# Uhrzeit kann so geschrieben werden 17:00 oder 1700
# Random == Zufällige Uhrzeit ankommen und gehen in Minuten

[default]
CC_Name = NAME
CC_Password = PASSWORD
Starttime = 13:30
Stoptime = 18:30
Random = 5

[settings]
OnlineLOG = 1
OnlineCTRL = 1
OnlineID = 0
LogMeIn = 1
Firefox = 1
NoBrowserWindow = 1
shutdownAfterStop = 0"""
    
    f = open(appcd + "/config.ini", "w")
    f.write(default)
    f.close()

def worker(e:threading.Event):
    print('Thread: gestartet.')
    while 1:
        time.sleep(0.5)
        e.wait()
        controller.is_run = True
        nowdate = datetime.datetime.now()
        starttime = datetime.datetime.combine(nowdate,controller.starttime)
        stoptime = datetime.datetime.combine(nowdate,controller.stoptime)
        if nowdate > starttime: starttime = starttime + datetime.timedelta(days=1)
        if nowdate > stoptime: stoptime = stoptime + datetime.timedelta(days=1)
        a = 'Programm start am ' + str(starttime.strftime('%d.%m.%Y, um %H:%M:%S')[:-3]) + ' Uhr. Logout um ' + str(stoptime.strftime('%H:%M:%S')[:-3]) + ' Uhr\n'
        print(a)
        if controller.login:
            controller.istime(controller.starttime)
            if controller.stop == False:
                print('Thread: Anmeldung wird ausgeführt...\n')
                try:
                    controller.run('kommen')
                    tstamp = datetime.datetime.now()
                    print('Thread: Erfolg. Eingeloggt am ' + str(tstamp.strftime('%d.%m.%Y um %H:%M:%S')) + '\n')
                except:
                    print('Thread: Fehler.\n')
        controller.istime(controller.stoptime)
        if controller.stop == False:
            print('\nThread: Abmeldung wird ausgeführt...\n')
            try:
                controller.run('gehen')
                tstamp = datetime.datetime.now()
                print('Thread: Erfolg. Ausgeloggt am ' + str(tstamp.strftime('%d.%m.%Y um %H:%M:%S')) + '\n')
            except:
                print('Thread: Fehler.\n')
        if controller.shutdown and controller.stop == False:
            e.clear()
            os.system('shutdown /s /t 300')
            print('Thread: Shutdown Befehl hinzugefügt für in 5 Minuten\nThread: ACHTUNG zum Abbrechen in der cmd schreiben -> shutdown /a\n')
        controller.is_run = False


# ASSIGN GLOBAL VARS
debug = False
controller:cc_controller = None
event = threading.Event()
thread = threading.Thread(target=worker, daemon=True, args=(event,))
appcd = None
data = None

if getattr(sys, 'frozen', False):
    appcd = os.path.dirname(sys.executable)
elif __file__:
    appcd = os.path.dirname(__file__)
else:
    appcd = str(pathlib.Path(__file__).parent.resolve())
    
if str(os.getcwd()) != appcd:
    os.chdir(appcd)

if os.path.exists(appcd + '/debug.true'):
    debug = True

if __name__ == '__main__':
    data = getconf(appcd + '/config.ini')

    if data == 0:
        writeconf()
        data = getconf(appcd + '/config.ini')
        if data == 0:
            print('ERNO:404_CONF')
            exit()
        a = input('Config wurde erstellt.\nBitte gebe dein Loginnamen vom CCPortal ein:\n')
        while a == '' or len(a) < 4 or a == None:
            if a.lower() == 'exit': exit()
            a = input('Nutzername war zu kurz oder fehlte komplett. Bitte versuche es erneut.\n')
        updateconf('default', 'CC_Name', a)
        a = input('\nBitte gebe nun dein Passwort vom CCPortal ein:\n')
        while a == '' or len(a) < 4 or a == None:
            if a.lower() == 'exit': exit()
            a = input('Passwort war zu kurz oder fehlte komplett. Bitte versuche es erneut.\n')
        updateconf('default', 'CC_Password', a)
        print('Config erstellt und Daten eingetragen')

    if checkconf(data) == False:
        print('ERNO:400_CONF')
        exit()
    
    controller = cc_controller(
        ccname=data['default']['CC_Name'], 
        ccpasswort=data['default']['CC_Password'], 
        login=bool(int(data.get('settings', 'LogMeIn', fallback=1))), 
        starttime=datetime.time(hour=int(data.get('default', 'Starttime', fallback='1345')[:2]), minute=int(data.get('default', 'Starttime', fallback='1345')[-2:])),
        stoptime=datetime.time(hour=int(data.get('default', 'Stoptime', fallback='1830')[:2]), minute=int(data.get('default', 'Stoptime', fallback='1830')[-2:])), 
        random=int(data.get('default', 'Random', fallback='5')),
        stop=False,
        firefox=bool(int(data.get('settings', 'Firefox', fallback=1))), 
        headless=bool(int(data.get('settings', 'NoBrowserWindow', fallback=1))), 
        shutdown=bool(int(data.get('settings', 'ShutdownAfterStop', fallback=1))), 
        debug=debug
    )

    thread.start()
    
    print('Selftest läuft...')

    r = controller.test()
    if r == False:
        print('ERNO:500_SELFTEST')
        exit()

    if platform.system() == 'Windows': os.system('cls')
    if platform.system() == 'Linux': os.system('clear')

    print('--------------- CCLogMeOut ---------------\n\n1) Start\n2) Stop\n3) Config erneut laden\n4) Config anzeigen\n5) Login/Logout Now\n6) Clear\n7) Selftest\n\n9) Beenden\n')
    if controller.stop == False and event.is_set():
        nowdate = datetime.datetime.now()
        starttime = datetime.datetime.combine(nowdate,controller.starttime)
        stoptime = datetime.datetime.combine(nowdate,controller.stoptime)
        if nowdate > starttime: starttime = starttime + datetime.timedelta(days=1)
        if nowdate > stoptime: stoptime = stoptime + datetime.timedelta(days=1)
        a = 'Username: ' + controller.ccname + '\nPasswort: ' + controller.ccpasswort + '\nProgramm start am ' + str(starttime.strftime('%d.%m.%Y, um %H:%M:%S')[:-3]) + ' Uhr. Logout um ' + str(stoptime.strftime('%H:%M:%S')[:-3]) + ' Uhr\n'
        print('CCLogMeOut ist gestartet.\n\n' + a)
    else: print('CCLogMeOut nicht gestartet.\n')
        
    while 1:
        if thread.is_alive() == False:
            print('ERNO:500_THREADISDEAD')
            exit()

        a = input('> ')
        while a.lower() not in {'1','2','3','4','5','9','exit','start','stop','quit','clear','show','config','reload','7','6','selftest', 'self', 'test','login','logout', 'now'}:
            print('Eingabe konnte nicht validiert werden.')
            a = input('> ')

        if a.lower() in {'9','exit','quit'}:
            if controller.is_run:
                controller.stop = True
                event.clear()
                print('CCLogMeOut wird gestoppt...')
                while controller.is_run: time.sleep(0.5)
                controller.stop = False
                print('CCLogMeOut wurde erfolgreich beendet.\n')
            print('Bye...')
            exit()

        if a.lower() in {'1','start'}:
            if controller.is_run == False and event.is_set() == False and thread.is_alive():
                event.set()
                time.sleep(5)
                if controller.is_run: 
                    print('CCLogMeOut gestartet.\n')
            else: print('CCLogMeout bereits gestartet...\n')

        if a.lower() in {'2','stop'}:
            if controller.is_run:
                controller.stop = True
                event.clear()
                print('CCLogMeOut wird gestoppt...')
                while controller.is_run: time.sleep(0.5)
                controller.stop = False
                print('CCLogMeOut wurde beendet.\n')
            else: print('CCLogMeOut ist bereits gestoppt.\n')

        if a.lower() in {'3','reload','config'}:
            if controller.is_run:
                controller.stop = True
                event.clear()
                print('CCLogMeOut wird gestoppt...')
                while controller.is_run: time.sleep(0.5)
                controller.stop = False
                print('CCLogMeOut wurde beendet.\n')

            data = getconf(appcd + '/config.ini')
            if data == 0:
                print('ERNO:404_CONF Config konnte nicht gefunden werden.\n')
            elif checkconf(data) == False:
                print('ERNO:400_CONF Config hatte ein Format fehler.\n')
            else:
                controller = cc_controller(
                    ccname=data['default']['CC_Name'], 
                    ccpasswort=data['default']['CC_Password'], 
                    login=bool(int(data.get('settings', 'LogMeIn', fallback=1))), 
                    starttime=datetime.time(hour=int(data.get('default', 'Starttime', fallback='1345')[:2]), minute=int(data.get('default', 'Starttime', fallback='1345')[-2:])),
                    stoptime=datetime.time(hour=int(data.get('default', 'Stoptime', fallback='1830')[:2]), minute=int(data.get('default', 'Stoptime', fallback='1830')[-2:])), 
                    random=int(data.get('default', 'Random', fallback='5')),
                    stop=False,
                    firefox=bool(int(data.get('settings', 'Firefox', fallback=1))), 
                    headless=bool(int(data.get('settings', 'NoBrowserWindow', fallback=1))), 
                    shutdown=bool(int(data.get('settings', 'ShutdownAfterStop', fallback=1))), 
                    debug=debug
                )
                print('Config neugeladen. CCLogMeOut ist nicht gestartet...\n')

        if a.lower() in {'4','show'}:
            nowdate = datetime.datetime.now()
            starttime = datetime.datetime.combine(nowdate, controller.starttime)
            stoptime = datetime.datetime.combine(nowdate, controller.stoptime)
            if nowdate > starttime: starttime = starttime + datetime.timedelta(days=1)
            if nowdate > stoptime: stoptime = stoptime + datetime.timedelta(days=1)
            a = 'Username: ' + controller.ccname
            a += '\nPasswort: ' + controller.ccpasswort
            a += '\nAutomatischer Login: ' + str(controller.login)
            a += '\nFirefox nutzen: ' + str(controller.firefox)
            a += '\nBrowser im Hintergrund ausführen: ' + str(controller.headless)
            a += '\nZufällige Zeit in Minuten +/-: ' + str(controller.random)
            a += '\nProgramm start am ' + str(starttime.strftime('%d.%m.%Y, um %H:%M:%S')[:-3]) + ' Uhr. Logout um ' + str(stoptime.strftime('%H:%M:%S')[:-3]) + ' Uhr'
            a += '\nAutomatischer Shutdown nach Logout: ' + str(controller.shutdown)
            print('Aktuelle Einstellungen:\n' + a + '\n')

        if a.lower() in {'5','login','logout', 'now'}:
            a = input('Schreibe Login oder Logout\nZum Abbrechen: Cancel, Exit, Stop\n> ')
            while a.lower() not in {'login', 'logout', 'exit', 'stop', 'cancel'}:
                a = input('Eingabe konnte nicht validiert werden. Schreibe Login oder Logout\nZum Abbrechen: Cancel, Exit, Stop\n> ')
            
            if a.lower() in {'login', 'logout'}:
                if controller.is_run:
                    controller.stop = True
                    event.clear()
                    print('CCLogMeOut wird gestoppt...')
                    while controller.is_run: time.sleep(0.5)
                    controller.stop = False
                    print('CCLogMeOut wurde beendet.\n')
                
                print('Bitte warten...')
                if a.lower() == 'login': 
                    r = controller.run('kommen')
                    if r: print('Erfolg.\n')
                    else: print('ERROR. Anscheinend warst du schon eingeloggt.\n')
                elif a.lower() == 'logout': 
                    r = controller.run('gehen')
                    if r: print('Erfolg.\n')
                    else: print('ERROR. Anscheinend warst du schon ausgeloggt.\n')

        if a.lower() in {'6','clear'}:
            if platform.system() == 'Windows': os.system('cls')
            if platform.system() == 'Linux': os.system('clear')

            print('--------------- CCLogMeOut ---------------\n\n1) Start\n2) Stop\n3) Config erneut laden\n4) Config anzeigen\n5) Login/Logout Now\n6) Clear\n7) Selftest\n\n9) Beenden\n')
            if controller.stop == False and event.is_set():
                nowdate = datetime.datetime.now()
                starttime = datetime.datetime.combine(nowdate,controller.starttime)
                stoptime = datetime.datetime.combine(nowdate,controller.stoptime)
                if nowdate > starttime: starttime = starttime + datetime.timedelta(days=1)
                if nowdate > stoptime: stoptime = stoptime + datetime.timedelta(days=1)
                a = 'Username: ' + controller.ccname + '\nPasswort: ' + controller.ccpasswort + '\nProgramm start am ' + str(starttime.strftime('%d.%m.%Y, um %H:%M:%S')[:-3]) + ' Uhr. Logout um ' + str(stoptime.strftime('%H:%M:%S')[:-3]) + ' Uhr\n'
                print('CCLogMeOut ist gestartet.\n\n' + a)
            else: print('CCLogMeOut nicht gestartet.\n')

        if a.lower() in {'7','selftest', 'self', 'test'}:
            print('Bitte warten... Selbsttest wird ausgeführt.')
            r = controller.test()
            if r: print('Erfolg. Alles funktioniert.\n')
            else: print('ERNO:500_SELFTEST\n')
