from fileinput import close
import json

with open('leagues.json', 'r') as f:
    data = json.load(f)

last_id = int(data['jogos'][-1]['id'])

fileR = open ("betanoDict.json", "r")
betanoDict = json.load(fileR)

fileW = open ("leagues.json", "w+")

ligas = ["PORTUGAL - Primeira Liga", "ITÁLIA - Série A", "INGLATERRA - Premier League", "ESPANHA - LaLiga"]

jogos = []

for liga in ligas:
    for jogo in betanoDict["betano"][liga]:
        if " - " in jogo:
            nomeJogo = jogo.split(" - ")[0] + "§" + jogo.split(" - ")[1]
        else :
            pass
        if len(betanoDict["betano"][liga][jogo]) > 0:
            odd1 = str(betanoDict["betano"][liga][jogo][0]["odd"])
            oddx = str(betanoDict["betano"][liga][jogo][1]["odd"])
            odd2 = str(betanoDict["betano"][liga][jogo][2]["odd"])
        if liga == "PORTUGAL - Primeira Liga":
            nomeLiga = "Liga Portuguesa"
        elif liga == "ITÁLIA - Série A":
            nomeLiga = "Liga Italiana"
        elif liga == "INGLATERRA - Premier League":
            nomeLiga = "Liga Inglesa"
        elif liga == "ESPANHA - LaLiga":
            nomeLiga = "Liga Espanhola"
        jogoInfo = {"liga":nomeLiga, "jogo":nomeJogo, "data": "Sem Informações", "local": "Sem Informações", "odd1":odd1, "oddx":oddx, "odd2":odd2, "casa": "Betano"}
        
        # verifica se o jogo já existe e atualiza as odds em vez de adicioná-lo
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

json.dump(data, fileW, indent=4)

