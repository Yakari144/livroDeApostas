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

def teste():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get("https://www.betano.pt/sport/futebol/portugal/primeira-liga/17083/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "event__name")))
        content = driver.page_source
        print(content)
        driver.quit()
    except Exception as e:
        print(e)
        return

#start timer
start_time = time.time()
#teste()
#end timer
print("--- %s seconds ---" % (time.time() - start_time))

def normaliza(text):
    text = text.replace(" ","")
    text = text.lower()
    text = unidecode.unidecode(text)
    return text

def myStrip(text):
    return re.sub(r'\s+', ' ', text).strip()

casasDict = {}

def betclic(url,liga):
    # cada jogo "groupEvents_card"
    #global betclicDict
    #response = requests.get(url)
    f = open("betclic.html", "r")
    response = f.read()
    f.close()
    soup = BeautifulSoup(response, 'html.parser')
    with open('leagues.json', 'r') as f:
        data = json.load(f)
    
    jogos = soup.find_all("sports-events-event", class_="groupEvents_card")
    for j in jogos:
        obj = {'liga':liga}
        j_soup = BeautifulSoup(str(j), 'html.parser')
        eqs = j_soup.find_all("div",class_="scoreboard_contestantLabel")
        eq1=normaliza(myStrip(eqs[0].text).strip())
        eq2=normaliza(myStrip(eqs[1].text).strip())
        
        if len(eqs) == 2:
            obj['jogo'] = myStrip(eqs[0].text).strip() + "§" + myStrip(eqs[1].text).strip()
        data = myStrip(j_soup.find("div",class_="event_infoTime").text).strip()
        obj['data'] = myStrip(data.split(" ")[0]).strip()

        odds = j_soup.find_all("sports-selections-selection",class_="oddButton")
        for o in odds:
            o_soup = BeautifulSoup(str(o), 'html.parser')
            nome_aposta = normaliza(myStrip(o_soup.find("span",class_="oddMatchName").text).strip())
            #print(nome_aposta)
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
            obj[aposta] = odd
        obj['local'] = "Sem Informação"
        obj['casa'] = "betclic"
        jogo_existente = False
        for j in data['jogos']:
            if j['jogo'] == obj['jogo'] and j['casa'] == obj['casa']:
                j['odd1'] = j['odd1']
                j['oddx'] = j['oddx']
                j['odd2'] = j['odd2']
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

#betclic("asf","Liga Portuguesa")

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
    options = webdriver.ChromeOptions()
#    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)

    # Acesse a URL desejada
    driver.get(url)

    # Aguarde até que o elemento "main-content" seja carregado
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "c-events__team")))

    # Obtenha o HTML da página da web
    html = driver.page_source
    
#    Feche o navegador da web
    driver.quit()   
    with open('leagues.json', 'r') as f:
        data = json.load(f)
    
    soup = BeautifulSoup(html, 'html.parser')
    
    jogos = soup.find_all("div", class_="c-events__item c-events__item_col")
    for j in jogos:
        obj = {'liga':liga}
        j_soup = BeautifulSoup(str(j), 'html.parser')
        eqs = j_soup.find_all("div",class_="c-events__team")
        if len(eqs) == 2:
            obj['jogo'] = myStrip(eqs[0].text).strip() + "§" + myStrip(eqs[1].text).strip()
        dH = myStrip(j_soup.find("div",class_="c-events__time min").text).strip()
        obj['data'] = myStrip(dH.split(" ")[0]).strip()
        hora = myStrip(dH.split(" ")[1]).strip()
        odds = j_soup.find_all("div",class_="c-bets__bet")
        i = 0
        for o in odds:
            if i > 3:
                break
            else:
                i+=1
            #print(nome_aposta)
            odd = myStrip(o.find_all(string=True, recursive=False)[1].text).strip()
            if i == 1:
                aposta = "odd1"
            elif i == 2:
                aposta = "oddx"
            elif i == 3:
                aposta = "odd2"
            obj[aposta] = odd
        obj['local'] = "Sem Informação"
        obj['casa'] = "22bet"
        
        jogo_existente = False
        for j in data['jogos']:
            if j['jogo'] == obj['jogo'] and j['casa'] == obj['casa']:
                j['odd1'] = j['odd1']
                j['oddx'] = j['oddx']
                j['odd2'] = j['odd2']
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

def bwin(url, liga):
    options = webdriver.ChromeOptions()
#    options.add_argument('headless')
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
            odd = myStrip(o_soup.find("div",class_="option-value").text).strip()
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
                    j['odd1'] = j['odd1']
                    j['oddx'] = j['oddx']
                    j['odd2'] = j['odd2']
                    jogo_existente = True
                    break
                
            # se o jogo não existir, adiciona-o
            if not jogo_existente:
                last_id += 1
                obj['id'] = str(last_id)
                data['jogos'].append(obj)
            
            print("Novo jogo: ",obj['jogo'])
        else:
            print("Apostas insuficientes: ",apostas)
    
    # json dump to file with utf-8 encoding
    with open('leagues.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
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

bet22("https://22bet-bet.com/pt/line/football/118663-portugal-primeira-liga","Liga Portuguesa")
#bwin('https://sports.bwin.pt/pt/sports/futebol-4/apostar/portugal-37/liga-portugal-bwin-102851',"Liga Portuguesa")
#betclic2()
#casasDict["betclic"] = betclicDict["betclic"]
#betano2()
#casasDict["betano"] = betanoDict["betano"]

