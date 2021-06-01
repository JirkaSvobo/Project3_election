import requests
import bs4
import sys
import os
import csv


def main(uzemniCelek: str, outputPath: str):
    scraped_link_const = 'https://volby.cz/pls/ps2017nss/'
    scraped_link_suf1 = 'ps3?xjazyk=CZ'

    scraped_link_CZ = f'{scraped_link_const}{scraped_link_suf1}'
    print(scraped_link_CZ)
    if not returnCodeCheck(scraped_link_CZ): quit()
    cislo_UzCelku,scraped_link_suf2 = getIDs_UzCelku(getSoup(scraped_link_CZ),uzemniCelek)
    print(f'Pro uzemni celek {uzemniCelek} je cislo: {cislo_UzCelku}, link je: {scraped_link_suf2}')

    scraped_link_obec = f'{scraped_link_const}{scraped_link_suf2}'
    print(scraped_link_obec)
    if not returnCodeCheck(scraped_link_obec): quit()
    vysledkyVoleb = getDetails_UzCelku(getSoup(scraped_link_obec), scraped_link_const)
#    print(vysledkyVoleb)    # for debugging

    zapisDoSouboru(vysledkyVoleb, outputPath,hledanyCelek)


def returnCodeCheck(scraped_link: str):
    response = requests.get(scraped_link)
    if str(response.status_code)[0] == '2':
        return True
    else:
        print(f'error in URL: {scraped_link}')
        return False


def getSoup(scraped_link: str):
    getr = requests.get(scraped_link)
    return bs4.BeautifulSoup(getr.content, "html.parser", from_encoding = 'utf-8')

def getIDs_UzCelku(soup,uzemniCelek)->tuple:
    selekce_a = soup.findAll('a')
    uzemni_urovne = [int(uroven1.get('name')) for uroven1 in selekce_a if uroven1.get('name') != None]
#    print(uzemni_urovne)     # for debugging

    for i in uzemni_urovne:
        jmenaCelku = getContent(soup, f"t{i}sa1 t{i}sb2", 'text')
#        print(format(jmenaCelku))      # for debugging
        try:
            jmenoCelku_index = jmenaCelku.index(uzemniCelek)
        except ValueError:
            if i == max(uzemni_urovne):
                print(f'Spatne zadane jmeno obce. Obec {uzemniCelek}')
                quit()
        else:
#            print(f'nalezen uzemni celek {uzemniCelek} ve skupine {f"t{i}sa1 t{i}sb2"} na pozici {jmenoCelku_index}')    # for debugging
            cislaCelku = getContent(soup, f"t{i}sa1 t{i}sb1", 'text')
            cisloCelku = cislaCelku[jmenoCelku_index]
            linkyCelku = getContent(soup, f"t{i}sa3", 'a["href"]')
            scraped_link_suf = linkyCelku[jmenoCelku_index]
            return cisloCelku,scraped_link_suf
#            break

def getDetails_UzCelku(soupUz, scraped_link_const)->dict:
    vysledkyDict = dict()
    urovneT = 3
    for j in range(1,urovneT+1):
        jmenaObci = getContent(soupUz, f"t{j}sa1 t{j}sb2", 'text')
        cislaObci = getContent(soupUz, f"t{j}sa1 t{j}sb1", 'text', 'cislo')
        linkObci = getContent(soupUz, f"t{j}sa1 t{j}sb1", 'a["href"]', 'cislo')
        for k, item in enumerate(jmenaObci):
            vysledkyDict[item] = {'jmeno_obce' : item, 'kod_obce' : cislaObci[k], 'link' : linkObci[k]}
    obceLst = list(vysledkyDict.keys())

    for i, obec in enumerate(obceLst):
#        print(f"{obec}: {scraped_link_const}{vysledkyDict[obec]['link']}")    # for debugging
        soupObec = getSoup(f"{scraped_link_const}{vysledkyDict[obec]['link']}")
        volici = getContent(soupObec, "sa2", 'text', 'cislo')
        obalky = getContent(soupObec, "sa3", 'text', 'cislo')
        platneHlasy = getContent(soupObec, "sa6", 'text', 'cislo')
        strany = [*getContent(soupObec, "t1sa1 t1sb2", 'text'), *getContent(soupObec, "t2sa1 t2sb2", 'text')]
        vysledkyDict[obec].update({'volici_v_seznamu': ''.join(c for c in volici[0] if c.isnumeric())})
        vysledkyDict[obec].update({'vydane_obalky': ''.join(c for c in obalky[0] if c.isnumeric())})
        vysledkyDict[obec].update({'platne_hlasy': ''.join(c for c in platneHlasy[0] if c.isnumeric())})
        vysledkyDict[obec].update({'kandidujici_strany': strany})

        vysledkyDict[obec].pop('link')
    return vysledkyDict

def getContent(soup,header,klicHledani,*args)->list:
    if not args:
        hledanyObsah_vTD = soup.findAll('td', {"headers": header})
    elif args[0] == 'cislo':
        hledanyObsah_vTD = soup.findAll('td', {'class':'cislo',"headers": header})
    elif args[0] == 'center':
        hledanyObsah_vTD = soup.findAll('td', {'class':'center',"headers": header})

    if klicHledani == 'text':
        return [item.text for item in hledanyObsah_vTD if item.text != '-']
    elif klicHledani == 'a["href"]':
        return [item.a["href"] for item in hledanyObsah_vTD if item.text != '-']

def zapisDoSouboru(dataDict, outputPath, identif):
    fieldnames = list(dataDict[list(dataDict.keys())[0]].keys())
#    print(fieldnames)    # for debugging
    fileName = f'vysledky_{identif}.csv'
    with open(os.path.join(outputPath,fileName), 'w+', newline='') as file:  # , encoding="utf-8"
        writer = csv.DictWriter(file, fieldnames, delimiter=',')
        writer.writeheader()
        for obec in list(dataDict.keys()):
            writer.writerow(dataDict[obec])
    return writer


if __name__ == "__main__":

    try:
        hledanyCelek = sys.argv[1]
    except:
        print('nesrozumitelny argument pro hledany uzemni celek zadany z radku, pouzije se default')
        hledanyCelek = 'Ostrava-město'  # 'Český Krumlov', 'Karlovy Vary', 'Ostrava-město'

    try:
        os.path.isdir(sys.argv[2])
        outputPath = sys.argv[2]
    except:
        print(f'nesrozumitelny argument pro cestu k zapsani vysledku, pouzije se default {os.getcwd()}')
        outputPath = os.getcwd()

    main(hledanyCelek,outputPath)