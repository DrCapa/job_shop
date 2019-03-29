# Maschinenbelegungsplan
Wir betrachten einen Produktionsprozess bestehend aus den Maschinen A, B und C. Weiterhin sind einige Aufträge mit zugehörigen Teilaufgaben gegeben. 
Jeder Auftrag ist bestimmt durch die Merkmale Teilauftrag (Task), Maschine (machine) und die Dauer (time). Zum Beispiel Auftrag 1:

|Task|Machine|Time|
|:---:|:---:|:---:|
| 1 | A | 3 |
| 2 | B | 2 |
| 3 | C | 2 |

Ziel ist die Minimierung der Produktionsdauer aller Aufträge unter einer Vielzahl von Nebenbedingungen. Diese sind zum Beispiel:
* eine Machine kann immer nur einen Teilauftrag gleichzeitig ausführen, 
* ein begonnener Teilauftrag muss beendet werden,
* die Reihenfolge der Teilauftrage muss eingehalten werden,
* ein Teilauftrag kann erst gestartet werden, wenn der vorangegangene Teilauftrag bereits beendet ist.

Das Programm ermöglicht es, Aufträge in der gegeben Struktur zu definieren, im Ordner Jobs abzuspeichern und erzeugt daraus ein Gantt-Diagramm der Ergebnisse.
