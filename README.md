
L16_ElectionsScraper.py
-------------------------------------------------------------------------------------------------------------------------------

před spustěním skriptu je potřeba nainstalovat Beautiful Soup

pip install beautifulsoup4

-------------------------------------------------------------------------------------------------------------------------------

vyhledávač výsledků voleb "L16_ElectionsScraper.py" pracuje se dvěma argumenty:
1) název územního celku, seznam viz dole (např: 'Český Krumlov', 'Karlovy Vary', 'Ostrava-město' ......)
2) cesta = adresář, kam má zapisovat výsledky voleb.
jméno souboru si vytvoří sám na základě názevu územního celku 

vyhledávač výsledkůje možné spouštět:
1) z příkazové řádky
2) z vývojového prostředí (PyCharm .....)


priklad zadani z příkazové řádky (u víceslovných názvů územních celků musejí být názvy ohraničeny úvozovkami:
       python L16_ElectionsScraper.py "Český Krumlov" D:\PythonScripts\EngetoAcademy\Project3_election
	   
při spousteni z vyvojoveho prostredi je potreba tyto dva argumenty zadat jako "default" hodnoty do bloků "try" ověřujících validitu vstupů,
 a to do "except" pod-bloků v hlavní části programu (pod "if __name__ == "__main__":").
 Pokud se nezadá cesta, program zapíše výsledky do aktuálního adresáře ze kterého je program spuštěn "os.getcwd()"
 
  
 
-------------------------------------------------------------------------------------------------------------------------------
 
 Územní celky
 
['Praha']
['Benešov', 'Beroun', 'Kladno', 'Kolín', 'Kutná Hora', 'Mělník', 'Mladá Boleslav', 'Nymburk', 'Praha-východ', 'Praha-západ', 'Příbram', 'Rakovník', 'Zahraničí']
['České Budějovice', 'Český Krumlov', 'Jindřichův Hradec', 'Písek', 'Prachatice', 'Strakonice', 'Tábor']
['Domažlice', 'Klatovy', 'Plzeň-město', 'Plzeň-jih', 'Plzeň-sever', 'Rokycany', 'Tachov']
['Cheb', 'Karlovy Vary', 'Sokolov']
['Děčín', 'Chomutov', 'Litoměřice', 'Louny', 'Most', 'Teplice', 'Ústí nad Labem']
['Česká Lípa', 'Jablonec nad Nisou', 'Liberec', 'Semily']
['Hradec Králové', 'Jičín', 'Náchod', 'Rychnov nad Kněžnou', 'Trutnov']
['Chrudim', 'Pardubice', 'Svitavy', 'Ústí nad Orlicí']
['Havlíčkův Brod', 'Jihlava', 'Pelhřimov', 'Třebíč', 'Žďár nad Sázavou']
['Blansko', 'Brno-město', 'Brno-venkov', 'Břeclav', 'Hodonín', 'Vyškov', 'Znojmo']
['Jeseník', 'Olomouc', 'Prostějov', 'Přerov', 'Šumperk']
['Kroměříž', 'Uherské Hradiště', 'Vsetín', 'Zlín']
['Bruntál', 'Frýdek-Místek', 'Karviná', 'Nový Jičín', 'Opava', 'Ostrava-město']

-------------------------------------------------------------------------------------------------------------------------------

pip install pipreqs

příkazem pipreqs spustenym v adresari projektu se vygeneruje "requirements.txt"