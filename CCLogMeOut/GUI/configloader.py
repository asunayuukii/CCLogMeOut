from configparser import ConfigParser as config

import os

class configLoader:
    def __init__(self, conpath:str) -> None:
        self.conpath = conpath
        self.con = self.getconf(conpath)
        self.config = self.initconf()

    def getconf(self, conpath: str) -> config:
        if os.path.isfile(conpath) == False: return 0

        con = config()
        con.read(conpath)

        return con
    
    def checkconf(self, conf:config) -> bool:
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
    
    def updateconf(self, section:str, option:str, value:str):
        self.con.set(section, option, value)

        with open(self.conpath, 'w') as configfile:
            self.con.write(configfile)
    
    def writeconf(self):
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
    
        f = open(self.conpath, "w")
        f.write(default)
        f.close()

    def initconf(self) -> dict:
        if self.con == 0:
            return {
                'result': False,
                'error': 404
            }
        
        if self.checkconf(self.con) == False:
            return {
                'result': False,
                'error': 405
            }

        return {
            'result': True,
            'error': 0,
            'ccname': self.con['default']['CC_Name'],
            'ccpasswort': self.con['default']['CC_Password'],
            'login': bool(int(self.con.get('settings', 'LogMeIn', fallback=1))),
            'starttime': self.con.get('default', 'Starttime', fallback='1345'),
            'stoptime': self.con.get('default', 'Stoptime', fallback='1800'),
            'random': int(self.con.get('default', 'Random', fallback='5')),
            'firefox': bool(int(self.con.get('settings', 'Firefox', fallback=1))),
            'headless': bool(int(self.con.get('settings', 'NoBrowserWindow', fallback=1))),
            'shutdown': bool(int(self.con.get('settings', 'ShutdownAfterStop', fallback=1))),
        }
