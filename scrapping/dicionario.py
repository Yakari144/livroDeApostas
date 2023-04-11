import unidecode
import re
from fuzzywuzzy import fuzz
import json

def normaliza(text):
    text = text.replace(" ","")
    text = text.lower()
    text = unidecode.unidecode(text)
    return text

def myStrip(text):
    return re.sub(r'\s+', ' ', text).strip()

diciYaka = json.loads(open('dicionario.json').read())    

# casa§fora
def yakari(j1,j2,s1,s2):
    c1 = normaliza(j1.split('§')[0])
    c2 = normaliza(j2.split('§')[0])
    f1 = normaliza(j1.split('§')[1])
    f2 = normaliza(j2.split('§')[1])
    rc = fuzz.ratio(c1,c2)
    rf = fuzz.ratio(f1,f2)
    if rc < rf:
        return rc
    else:
        return rf
    
def addDicionario(j1,j2):
    global diciYaka
    if j1 not in diciYaka:
        diciYaka[j1] = [j1]
    if j2 not in diciYaka:
        diciYaka[j2] = [j2]
    # merge 2 lists into 1 removing duplicates

    diciYaka[j1] = list(set(diciYaka[j1] + diciYaka[j2]))
    diciYaka[j2] = list(set(diciYaka[j1] + diciYaka[j2]))

def main():
    global diciYaka
    with open('leagues.json','r+') as f:
        dic = json.load(f)
    print(len(dic['jogos']))
    for j1 in dic['jogos']:
        for j2 in dic['jogos']:
            if j1['jogo'] != j2['jogo']:
                rat =  yakari(j1['jogo'],j2['jogo'],0,0)
                if rat > 65:
                    c1 = j1['jogo'].split('§')[0]
                    c2 = j2['jogo'].split('§')[0]
                    f1 = j1['jogo'].split('§')[1]
                    f2 = j2['jogo'].split('§')[1]
                    addDicionario(c1,c2)
                    addDicionario(f1,f2)
                    break
    with open('dicionario.json', 'w', encoding='utf-8') as f:
        json.dump(diciYaka, f, ensure_ascii=False, indent=4)

# Definir lista de sinônimos para cada equipe
team_synonyms = {
"almeria" : ["Almeria", "UD Almería"],
"arouca" : ["Arouca", "FC Arouca"],
"arsenal" : ["Arsenal", "Arsenal FC"],
"astonvilla" : ["Aston Villa", "Aston Villa FC"],
"atalanta" : ["Atalanta", "Atalanta BC"],
"athleticbilbau" : ["Athletic Bilbao", "Atletico de Bilbao"],
"atleticomadrid" : ["Atletico Madrid", "Atlético Madrid"],
"barcelona" : ["Barcelona", "FC Barcelona"],
"benfica" : ["Benfica", "SL Benfica", "Sport Lisboa e Benfica"],
"betis" : ["Betis", "Real Betis", "Real Bétis", "Bétis"],
"boavista" : ["Boavista", "Boavista FC", "Boavista Porto"],
"bolonha" : ["Bologna 1909", "Bologna", "Bolonha"],
"bournemouth" : ["Bournemouth", "AFC Bournemouth"],
"brentford" : ["Brentford"],
"brighton" : ["Brighton & Hove Albion", "Brighton"],
"cadiz" : ["Cádiz", "Cadiz FC"],
"casapia" : ["Casa Pia", "Casa Pia AC"],
"celtavigo" : ["Celta", "Celta Vigo", "Celta de Vigo"],
"chaves" : ["Chaves", "GD Chaves"],
"chelsea" : ["Chelsea", "Chelsea FC"],
"cremonese" : ["Cremonese", "Cremonese Calcio", "US Cremonese"],
"crystalpalace" : ["Crystal Palace", "Crystal Palace FC"],
"elche" : ["Elche", "Elche CF"],
"empoli" : ["Empoli", "Empoli FC"],
"espanyol" : ["Espanyol", "Espanhol"],
"estoril" : ["Estoril", "GD Estoril Praia"],
"everton" : ["Everton FC", "Everton"],
"famalicao" : ["FC Famalicão", "FC Famalicao", "Famalicão", "Famalicao"],
"fcporto" : ["FC Porto", "Porto", "porto"],
"fiorentina" : ["Fiorentina", "Fiorentina FC"],
"fulham" : ["Fulham FC", "Fulham"],
"getafe" : ["Getafe", "Getafe CF"],
"gilvicente" : ["Gil Vicente", "Gil Vicente FC", "Gil Vicente"],
"girona" : ["Girona", "Girona FC"],
"inter" : ["Internazionale Milano", "Inter", "Inter Milan", "Inter de Milão", "Inter Milão"],
"juventus" : ["Juventus", "Juventus Turin", "Juventus FC"],
"lazio" : ["Lazio", "Lazio Roma", "Lázio", "Lazio Roma"],
"lecce" : ["Lecce", "US Lecce"],
"leeds" : ["Leeds United AFC", "Leeds United", "Leeds"],
"leicester" : ["Leicester City", "Leicester"],
"liverpool" : ["Liverpool", "Liverpool FC"],
"maiorca" : ["Mallorca", "Maiorca", "RCD Mallorca"],
"manchestercity" : ["Manchester City"],
"manchesterutd" : ["Manchester United"],
"maritimo" : ["Marítimo", "CS Marítimo"],
"milan" : ["Milan", "AC Milan", "AC Milan 1899", "Milão", "AC Milão"],
"monza" : ["Monza 1912", "Monza", "AC Monza"],
"napoles" : ["Napoli", "Napoli FC", "Napoles", "Nápoles"],
"newcastle" : ["Newcastle United FC", "Newcastle United", "Newcastle"],
"nottinghamforest" : ["Nottingham Forest", "Nottingham", "Nottingham F."],
"osasuna" : ["Osasuna", "Osasuna P. Navarra"],
"pacosdeferreira" : ["Paços de Ferreira", "FC Paços de Ferreira"],
"portimonense" : ["Portimonense Sporting Clube", "Portimonense", "Portimonense SC"],
"rayovallecano" : ["Rayo Vallecano"],
"realmadrid" : ["Real Madrid", "Real Madrid CF", "Real Madrid C.F.", "Real Madrid C.F"],
"realsociedad" : ["Real Sociedad"],
"realvalladolid" : ["Real Valladolid"],
"rioave" : ["Rio Ave", "Rio Ave FC", "Rio Ave Futebol Clube"],
"roma" : ["Roma", "AS Roma"],
"salernitana" : ["Salernitana 1919", "Salernitana"],
"sampdoria" : ["Sampdoria", "Sampdoria Genua"],
"santaclara" : ["Santa Clara", "CD Santa Clara"],
"sassuolo" : ["Sassuolo Calcio", "Sassuolo"],
"sevilha" : ["Sevilla", "Sevilla FC"],
"southampton" : ["Southampton", "Southampton FC"],
"sp.braga" : ["SC Braga", "Sporting Clube de Braga", "Sporting Braga", "Braga", "SC Braga"],
"spezia" : ["Spezia Calcio", "Spezia"],
"sporting" : ["Sporting Clube de Portugal", "Sporting CP", "Sporting"],
"torino" : ["Torino FC", "Torino"],
"tottenham" : ["Tottenham Hotspur", "Tottenham"],
"udinese" : ["Udinese Calcio", "Udinese"],
"valencia" : ["Valência", "Valência CF", "Valencia", "Valencia CF"],
"verona" : ["Hellas Verona", "Verona"],
"villarreal" : ["Villarreal", "Villarreal CF"],
"vitoriasc" : ["Vitoria Guimarães", "Vitória Guimarães", "Vitória SC", "Vitória", "Vitória S.C."],
"vizela" : ["FC Vizela", "Vizela"],
"westham" : ["West Ham United", "West Ham"],
"wolves" : ["Wolverhampton Wanderers", "Wolverhampton", "Wolves"],
}

main()

a = [1,2,3]
b = [2,3,4]

