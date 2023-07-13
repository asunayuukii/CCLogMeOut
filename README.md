# CCLogMeOut v1.5
![CCLogMeOut](https://i.ibb.co/hDwhfbw/cclogmeout.png)
**[German Only]** CCLogMeOut ist ein Bot für die Zeiterfassung von ComCave. Dieser Bot loggt dich auf der webseite ein und stempelt dich ein oder aus je nach deinem letzten Status.

Der Bot nutzt die Libary [Selenium](https://pypi.org/project/selenium/)

Der Browser muss Installiert sein. Sprich wenn man Chrome verwenden möchte muss Chrome (nicht chromium based Browser like Opera/Edge co) installiert sein

**DOWNLOAD LINK: https://github.com/asunayuukii/CCLogMeOut/releases** 
(auch unter releases zu finden)

## Einstellungen

Bitte vor der nutzung die `config.ini` konfigurieren. Die Datei muss folgendes Format verwenden (Zeile):
| Name| Erklärung | Beispielwert | 
|--|--|--|
| cc_name | Nutzername von CC | MeinNutzername123 |
| cc_password | Passwort von CC | SehrSicheresPasswort |
| starttime | Uhrzeit, wann der Bot dich einloggen soll | 14:15 |
| stoptime | Uhrzeit, wann der Bot dich ausloggen soll | 18:30 |
| random | Zeit in Minuten damit der Bot dich nicht immer Exakt gleiche uhrzeit einloggt/ausloggt | 5 |
| onlinelog | Online Log, wird später hinzugefügt | 0 |
| onlinectrl | Online Steuerung (An/Aus und Uhrzeit einstellen (Keine Login daten können geändert oder eingesehen werden)), wird später hinzugefügt | 0 |
| onlineid | Online ID (Um den Bot im Internet zu Identifizieren), wird später hinzugefügt | 0 |
| logmein | Ob der Bot dich auch einloggen soll, wenn 0 = Aus und 1 = An | 1 |
| firefox | Ob Firefox genutzt werden soll, wenn 0 = Aus und 1 = An | 1 |
| nobrowserwindow | Ob der Browser (Ist ein Seperates Fenster hat kein Effekt auf euren Browser) ausgeblendet wird beim einloggen/ausloggen , wenn 0 = Aus und 1 = An | 1 |
| shutdownafterstop | Fährt den PC nach erfolgreichem ausloggen herrunter (5 minuten später), wenn 0 = Aus und 1 = An | 0 |

# Debian Based OS CLI (Command Line Interface)
Da vielleicht auch der Wunsch besteht das Programm auf einem VServer laufen soll habe Ich das Script ein wenig angepasst.

Getestet auf RaspberryPi 4 64 Bit

**Nutze [Screen](https://wiki.ubuntuusers.de/Screen/) um eine Anwendung im Hintergrund laufen zu lassen.** 

**DOWNLOAD LINK: https://github.com/asunayuukii/CCLogMeOut/releases** 
(auch unter releases zu finden)

## Installations Anleitung:
Niemals als root programme installieren oder ausführen -> https://wiki.ubuntuusers.de/mit_Root-Rechten_arbeiten/ -> https://www.thefastcode.com/de-eur/article/why-you-shouldn-t-log-into-your-linux-system-as-root

| | Befehl |
|--|--|
| 1 | `cd && mkdir cclogmeout` |
| 2a | `nano ccmelogout_debian.py` |
| 2b | Script kopieren und Script einfügen |
| 2c | Zeile 121 NAME, PASSWORT und Uhrzeit ändern |
| 2d | "STRG + X" "y" "ENTER" zum Speichern |
| 3 | `chmod +x ccmelogout_debian.py` |
| 4 | `pip install selenium==3.141.0` |
| 5 | `wget https://github.com/SeleniumHQ/htmlunit-driver/releases/download/2.64.0/htmlunit-driver-2.64.0-jar-with-dependencies.jar` |
| 6 | `mv htmlunit-driver-2.64.0-jar-with-dependencies.jar htmlunit-driver.jar` |
| 7 | `wget https://github.com/SeleniumHQ/selenium/releases/download/selenium-3.141.5/selenium-server-standalone-3.141.5.jar` |
| 8 | `mv selenium-server-standalone-3.141.5.jar selenium-server-standalone.jar` |
| 9a | `nano startscript.sh` |
| 9b | `nohup java -cp selenium-server-standalone.jar:htmlunit-driver.jar org.openqa.grid.selenium.GridLauncherV3 &` |
| 9c | "STRG + X" "y" "ENTER" zum Speichern |
| 10 | `chmod +x startserver.sh` |
| 11 | `./startserver.sh` |
| 12 | `./ccmelogout_debian.py` |

## FAQ - Troubleshooting:

**System aktuell?**
- sudo apt-get update && sudo apt-get upgrade -y >> sudo reboot

**Python installiert?**
- python3 --version >> Python installieren >> sudo apt-get install python3 python3-dev

**pip installiert?**
- pip --version >> pip installieren >> sudo apt-get install python3-pip

**java installiert?**
- java --version >> java installieren >> sudo apt-get install default-jre
