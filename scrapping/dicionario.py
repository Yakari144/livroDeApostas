import json
import spacy
from spacy.matcher import Matcher


def julinho():
    fileR = open ("leagues.json", "r")
    data = json.load(fileR)
    
    fileW = open ("nomesEquipas.txt", "w+")
    
    for jogo in data['jogos']:
        fileW.write(jogo['jogo'].split('§')[0] + '\n')
        fileW.write(jogo['jogo'].split('§')[1] + '\n')


nlp = spacy.load("en_core_web_sm")

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

# Definir padrões de correspondência de nomes de equipes
patterns = []
for team_name, synonyms in team_synonyms.items():
    pattern = [{"LOWER": synonym.lower()} for synonym in synonyms]
    patterns.append({"label": "TEAM", "pattern": pattern})

# Adicionar padrões de correspondência de nomes de equipes ao Matcher
matcher = Matcher(nlp.vocab)
for pattern in patterns:
    matcher.add("TEAM", None, pattern)

# Adicionar Matcher ao pipeline do spaCy
nlp.add_pipe(matcher, after="ner")

# Texto de exemplo contendo nomes de equipes
text = "O Benfica joga hoje contra o FC Porto"

# Processar texto com pipeline do spaCy
doc = nlp(text)

# Substituir nomes de equipes pelos seus nomes comuns
for ent in doc.ents:
    if ent.label_ == "TEAM":
        team_name = ent.text
        for common_name, synonyms in team_synonyms.items():
            if team_name in synonyms:
                text = text.replace(team_name, common_name)

print(text)
