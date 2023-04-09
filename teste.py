import requests
from bs4 import BeautifulSoup
import json

casasDict = {}

def betclic(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    odds = []
    teams = []

    for div in soup.find_all('span', class_='oddValue'):
        odd = div.text.strip().replace('\n','')
        odds.append(odd)

    for div in soup.find_all('span', class_='oddMatchName'):
        team = div.text.strip().replace('\n','')
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
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    #betanoDict["bet22"][liga]={}

    
    dados = soup.find_all("script", type="application/ld+json")
    for d in dados:
        if "SportsEvent" in str(d):
            dados = d
            break
    # get <script> </script> content
    dados = str(dados).split("<script type=\"application/ld+json\">")[1].split("</script>")[0]
    print(dados)
    dados = json.loads(dados)

    for e in dados:
        eCasa = e['homeTeam']['name']
        eFora = e['awayTeam']['name']
        nome_jogo = eCasa + " § " + eFora


    # json dump to file with utf-8 encoding
    #with open('bet22.json', 'w', encoding='utf-8') as f:
    #    json.dump(dados, f, ensure_ascii=False, indent=4)

bet22("https://22bet-bet.com/pt/line/football","liga")

betanoDict = {"bet22":{}}

def betano(url, liga):
    global betanoDict
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    betanoDict["bet22"][liga]={}

    dados = soup.find_all("body", class_="")[0]
    # get <script> </script> content
    dados = str(dados).split("<script>")[1].split("</script>")[0]
    dados = dados.split("=")[1:]
    dados = "=".join(dados)
    dados = json.loads(dados)

    eventos = dados["data"]["blocks"]
    for e in eventos:
        lista_de_jogos = e["events"]
        for j in lista_de_jogos:
            nome_jogo = j["name"]
            betanoDict["betano"][liga][nome_jogo] = []
            mercados = j["markets"]
            for m in mercados:
                if m["name"] == "Resultado Final":
                    selecoes = m["selections"]
                    for s in selecoes:
                        equipa = s["name"] # "1"
                        nomeEquipa = s["fullName"] # "Manchester City"
                        odd = s["price"] # "1.25"
                        betanoDict["betano"][liga][nome_jogo].append({"nome":nomeEquipa, "odd":odd})
    
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

    ligas = dados["data"]["leaguesList"]

    for l in ligas:
        betano("https://www.betano.pt"+l["url"], l["text"])
    
    # json dump to file with utf-8 encoding
    with open('betano.json', 'w', encoding='utf-8') as f:
        json.dump(betanoDict, f, ensure_ascii=False, indent=4)


#betclic2()
#casasDict["betclic"] = betclicDict["betclic"]
#betano2()
#casasDict["betano"] = betanoDict["betano"]