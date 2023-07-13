from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
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

    def run(self, value) -> bool:
        browser = None
        
        if self.firefox:
            if self.headless:
                op = webdriver.FirefoxOptions()
                op.headless = True
                browser = webdriver.Firefox(options=op)
            else: browser = webdriver.Firefox()
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
            browser = None
        
            if self.firefox:
                if self.headless:
                    op = webdriver.FirefoxOptions()
                    op.headless = True
                    browser = webdriver.Firefox(options=op)
                else: browser = webdriver.Firefox()
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
    
if __name__ == '__main__':
    exit()
