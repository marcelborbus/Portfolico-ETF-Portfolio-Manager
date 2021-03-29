# portfoliomanager
## Installation
in python 3.7 oder 3.8:

pip install -r requirements.txt

python main.py

## Theoretische Erklärung
Erstmal versuchen wir dem Nutzer eine Kombination an gewichteten ETFs vorzuschlagen, welche seinen Wünschen möglichst nahe kommt, 
sprich die Auswahl wird noch nicht auf Rendite, Volatilität usw. optimisiert. Sprich: "Damit deine angegebene Länderverteilung möglichst gut 
in deinem Portfolio repräsentiert wird, könntest du dieses Portfolio in erwägung ziehen".

Für dieses Optimisierungsproblem lässt sich ein Quadratisches Programm (QP). Drückt man die Länderanteile 
als Vektoren aus und gewichtet sie mit einer Variable zwischen 0 und 1, dann kann man sagen, dass der Abstand zwischen den gewichteten ETFs 
und einem Ziel-ETF minimal sein sollte. Wenn man dies dann aufgeställt hat kann man dies einen Optimizer lösen lassen. Wir benutzen CPLEX von IBM.
Meines Wissens nach löst CPLEX das Modell mit Branch and Bound Algorithmen, aber das ist für uns erstmal irellevant und deshalb habe ich mich damit auch noch 
nicht auseinandergesetzt.

Quadratisches Programm:
https://drive.google.com/file/d/1_RIRFqNB4Cg9X4gSXmcwkPqj4f_FBSiL/view?usp=sharing

Gesucht sind die gewichte w, welche zusammen 1 ergeben sollen. Unter dieser Bedingung versucht man die ETF-Vektoren v so 
zu gewichten, dass der Abstand zwischen den gewichteten ETFs w*v und dem Präferenzenvektor t möglichst minimal ist.

Da wir die Anzahl der ETFs erstmal auf 10 begrenzen wollten, ist w = 0 oder zwischen 0,1 und 1. Um genau zu sein 
ist das Optimisierungsproblem nicht rein quadratisch, sondern ein gemischt-ganzzahliges quadratisches Programm (MIQP). Da sich MIQP 
einfach mit CPLEX modellieren lassen, haben wir uns für diesen Optimizer entschieden.
