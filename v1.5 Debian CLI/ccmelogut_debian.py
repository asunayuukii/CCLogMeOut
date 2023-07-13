#! /usr/bin/python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time, os, datetime, pathlib, sys, random, threading, urllib.request

global controller
global thread

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

    def run(self, value:str) -> bool:
        selenium_hub_url = "http://localhost:4444/wd/hub"
        htmlunit_capabilities = DesiredCapabilities.HTMLUNITWITHJS.copy()

        browser = webdriver.Remote(command_executor = selenium_hub_url, desired_capabilities = htmlunit_capabilities)

        browser.get('https://portal.cc-student.com/index.php?cmd=kug')

        usrinput = browser.find_element(By.NAME, 'login_username')
        usrinput.send_keys(self.ccname)
        time.sleep(random.randint(3,6))

        pswinput = browser.find_element(By.NAME, 'login_passwort')
        pswinput.send_keys(self.ccpasswort)
        time.sleep(random.randint(3,6))

        pswinput.send_keys(Keys.ENTER)

        time.sleep(random.randint(3,6))

        zeiterfassung = browser.find_element(By.LINK_TEXT, 'Zeiterfassung')
        zeiterfassung.click()

        gehenbtn = browser.find_element(By.NAME, 'kommengehenbutton')

        if gehenbtn.get_attribute('value').lower() != value.lower():
            return False

        time.sleep(random.randint(3,6))
        gehenbtn.click()
        time.sleep(random.randint(3,6))
        browser.quit()
        return True

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
            if self.stop: return True
            time.sleep(20)
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
            if controller.stop == False:
                print('\nThread: Anmeldung wird ausgeführt...\n')
                try:
                    controller.run('kommen')
                    tstamp = datetime.datetime.now()
                    print('\nThread: Erfolg. Eingeloggt am ' + str(tstamp.strftime('%d.%m.%Y um %H:%M:%S')) + '\n')
                except:
                    print('\nThread: Fehler.\n')
        controller.istime(controller.stoptime)
        if controller.stop == False:
            print('\nThread: Abmeldung wird ausgeführt...\n')
            try:
                controller.run('gehen')
                tstamp = datetime.datetime.now()
                print('\nThread: Erfolg. Ausgeloggt am ' + str(tstamp.strftime('%d.%m.%Y um %H:%M:%S')) + '\n')
            except:
                print('\nThread: Fehler.\n')
        controller.is_run = False

controller:cc_controller = None
event = threading.Event()
thread = threading.Thread(target=worker, daemon=True, args=(event,))
    
if __name__ == '__main__':
    start = datetime.time(hour=8,minute=0)
    stop = datetime.time(hour=18,minute=0)
    controller = cc_controller(
        ccname='Name', 
        ccpasswort='Password', 
        login=True, 
        starttime=start,
        stoptime=stop, 
        random=5,
        stop= False,
        firefox=False, 
        headless=False, 
        shutdown=False, 
        debug=False
    )
    thread.start()
    if controller.test() == False: # Kriege beim Testen noch ein error obwohl alles funktioniert
        print('test failed')
        exit()
    nowdate = datetime.datetime.now()
    starttime = datetime.datetime.combine(nowdate,controller.starttime)
    stoptime = datetime.datetime.combine(nowdate,controller.stoptime)
    if nowdate > starttime: starttime = starttime + datetime.timedelta(days=1)
    if nowdate > stoptime: stoptime = stoptime + datetime.timedelta(days=1)
    a = 'Username: ' + controller.ccname + '\nPasswort: ' + controller.ccpasswort + '\nProgramm start um ' + str(starttime.strftime('%d/%m/%Y, %H:%M:%S')[:-3]) + ' Uhr. Logout um ' + str(stoptime.strftime('%d/%m/%Y, %H:%M:%S')[:-3]) + '\n'
    print('------------ CCLogMeOut ------------\n\n' + a + '\n\nStart / Stop / Exit\n')
    
    while 1:
        a = input()
        while a.lower() not in {'start', 'stop', 'exit', 'quit'}:
            a = input('Befehl unbekannt. Start / Stop / Exit\n')

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
