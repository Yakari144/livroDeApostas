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
    "Benfica": ["Benfica", "SL Benfica", "Sport Lisboa e Benfica"],
    "Porto": ["FC Porto", "FCP", "Porto", "FCPorto"],
    "Braga": ["SC Braga", "SCB", "Braga", "SCBraga", "Sp. Braga"],
    # Adicionar outras equipes aqui
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
