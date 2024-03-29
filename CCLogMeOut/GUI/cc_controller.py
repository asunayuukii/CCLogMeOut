from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time, os, datetime, pathlib, sys, random

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

    def run(self, value) -> int:
        browser = None
        if self.firefox:
            if self.headless:
                op = webdriver.FirefoxOptions()
                op.headless = True
                op.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
                browser = webdriver.Firefox(options=op)
            else: 
                op = webdriver.FirefoxOptions()
                op.headless = False
                op.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
                browser = webdriver.Firefox(options=op)
        else:
            if self.headless:
                op = webdriver.ChromeOptions()
                op.add_argument('--headless=new')
                op.add_argument('--log-level=3')
                op.add_experimental_option('excludeSwitches', ['enable-logging'])
                browser = webdriver.Chrome(options=op)
            else:
                op = webdriver.ChromeOptions()
                op.add_argument('--log-level=3')
                op.add_experimental_option('excludeSwitches', ['enable-logging'])
                browser = webdriver.Chrome(options=op)

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
        except NoSuchElementException as e: #LoginError
            if self.debug: print(e)
            browser.quit()
            return -2
        except Exception as e: #Error Unknown
            if self.debug: print(e)
            browser.quit()
            return 0

    def test(self) -> bool:
        try:
            browser = None
        
            if self.firefox:
                if self.headless:
                    op = webdriver.FirefoxOptions()
                    op.headless = True
                    op.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
                    browser = webdriver.Firefox(options=op)
                else: 
                    op = webdriver.FirefoxOptions()
                    op.headless = False
                    op.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
                    browser = webdriver.Firefox(options=op)
            else:
                if self.headless:
                    op = webdriver.ChromeOptions()
                    op.add_argument('--headless=new')
                    op.add_argument('--log-level=3')
                    op.add_experimental_option('excludeSwitches', ['enable-logging'])
                    browser = webdriver.Chrome(options=op)
                else:
                    op = webdriver.ChromeOptions()
                    op.add_argument('--log-level=3')
                    op.add_experimental_option('excludeSwitches', ['enable-logging'])
                    browser = webdriver.Chrome(options=op)
            
            browser.get('https://google.com/')
            browser.quit()
            return True
        except Exception as e:
            if self.debug: print(e)
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
    
if __name__ == '__main__':
    exit()
