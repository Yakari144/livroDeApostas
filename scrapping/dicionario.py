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

main()

a = [1,2,3]
b = [2,3,4]

