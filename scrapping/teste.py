import requests
from bs4 import BeautifulSoup
import json
import os
import time
import re
import unidecode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def normaliza(text):
    text = text.replace(" ","")
    text = text.lower()
    text = unidecode.unidecode(text)
    return text

def myStrip(text):
    return re.sub(r'\s+', ' ', text).strip()

casasDict = {}

def betclic(url,liga):
    #global betclicDict
    
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    
    with open('leagues.json', 'r') as f:
        data = json.load(f)
    
    last_id = int(data['jogos'][-1]['id'])
    
    jogos = soup.find_all("sports-events-event", class_="groupEvents_card")
    for j in jogos:
        obj = {'liga':liga}
        j_soup = BeautifulSoup(str(j), 'html.parser')
        eqs = j_soup.find_all("div",class_="scoreboard_contestantLabel")
        eq1=normaliza(myStrip(eqs[0].text).strip())
        eq2=normaliza(myStrip(eqs[1].text).strip())
        
        if len(eqs) == 2:
            obj['jogo'] = myStrip(eqs[0].text).strip() + "§" + myStrip(eqs[1].text).strip()
        day = myStrip(j_soup.find("div",class_="event_infoTime").text).strip()
        obj['data'] = myStrip(day.split(" ")[0]).strip()

        odds = j_soup.find_all("sports-selections-selection",class_="oddButton")
        for o in odds:
            o_soup = BeautifulSoup(str(o), 'html.parser')
            nome_aposta = normaliza(myStrip(o_soup.find("span",class_="oddMatchName").text).strip())
            odd = myStrip(o_soup.find("span",class_="oddValue").text).strip()
            aposta=""

            if eq1 in nome_aposta or nome_aposta in eq1:
                aposta = "odd1"
            elif eq2 in nome_aposta or nome_aposta in eq2:
                aposta = "odd2"
            elif "empate" in nome_aposta or nome_aposta in "empate":
                aposta = "oddx"
            else:
                print("ERRO: " + nome_aposta+" - "+eq1+" - "+eq2)
            obj[aposta] = odd.replace(',','.')
        obj['local'] = "Sem Informação"
        obj['casa'] = "betclic"
        jogo_existente = False
        for j in data['jogos']:
            if j['jogo'] == obj['jogo'] and j['casa'] == obj['casa']:
                j['odd1'] = obj['odd1']
                j['oddx'] = obj['oddx']
                j['odd2'] = obj['odd2']
                jogo_existente = True
                break
                
        # se o jogo não existir, adiciona-o
        if not jogo_existente:
            last_id += 1
            obj['id'] = str(last_id)
            data['jogos'].append(obj)

    # json dump to file with utf-8 encoding
    with open('leagues.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
def betclic2():
#  ligas = dados["data"]["leaguesList"]
    ligas = ["https://www.betclic.pt/futebol-s1/portugal-primeira-liga-c32", "https://www.betclic.pt/futebol-s1/inglaterra-premier-league-c3",
            "https://www.betclic.pt/futebol-s1/italia-serie-a-c6", "https://www.betclic.pt/futebol-s1/espanha-la-liga-c7"]
        
    for l in ligas:
        if "primeira-liga" in l:
            nomeLiga = "Liga Portuguesa"
        elif "premier-league" in l:
            nomeLiga = "Liga Inglesa"
        elif "serie-a" in l:
            nomeLiga = "Liga Italiana"
        elif "la-liga" in l:
            nomeLiga = "Liga Espanhola"
        betclic(l, nomeLiga)
    
def bet22(url,liga):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)

    # Acesse a URL desejada
    driver.get(url)

    # Aguarde até que o elemento "main-content" seja carregado
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "c-events__team")))

    # Obtenha o HTML da página da web
    html = driver.page_source
    
    # Feche o navegador da web
    driver.quit()   
    
    with open('leagues.json', 'r') as f:
        data = json.load(f)
        
    last_id = int(data['jogos'][-1]['id'])
    
    soup = BeautifulSoup(html, 'html.parser')
    
    jogos = soup.find_all("div", class_="c-events__item c-events__item_col")
    for j in jogos:
        obj = {'liga':liga}
        j_soup = BeautifulSoup(str(j), 'html.parser')
        eqs = j_soup.find_all("span",class_="c-events__team")
            
        if len(eqs) == 2:
            obj['jogo'] = myStrip(eqs[0].text).strip() + "§" + myStrip(eqs[1].text).strip()
        dH = myStrip(j_soup.find("div",class_="c-events__time min").text).strip()
        obj['data'] = myStrip(dH.split(" ")[0]).strip()
        hora = myStrip(dH.split(" ")[1]).strip()
        odds = j_soup.find_all("div",class_="c-bets__bet")
        i = 0
        for o in odds:
            if i > 3:
                continue
            else:
                i+=1
            odd = myStrip(o.text).strip().replace(',','.')
            if i == 1:
                aposta = "odd1"
            elif i == 2:
                aposta = "oddx"
            elif i == 3:
                aposta = "odd2"
            else:
                continue
            obj[aposta] = odd
        obj['local'] = "Sem Informação"
        obj['casa'] = "22bet"
        
        jogo_existente = False
        for j in data['jogos']:
            if j['jogo'] == obj['jogo'] and j['casa'] == obj['casa']:
                j['odd1'] = obj['odd1']
                j['oddx'] = obj['oddx']
                j['odd2'] = obj['odd2']
                jogo_existente = True
                continue
                
        # se o jogo não existir, adiciona-o
        if not jogo_existente:
            last_id += 1
            obj['id'] = str(last_id)
            if "equipadacasa" not in normaliza(obj['jogo']) and "especiais" not in normaliza(obj['jogo']):
                data['jogos'].append(obj)
    
    # json dump to file with utf-8 encoding
    with open('leagues.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def bet222():
#  ligas = dados["data"]["leaguesList"]
    ligas = ["https://22bet-bet.com/pt/line/football/118663-portugal-primeira-liga", "https://22bet-bet.com/pt/line/football/88637-england-premier-league",
            "https://22bet-bet.com/pt/line/football/110163-italy-serie-a", "https://22bet-bet.com/pt/line/football/127733-spain-la-liga"]
        
    for l in ligas:
        if "primeira-liga" in l:
            nomeLiga = "Liga Portuguesa"
        elif "premier-league" in l:
            nomeLiga = "Liga Inglesa"
        elif "serie-a" in l:
            nomeLiga = "Liga Italiana"
        elif "la-liga" in l:
            nomeLiga = "Liga Espanhola"
        bet22(l, nomeLiga)
        
def bwin(url, liga):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)

    # Acesse a URL desejada
    driver.get(url)

    # Aguarde até que o elemento "main-content" seja carregado
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "participant")))

    # Obtenha o HTML da página da web
    html = driver.page_source
    
#    Feche o navegador da web
    driver.quit()   

    with open('leagues.json', 'r') as f:
        data = json.load(f)

    last_id = int(data['jogos'][-1]['id'])
    
    soup = BeautifulSoup(html, 'html.parser')
    
    jogos = soup.find_all("div", class_="grid-event-wrapper")
    for j in jogos:
        obj = {'liga':liga}
        j_soup = BeautifulSoup(str(j), 'html.parser')
        eqs = j_soup.find_all("div",class_="participant-container")
            
        if len(eqs) == 2:
            obj['jogo'] = myStrip(eqs[0].text).strip() + "§" + myStrip(eqs[1].text).strip()

        obj['data'] = myStrip(j_soup.find("ms-event-info",class_="grid-event-info").text).strip()
        odds = j_soup.find_all("div",class_="option-indicator")
        apostas = []
        for o in odds:
            o_soup = BeautifulSoup(str(o), 'html.parser')
            odd = myStrip(o_soup.find("div",class_="option-value").text).strip().replace(',','.')
            apostas.append(odd)
        
        obj['local'] = "Sem Informação"
        obj['casa'] = "bwin"
        
        if len(apostas) >= 3:
            obj['odd1'] = apostas[0]
            obj['oddx'] = apostas[1]
            obj['odd2'] = apostas[2]
            
            jogo_existente = False
            for j in data['jogos']:
                if j['jogo'] == obj['jogo'] and j['casa'] == obj['casa']:
                    j['odd1'] = obj['odd1']
                    j['oddx'] = obj['oddx']
                    j['odd2'] = obj['odd2']
                    jogo_existente = True
                    break
                
            # se o jogo não existir, adiciona-o
            if not jogo_existente:
                last_id += 1
                obj['id'] = str(last_id)
                data['jogos'].append(obj)
    
    # json dump to file with utf-8 encoding
    with open('leagues.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
def bwin2():
    ligas = ["https://sports.bwin.pt/pt/sports/futebol-4/apostar/portugal-37/liga-portugal-bwin-102851", "https://sports.bwin.pt/pt/sports/futebol-4/apostar/inglaterra-14/premier-league-102841",
            "https://sports.bwin.pt/pt/sports/futebol-4/apostar/espanha-28/la-liga-102829", "https://sports.bwin.pt/pt/sports/futebol-4/apostar/it%C3%A1lia-20/serie-a-102846"]
        
    for l in ligas:
        nome = l.split("/")[8]
        if nome == "liga-portugal-bwin-102851":
            nomeLiga = "Liga Portuguesa"
        elif nome == "premier-league-102841":
            nomeLiga = "Liga Inglesa"
        elif nome == "serie-a-102846":
            nomeLiga = "Liga Italiana"
        elif nome == "la-liga-102829":
            nomeLiga = "Liga Espanhola"
        bwin(l, nomeLiga)

def betano(url, liga):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    dados = soup.find_all("body", class_="")[0]
    # get <script> </script> content
    dados = str(dados).split("<script>")[1].split("</script>")[0]
    dados = dados.split("=")[1:]
    dados = "=".join(dados)
    dados = json.loads(dados)
    eventos = dados["data"]["blocks"]
    
    equipas = []
    
    with open('leagues.json', 'r') as f:
        data = json.load(f)

    if len(data['jogos'])==0:
        last_id = 0
    else:
        last_id = int(data['jogos'][-1]['id'])

    
    fileW = open ("leagues.json", "w+")
    
    #Percorrer os diferentes jogos de respetiva liga
    for e in eventos:
        lista_de_jogos = e["events"]
        for j in lista_de_jogos:
            nomeLiga = liga
            if " - " in j["name"] and j["name"].split(" ")[0] != "Série":
                
                eq1 = j["name"].split(" - ")[0]
                eq2 = j["name"].split(" - ")[1]
        
                if not eq1 in equipas:
                    equipas.append(eq1)
                if not eq2 in equipas:
                    equipas.append(eq2)
                
                nomeJogo = j["name"].split(" - ")[0] + "§" + j["name"].split(" - ")[1]
                mercados = j["markets"]
                for m in mercados:
                    if m["name"] == "Resultado Final":
                        selecoes = m["selections"]
                        odd1 = str(selecoes[0]["price"]).replace(',','.')
                        oddx = str(selecoes[1]["price"]).replace(',','.')
                        odd2 = str(selecoes[2]["price"]).replace(',','.')
                
                jogoInfo = {"liga":nomeLiga, "jogo":nomeJogo, "data": "Sem Informações", "local": "Sem Informações", "odd1":odd1, "oddx":oddx, "odd2":odd2, "casa": "Betano"}
                
                jogo_existente = False
                for j in data['jogos']:
                    if j['jogo'] == nomeJogo:
                        j['odd1'] = odd1
                        j['oddx'] = oddx
                        j['odd2'] = odd2
                        jogo_existente = True
                        break
        
            # se o jogo não existir, adiciona-o
                if not jogo_existente:
                    last_id += 1
                    jogoInfo['id'] = str(last_id)
                    data['jogos'].append(jogoInfo)
                
            else :
                pass
    json.dump(data, fileW, indent=4)
    
    ficheiroNomes = open("equipas.txt", "a")
    
    for e in equipas:
        ficheiroNomes.write(e+"\n")

def betano2():
    ligas = ["https://www.betano.pt/sport/futebol/portugal/primeira-liga/17083/", "https://www.betano.pt/sport/futebol/inglaterra/premier-league/1/",
            "https://www.betano.pt/sport/futebol/italia/serie-a/1635/#", "https://www.betano.pt/sport/futebol/espanha/laliga/5/"]
        
    for l in ligas:
        nome = l.split("/")[6]
        if nome == "primeira-liga":
            nomeLiga = "Liga Portuguesa"
        elif nome == "premier-league":
            nomeLiga = "Liga Inglesa"
        elif nome == "serie-a":
            nomeLiga = "Liga Italiana"
        elif nome == "laliga":
            nomeLiga = "Liga Espanhola"
        betano(l, nomeLiga)

if __name__ == "__main__":
    while True:
        betano2()
        bwin2()
        bet222()
        betclic2()
        time.sleep(20)

