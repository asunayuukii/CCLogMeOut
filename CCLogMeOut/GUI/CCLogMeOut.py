import time, os, datetime, pathlib, sys, threading, platform
from cc_controller import cc_controller
from configloader import configLoader

#Global VARS
global debug
global controller
global thread
global appcd
global data
global out

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
        if controller.login: a = '\nLogin am ' + str(starttime.strftime('%d.%m.%Y, um %H:%M:%S')[:-3]) + ' Uhr. Logout um ' + str(stoptime.strftime('%H:%M:%S')[:-3]) + ' Uhr'
        else: a = '\nLogout am ' + str(stoptime.strftime('%d.%m.%Y, um %H:%M:%S')[:-3]) + ' Uhr'
        print(a)
        if controller.login:
            controller.istime(controller.starttime)
            if controller.stop == False and controller.skip == False:
                print('Thread: Anmeldung wird ausgeführt...\n')
                crun = controller.run('kommen')
                cerr = 0
                while ((crun == 0 or crun == -2) and cerr < 3):
                    cerr -= -1
                    print('Thread: Error. Retry '+ str(cerr) + '/3 ... ')
                    time.sleep(30.0)
                    crun = controller.run('kommen')
                tstamp = datetime.datetime.now()
                if crun == 1: print('Thread: Erfolg. Eingeloggt am ' + str(tstamp.strftime('%d.%m.%Y um %H:%M:%S')) + '\n')
                elif crun == -1: print('Thread: Error. Nutzer war bereits eingeloggt.. Keine Aktion vorgenommen.')
                elif crun == -2: print('Thread: Error. Logindaten wahrscheinlich fehlerhaft.. Keine Aktion vorgenommen.')
                elif crun == 0: print('Thread: Error. Unbekannter ERROR.. Keine Aktion vorgenommen.')
                else: print('Thread: Error. Unbekannter ERROR ohne Errorkey.. Keine Aktion vorgenommen. ')
        controller.skip = False
        controller.istime(controller.stoptime)
        if controller.stop == False and controller.skip == False:
            print('\nThread: Abmeldung wird ausgeführt...\n')
            crun = controller.run('gehen')
            cerr = 0
            while ((crun == 0 or crun == -2) and cerr < 3):
                cerr -= -1
                print('Thread: Error. Retry '+ str(cerr) + '/3 ... ')
                time.sleep(30.0)
                crun = controller.run('gehen')
            tstamp = datetime.datetime.now()
            if crun == 1: print('Thread: Erfolg. Ausgeloggt am ' + str(tstamp.strftime('%d.%m.%Y um %H:%M:%S')) + '\n')
            elif crun == -1: print('Thread: Error. Nutzer war bereits eingeloggt.. Keine Aktion vorgenommen.')
            elif crun == -2: print('Thread: Error. Logindaten wahrscheinlich fehlerhaft.. Keine Aktion vorgenommen.')
            elif crun == 0: print('Thread: Error. Unbekannter ERROR.. Keine Aktion vorgenommen.')
            else: print('Thread: Error. Unbekannter ERROR ohne Errorkey.. Keine Aktion vorgenommen. ')
        controller.skip = False
        if controller.shutdown and controller.stop == False:
            e.clear()
            os.system('shutdown /s /t 300')
            print('Thread: Shutdown Befehl hinzugefügt für in 5 Minuten\nThread: ACHTUNG zum Abbrechen in der cmd schreiben -> shutdown /a\n')
        controller.is_run = False

def start() -> None:
    if controller.is_run == False and event.is_set() == False and thread.is_alive():
        event.set()
        time.sleep(5)
        if controller.is_run: print('CCLogMeOut gestartet.\n')
    else: print('CCLogMeout bereits gestartet...\n')

def stop() -> None:
    if controller.is_run:
        controller.stop = True
        event.clear()
        print('CCLogMeOut wird gestoppt...')
        while controller.is_run: time.sleep(0.5)
        controller.stop = False
        print('CCLogMeOut wurde beendet.\n')
    else: print('CCLogMeOut ist bereits gestoppt.\n')

def reload() -> None:
    newdata = configLoader(appcd + '/config.ini')
    newdata.config
    if newdata.config['result'] == False:
        if newdata.config['error'] == 404:
            print('ERNO:404_CONF Config konnte nicht gefunden werden.\n')
        if newdata.config['error'] == 405:
            print('ERNO:400_CONF Config hatte ein Format fehler.\n')
    else:
        data = newdata
        controller = cc_controller(
        ccname=data.config['ccname'], 
        ccpasswort=data.config['ccpasswort'], 
        login=data.config['login'], 
        starttime=datetime.time(hour=int(data.config['starttime'][:2]), minute=int(data.config['starttime'][-2:])),
        stoptime=datetime.time(hour=int(data.config['stoptime'][:2]), minute=int(data.config['stoptime'][-2:])), 
        random=data.config['random'],
        stop=False,
        firefox=data.config['firefox'], 
        headless=data.config['headless'], 
        shutdown=data.config['shutdown'], 
        debug=debug
        )
        print('Config neugeladen. CCLogMeOut ist nicht gestartet...\n')

def show() -> None:
    pass

def login() -> None:
    pass

def logout() -> None:
    pass

def skip() -> None:
    if controller.is_run == False:
        print('CCLogMeOut ist nicht gestartet.. Skip nicht möglich.\n')
        return
    controller.skip = True
    while controller.skip: time.sleep(0.5)
    nowdate = datetime.datetime.now()
    starttime = datetime.datetime.combine(nowdate,controller.starttime)
    stoptime = datetime.datetime.combine(nowdate,controller.stoptime)
    if nowdate > starttime: starttime = starttime + datetime.timedelta(days=1)
    if nowdate > stoptime: stoptime = stoptime + datetime.timedelta(days=1)
    if controller.login: a = '\nLogin am ' + str(starttime.strftime('%d.%m.%Y, um %H:%M:%S')[:-3]) + ' Uhr. Logout um ' + str(stoptime.strftime('%H:%M:%S')[:-3]) + ' Uhr'
    else: a = '\nLogout am ' + str(stoptime.strftime('%d.%m.%Y, um %H:%M:%S')[:-3]) + ' Uhr'
    print('Login/Logout geskippt...', a, '\n')


# ASSIGN GLOBAL VARS
debug = False
controller:cc_controller = None
event = threading.Event()
thread = threading.Thread(target=worker, daemon=True, args=(event,))
appcd = None
data = None
silent = True

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

if len(sys.argv) > 1:
    for arg in sys.argv:
        if arg.lower() == 'silent': silent = True

if __name__ == '__main__':
    data = configLoader(appcd + '/config.ini')

    if data.config['result'] == False:
        if data.config['error'] == 404:
            data.writeconf()
            data = configLoader(appcd + '/config.ini')
        
        if data.config['result'] == False and data.config['error'] == 404:
            print('ERNO:404_CONF')
            exit()
        
        a = input('Config wurde erstellt.\nBitte gebe dein Loginnamen vom CCPortal ein:\n')
        while a == '' or len(a) < 4 or a == None:
            if a.lower() == 'exit': exit()
            a = input('Nutzername war zu kurz oder fehlte komplett. Bitte versuche es erneut.\n')
        
        data.updateconf('default', 'CC_Name', a)

        a = input('\nBitte gebe nun dein Passwort vom CCPortal ein:\n')
        while a == '' or len(a) < 4 or a == None:
            if a.lower() == 'exit': exit()
            a = input('Passwort war zu kurz oder fehlte komplett. Bitte versuche es erneut.\n')

        data.updateconf('default', 'cc_password', a)
        data.config = data.initconf()

        print('Config erstellt und Daten eingetragen')

    if data.config['error'] == 405:
        print('ERNO:400_CONF')
        input()
    
    controller = cc_controller(
        ccname=data.config['ccname'], 
        ccpasswort=data.config['ccpasswort'], 
        login=data.config['login'], 
        starttime=datetime.time(hour=int(data.config['starttime'][:2]), minute=int(data.config['starttime'][-2:])),
        stoptime=datetime.time(hour=int(data.config['stoptime'][:2]), minute=int(data.config['stoptime'][-2:])), 
        random=data.config['random'],
        stop=False,
        firefox=data.config['firefox'], 
        headless=data.config['headless'], 
        shutdown=data.config['shutdown'], 
        debug=debug
    )

    thread.start()
    
    print('Selftest läuft...')

    if debug == False:
        r = controller.test()
        if r == False:
            print('ERNO:500_SELFTEST')
            input()

    if platform.system() == 'Windows': os.system('cls')
    if platform.system() == 'Linux': os.system('clear')

    print('--------------- CCLogMeOut ---------------\n\n1) Start\n2) Stop\n3) Config erneut laden\n4) Config anzeigen\n5) Login/Logout Now\n6) Clear\n7) Selftest\n8) Skip\n\n9) Beenden\n')
    if controller.stop == False and event.is_set():
        nowdate = datetime.datetime.now()
        starttime = datetime.datetime.combine(nowdate,controller.starttime)
        stoptime = datetime.datetime.combine(nowdate,controller.stoptime)
        if nowdate > starttime: starttime = starttime + datetime.timedelta(days=1)
        if nowdate > stoptime: stoptime = stoptime + datetime.timedelta(days=1)
        if controller.login: a += 'Username: ' + controller.ccname + '\nPasswort: ' + controller.ccpasswort + '\nProgramm start am ' + controller.starttime + ' Uhr. Logout um ' + controller.stoptime + ' Uhr\n'
        else: a += 'Username: ' + controller.ccname + '\nPasswort: ' + controller.ccpasswort + '\nLogout am ' + controller.stoptime + ' Uhr\n'
        print('CCLogMeOut ist gestartet.\n\n' + a)
        
    while 1:
        if thread.is_alive() == False:
            print('ERNO:500_THREADISDEAD')
            input()

        a = input('> ')
        while a.lower() not in {'1','2','3','4','5','9','exit','start','stop','quit','clear','show','config','reload','7','6','selftest', 'self', 'test','login','logout', 'now', '8', 'skip'}:
            print('Eingabe konnte nicht validiert werden.')
            a = input('> ')

        if a.lower() in {'9','exit','quit'}:
            if controller.is_run: stop()
            print('Bye...')
            input()
            exit()

        if a.lower() in {'1','start'}: start()

        if a.lower() in {'2','stop'}: stop()

        if a.lower() in {'3','reload','config'}:
            if controller.is_run: stop()
            reload()

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
            if controller.login: a += '\nLogin am ' + str(starttime.strftime('%d.%m.%Y, um %H:%M:%S')[:-3]) + ' Uhr. Logout um ' + str(stoptime.strftime('%H:%M:%S')[:-3]) + ' Uhr'
            else: a += '\nLogout am ' + str(stoptime.strftime('%d.%m.%Y, um %H:%M:%S')[:-3]) + ' Uhr'
            a += '\nAutomatischer Shutdown nach Logout: ' + str(controller.shutdown)
            print('Aktuelle Einstellungen:\n' + a + '\n')

        if a.lower() in {'5','login','logout', 'now'}:
            if a.lower() not in {'login', 'logout'}:
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
                
                print('\nBitte warten...')
                if a.lower() == 'login': 
                    r = controller.run('kommen')
                    if r == 1: print('Erfolg.\n')
                    elif r == -1: print('ERROR. Anscheinend warst du schon eingeloggt.\n')
                    elif r == -2: print('ERROR. Logindaten wahrscheinlich fehlerhaft.\n')
                    else: ('ERROR. Fehler unbekannt.\n')
                elif a.lower() == 'logout': 
                    r = controller.run('gehen')
                    if r == 1: print('Erfolg.\n')
                    elif r == -1: print('ERROR. Anscheinend warst du schon ausgeloggt.\n')
                    elif r == -2: print('ERROR. Logindaten wahrscheinlich fehlerhaft.\n')
                    else: ('ERROR. Fehler unbekannt.\n')

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
                a = ''
                if controller.login: a += 'Username: ' + controller.ccname + '\nPasswort: ' + controller.ccpasswort + '\nProgramm start am ' + str(starttime.strftime('%d.%m.%Y, um %H:%M:%S')[:-3]) + ' Uhr. Logout um ' + str(stoptime.strftime('%H:%M:%S')[:-3]) + ' Uhr\n'
                else: a += 'Username: ' + controller.ccname + '\nPasswort: ' + controller.ccpasswort + '\nLogout am ' + str(stoptime.strftime('%d.%m.%Y, um %H:%M:%S')[:-3]) + ' Uhr\n'
                print('CCLogMeOut ist gestartet.\n\n' + a)
            else: print('CCLogMeOut nicht gestartet.\n')

        if a.lower() in {'7','selftest', 'self', 'test'}:
            print('Bitte warten... Selbsttest wird ausgeführt.')
            r = controller.test()
            if r: print('Erfolg. Alles funktioniert.\n')
            else: print('ERNO:500_SELFTEST\n')
        
        if a.lower() in {'8','skip'}:
            skip()
