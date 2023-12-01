#! /usr/bin/python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
import time, os, datetime, pathlib, sys, random, threading, urllib.request

global controller
global thread

loginname = 'Name'
loginpasswort = 'Passwort'
startt = datetime.time(hour=14,minute=00)
stopt = datetime.time(hour=19,minute=00)
randomtime = 15

class cc_controller():
    def __init__(self, ccname:str, ccpasswort:str, login:bool = False, starttime:datetime = datetime.time(hour=13,minute=30,second=0), stoptime:datetime = datetime.time(hour=18,minute=0,second=0), random:int = 5, stop:bool = False, firefox:bool = False, headless:bool = False, shutdown:bool = False, debug:bool = False):
        self.ccname = ccname
        self.ccpasswort = ccpasswort
        self.login = login
        self.starttime = starttime
        self.stoptime = stoptime
        self.random = random
        self.stop = stop
        self.firefox = firefox
        self.headless = headless
        self.shutdown = shutdown
        self.is_run = False
        self.debug = debug
        self.skip = False

    def run(self, value:str) -> int:
        selenium_hub_url = "http://localhost:4444/wd/hub"
        htmlunit_capabilities = DesiredCapabilities.HTMLUNITWITHJS.copy()
        browser = webdriver.Remote(command_executor = selenium_hub_url, desired_capabilities = htmlunit_capabilities)
        
        try:
            browser.get('https://portal.cc-student.com/index.php?cmd=kug')

            usrinput = browser.find_element(By.NAME, 'login_username')
            usrinput.send_keys(self.ccname)
            time.sleep(random.randint(1,3))

            pswinput = browser.find_element(By.NAME, 'login_passwort')
            pswinput.send_keys(self.ccpasswort)
            time.sleep(random.randint(1,3))

            pswinput.send_keys(Keys.ENTER)
            time.sleep(random.randint(1,3))

            zeiterfassung = browser.find_element(By.LINK_TEXT, '- Zeiterfassung')
            zeiterfassung.click()
            time.sleep(random.randint(2,4))

            dialog = browser.find_element(By.CLASS_NAME, 'buttonShowDialogButton')
            dialog.click()
            time.sleep(random.randint(2,4))
            
            gehenbtn = browser.find_element(By.NAME, 'kommengehenbutton')
            if gehenbtn.get_attribute('value').lower() != value.lower():
                browser.quit()
                return -1 #error already gehen/kommen
            gehenbtn.click()
            time.sleep(random.randint(2,4))

            closebtn = browser.find_element(By.CLASS_NAME, 'ui-dialog-titlebar-close')
            closebtn.click()
            time.sleep(random.randint(2,4))
            browser.quit()
            return 1
        except NoSuchElementException: #LoginError
            browser.quit()
            return -2
        except: #Error Unknown
            browser.quit()
            return 0


    def test(self) -> bool:
        try:
            code = urllib.request.urlopen("http://localhost:4444").getcode()
            if code != 200: return False
            selenium_hub_url = "http://localhost:4444/wd/hub"
            htmlunit_capabilities = DesiredCapabilities.HTMLUNITWITHJS.copy()

            browser = webdriver.Remote(command_executor = selenium_hub_url, desired_capabilities = htmlunit_capabilities)

            browser.get('https://example.org/')
            browser.quit()
            return True
        except Exception as e:
            return False
        except:
            return False
        
    def istime(self, timer:datetime) -> bool:
        nowdate = datetime.datetime.now()
        nextdate = datetime.datetime.combine(nowdate,timer)
        nextdate = nextdate + datetime.timedelta(minutes=random.randint(-self.random,self.random), seconds=random.randint(0,59))
        if nowdate > nextdate: nextdate = nextdate + datetime.timedelta(days=1)
        while nowdate < nextdate:
            if self.stop or self.skip: return True
            time.sleep(random.randint(5,20))
            nowdate = datetime.datetime.now()
        return True
    
def worker(e):
    print('\nThread: gestartet.\n')
    while 1:
        time.sleep(0.5)
        e.wait()
        controller.is_run = True
        if controller.login:
            controller.istime(controller.starttime)
            if controller.stop == False and datetime.datetime.now().weekday() not in {5,6} and controller.skip == False:
                print('\nThread: Anmeldung wird ausgeführt...\n')
                crun = controller.run('kommen')
                cerr = 0
                while (crun == 0 and cerr < 3):
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
        if controller.stop == False and datetime.datetime.now().weekday() not in {5,6} and controller.skip == False:
            print('\nThread: Abmeldung wird ausgeführt...\n')
            crun = controller.run('gehen')
            cerr = 0
            while (crun == -1 and cerr < 3):
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
        controller.is_run = False

controller:cc_controller = None
event = threading.Event()
thread = threading.Thread(target=worker, daemon=True, args=(event,))
    
if __name__ == '__main__':
    controller = cc_controller(
        ccname=loginname, 
        ccpasswort=loginpasswort, 
        login=True, 
        starttime=startt,
        stoptime=stopt, 
        random=randomtime,
        stop= False,
        firefox=False, 
        headless=False, 
        shutdown=False, 
        debug=False
    )
    thread.start()
    if controller.test() == False:
        print('test failed')
        exit()
    nowdate = datetime.datetime.now()
    starttime = datetime.datetime.combine(nowdate,controller.starttime)
    stoptime = datetime.datetime.combine(nowdate,controller.stoptime)
    if nowdate > starttime: starttime = starttime + datetime.timedelta(days=1)
    if nowdate > stoptime: stoptime = stoptime + datetime.timedelta(days=1)
    if controller.login: a = 'Username: ' + controller.ccname + '\nPasswort: ' + controller.ccpasswort + '\nProgramm start am ' + str(starttime.strftime('%d.%m.%Y, um %H:%M:%S')[:-3]) + ' Uhr. Logout um ' + str(stoptime.strftime('%H:%M:%S')[:-3]) + ' Uhr\n'
    else: a = 'Username: ' + controller.ccname + '\nPasswort: ' + controller.ccpasswort + '\nLogout am ' + str(stoptime.strftime('%d.%m.%Y, um %H:%M:%S')[:-3]) + ' Uhr\n'
    print('------------ CCLogMeOut ------------\n\n' + a + '\n\nStart / Stop / Skip / Exit\n')
    
    while 1:
        a = input()
        while a.lower() not in {'start', 'stop', 'skip', 'exit', 'quit'}:
            a = input('Befehl unbekannt. Start / Stop / Skip / Exit\n')

        if a.lower() == 'start':
            if controller.is_run == False and event.is_set() == False and thread.is_alive():
                event.set()
                time.sleep(5)
                if controller.is_run: print('CCLogMeOut gestartet.\n')
            else: print('CCLogMeout bereits gestartet...\n')

        if a.lower() == 'stop':
            if controller.is_run:
                controller.stop = True
                event.clear()
                print('CCLogMeOut wird gestoppt...')
                while controller.is_run: time.sleep(0.5)
                controller.stop = False
                print('CCLogMeOut wurde erfolgreich beendet.\n')
            else:
                print('CCLogMeOut ist bereits gestoppt.\n')

        if a.lower() == 'skip':
            if controller.is_run:
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
        
        if a.lower() == 'exit' or a.lower() == 'quit':
            if controller.is_run:
                controller.stop = True
                event.clear()
                print('CCLogMeOut wird gestoppt...')
                while controller.is_run: time.sleep(0.5)
                controller.stop = False
                print('CCLogMeOut wurde erfolgreich beendet.\n')
            print('Bye...')
            exit()
