# # CCLogMeOut
**[German Only]** CCLogMeOut ist ein Bot für die Zeiterfassung von ComCave. Dieser Bot loggt dich auf der webseite ein und stempelt dich ein oder aus je nach deinem letzten Status.

Der Bot nutzt die Libary [Selenium](https://pypi.org/project/selenium/)

Bitte vor der nutzung die `login.txt` konfigurieren. Die Datei muss folgendes Format verwenden (Zeile):
| Zeile | Erklärung | Beispiel | 
|--|--|--|
| 1 | Nutzername von CC | MeinNutzername123 |
| 2 | Passwort von CC | SehrSicheresPasswort |
| 3 | Uhrzeit, wenn der Bot die Aufgabe um 14:15 durchführen soll | 1415 |
| 4 | Autoshutdown, fährt PC automatisch herunter true oder false | false |
