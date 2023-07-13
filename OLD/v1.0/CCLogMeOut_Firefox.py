from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time, os, datetime, pathlib, sys

debug = False

def istime(h:int = 13, m:int = 0) -> bool:
    nowdate = datetime.datetime.now()
    nextdate = nowdate.replace(hour=h, minute=m)
    if nowdate > nextdate: nextdate = nextdate + datetime.timedelta(days=1)
    while nowdate < nextdate:
        time.sleep(20)
        nowdate = datetime.datetime.now()
    return True

def getusr(logpath: str) -> tuple:
    if os.path.exists(logpath) == False: return 0
    file = open(logpath)

    cont = None
    with file as f:
        cont = f.read().split()

    file.close()

    if cont[0] == None or cont[1] == None:
        return 0
    
    h = 13
    m = 0
    shutdown = False

    
    if len(cont) >= 3:
        if len(cont[2]) == 2 and cont[2].isnumeric():
            h = int(cont[2])
            if h > 23 or h < 9:
                h = 13
        
        elif len(cont[2]) == 4 and cont[2].isnumeric():
            h = int(str(cont[2])[:2])
            m = int(str(cont[2])[-2:])
            if h > 23 or h < 9:
                h = 13
            if m > 59 or m < 0:
                m = 0

    if len(cont) >= 4: 
        if cont[3] != None and cont[3].lower() == 'true':
            shutdown = True
    
    return (cont[0], cont[1], (h, m), shutdown)


def logout(usr: str, psw: str) -> None:
    browser = webdriver.Firefox()
    browser.get('https://portal.cc-student.com/index.php?cmd=kug')

    usrinput = browser.find_element(By.NAME, 'login_username')
    usrinput.send_keys(usr)
    time.sleep(5)

    pswinput = browser.find_element(By.NAME, 'login_passwort')
    pswinput.send_keys(psw)
    time.sleep(5)

    pswinput.send_keys(Keys.ENTER)

    time.sleep(5)

    # browser.get('https://portal.cc-student.com/index.php?cmd=kug')
    zeiterfassung = browser.find_element(By.LINK_TEXT, 'Zeiterfassung')
    zeiterfassung.click()

    gehenbtn = browser.find_element(By.NAME, 'kommengehenbutton')
    time.sleep(5)
    gehenbtn.click()
    time.sleep(5)
    browser.quit()

def selftest() -> bool:
    try:
        browser = webdriver.Firefox()
        browser.get('https://google.com/')
        browser.quit()
        return True
    except Exception as e: 
        if debug: print('\n' + e + '\n')
        return False

if __name__ == '__main__':
    print('CCLogMeOut - Firefox\n---------------------------\n')

    # Current Directory
    appcd = None

    # Unterscheiden zwischen Script oder EXE
    if getattr(sys, 'frozen', False):
        appcd = os.path.dirname(sys.executable)
    elif __file__:
        appcd = os.path.dirname(__file__)
    else:
        appcd = str(pathlib.Path(__file__).parent.resolve())
    
    # Verhindern das Python in System32 ausgeführt wird.
    if str(os.getcwd()) != appcd:
        os.chdir(appcd)

    if os.path.exists(appcd + '\\debug.true'):
        debug = True
    
    # Text File auslesen in AppCD
    data = getusr(appcd + '\\login.txt')

    print('Selftest gestartet.')
    
    # Selbsttest um das ausführen des Browsers zu gewährleisten
    r = selftest()
    if r == False:
        print('ERROR. Selftest gescheitert.')
        time.sleep(30)
        exit()
    
    print('Selftest erfolgreich.\n')
    
    # Fehler beim Lesen von Loginname und Passwort
    if data == 0:
        print('login.txt nicht gefunden oder keine daten enthalten.')
        time.sleep(30)
        exit()
    
    timer = datetime.time(hour=data[2][0], minute=data[2][1], second=00)
    print('Username: ' + data[0] + '\nPasswort: ' + data[1] + '\nProgramm start um ' + str(timer.strftime('%X')[:-3]) + ' Uhr.\n')
    
    if data[3]:
        print('AutoShutdown aktiviert.\n')
    
    print('Warte auf den richtigen Zeitpunkt...')
    
    # Warten bis Uhrzeit erreicht ist (Nur volle Stunden)
    istime(data[2][0], data[2][1])
    
    print('Starte Logout.')
    
    # Logout Methode wird gestartet
    try:
        logout(data[0], data[1])
        print('Logout erfolgreich\n')
    except Exception as e:
        if debug: print('\n' + e + '\n')
        print('ERROR. Logout konnte nicht erfolgreich beendet werden.\n')
        time.sleep(30)
        exit()

    if data[3]:
        print("AutoShutdown: PC fährt in 5 Minuten herunter.")
        os.system("shutdown /s /t 300")

    time.sleep(30)
   
    exit()
