import requests
from bs4 import BeautifulSoup
import json
import os
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def teste():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.betano.pt/sport/futebol/portugal/primeira-liga/17083/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "event__name")))
        content = driver.page_source
        print(content)
        driver.quit()
    except Exception as e:
        print(e)
        return

#teste()


def myStrip(text):
    return re.sub(r'\s+', ' ', text).strip()

casasDict = {}

def betclic(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    odds = []
    teams = []

    for div in soup.find_all('span', class_='oddValue'):
        odd = myStrip(div.text).strip().replace('\n','')
        odds.append(odd)

    for div in soup.find_all('span', class_='oddMatchName'):
        team = myStrip(div.text).strip().replace('\n','')
        teams.append(team)

    for i in range(len(odds)):
        if i in range(len(teams)):
            print(str(i) + ": " + teams[i] + " - " + odds[i])

def betclic2():
    url = 'https://www.betclic.pt/futebol-s1'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    hrefs = []
    for a in soup.find_all('a', href=True):
        if "/futebol-s1/" in a['href']:
            # from a url like https://www.betclic.pt/futebol-s1/inglaterra-premier-league-1/arsenal-vs-chelsea-1 get https://www.betclic.pt/futebol-s1/inglaterra-premier-league-1
            href = a['href'].split('/')
            href = "https://www.betclic.pt/"+href[1]+"/"+href[2]+"/"
            if href not in hrefs:
                hrefs.append(href)
    for href in hrefs:
        print(href)
        betclic(href)

def bet22(url,liga):
    #global bet22Dict
    #response = requests.get(url)
    f = open("bet22.html", "r")
    response = f.read()
    f.close()
    soup = BeautifulSoup(response, 'html.parser')
    bet22Dict = {}
    bet22Dict["bet22"]=[]
    
    jogos = soup.find_all("div", class_="events__item events__item_col")
    for j in jogos:
        obj = {'liga':liga}
        j_soup = BeautifulSoup(str(j), 'html.parser')
        obj['jogo'] = myStrip(j_soup.find("span",class_="events-links__info").text).strip()
        dH = myStrip(j_soup.find("div",class_="events__cell events__cell_row events__cell_time").text).strip()
        obj['data'] = myStrip(dH.split(" ")[0]).strip()
        hora = myStrip(dH.split(" ")[1]).strip()
        odds = j_soup.find_all("div",class_="coef coef__num")
        for o in odds:
            o_soup = BeautifulSoup(str(o), 'html.parser')
            nome_aposta = myStrip(o_soup.find("div",class_="coef__name").text).strip()
            #print(nome_aposta)
            odd = myStrip(o.find_all(string=True, recursive=False)[1].text).strip()

            if "1Х2 -" in nome_aposta:
                team = myStrip(nome_aposta.replace("1Х2 -","")).strip()
                if team[0] == "V":
                    team = team[1:]
                aposta = "odd"+team
                obj[aposta] = odd
        obj['local'] = "Sem Informação"
        obj['casa'] = "22bet"
        obj['id'] = len(bet22Dict["bet22"])
        bet22Dict["bet22"].append(obj)
    
    # json dump to file with utf-8 encoding
    with open('bet22.json', 'w', encoding='utf-8') as f:
        json.dump(bet22Dict, f, ensure_ascii=False, indent=4)

def bwin(url, liga):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)

    # Acesse a URL desejada
    driver.get('https://sports.bwin.pt/pt/sports/futebol-4/apostar/portugal-37/liga-portugal-bwin-102851')

    # Aguarde até que o elemento "main-content" seja carregado
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "participant")))

    # Obtenha o HTML da página da web
    html = driver.page_source
    
#    Feche o navegador da web
    driver.quit()   
    
    soup = BeautifulSoup(html, 'html.parser')
    bwinDict = {}
    bwinDict["bwin"]=[]
    
    jogos = soup.find_all("div", class_="grid-event-wrapper ng-star-inserted")
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
            odd = myStrip(o_soup.find("div",class_="option-value").text).strip()
            apostas.append(odd)
        
        obj['local'] = "Sem Informação"
        obj['casa'] = "bwin"
        obj['id'] = str(len(bwinDict["bwin"]))
        
        if len(apostas) >= 3:
            obj['odd1'] = apostas[0]
            obj['oddx'] = apostas[1]
            obj['odd2'] = apostas[2]
            bwinDict["bwin"].append(obj)
        else:
            print("Apostas insuficientes: ",apostas)
    
    # json dump to file with utf-8 encoding
    with open('bwin.json', 'w', encoding='utf-8') as f:
        json.dump(bwinDict, f, ensure_ascii=False, indent=4)
        

def betano(url, liga):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    betanoDict = {}
    betanoDict["betano"]=[]
    dados = soup.find_all("body", class_="")[0]
    # get <script> </script> content
    dados = str(dados).split("<script>")[1].split("</script>")[0]
    dados = dados.split("=")[1:]
    dados = "=".join(dados)
    dados = json.loads(dados)
    eventos = dados["data"]["blocks"]
    
    with open('leagues.json', 'r') as f:
        data = json.load(f)

    last_id = int(data['jogos'][-1]['id'])
    
    fileW = open ("leagues.json", "w+")
    
    #Percorrer os diferentes jogos de respetiva liga
    for e in eventos:
        lista_de_jogos = e["events"]
        for j in lista_de_jogos:
            nomeLiga = liga
            if " - " in j["name"] and j["name"].split(" ")[0] != "Série":
                nomeJogo = j["name"].split(" - ")[0] + "§" + j["name"].split(" - ")[1]
                mercados = j["markets"]
                for m in mercados:
                    if m["name"] == "Resultado Final":
                        selecoes = m["selections"]
                        odd1 = str(selecoes[0]["price"])
                        oddx = str(selecoes[1]["price"])
                        odd2 = str(selecoes[2]["price"])
                
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
            
            
def betano2():
    url = "https://www.betano.pt/sport/futebol/portugal/primeira-liga/17083/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    dados = soup.find_all("body", class_="")[0]
    # get <script> </script> content
    dados = str(dados).split("<script>")[1].split("</script>")[0]
    #print(dados)
    # from "a = b" discard a and return string "b"
    dados = dados.split("=")[1:]
    dados = "=".join(dados)
    dados = json.loads(dados)

#  ligas = dados["data"]["leaguesList"]
    ligas = ["https://www.betano.pt/sport/futebol/portugal/primeira-liga/17083/", "https://www.betano.pt/sport/futebol/inglaterra/premier-league/1/",
            "https://www.betano.pt/sport/futebol/italia/serie-a/1635/", "https://www.betano.pt/sport/futebol/espanha/laliga/5/"]
        
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

#bet22("https://22bet-bet.com/pt/line/football","liga")
bwin("https://sports.bwin.pt/pt/sports","liga")
#betclic2()
#casasDict["betclic"] = betclicDict["betclic"]
#betano2()
#casasDict["betano"] = betanoDict["betano"]
