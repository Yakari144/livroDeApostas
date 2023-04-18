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
    nl = []
    for i in diciYaka[j2]:
        if i not in nl:
            nl.append(i)
    for i in diciYaka[j1]:
        if i not in nl:
            nl.append(i)
    for i in nl:
        diciYaka[i] = nl
        diciYaka[i].sort()

## write a function to ask the user if the two strings are the same
def ask(j1,j2):
    c1 = j1.split('§')[0]
    c2 = j2.split('§')[0]
    f1 = j1.split('§')[1]
    f2 = j2.split('§')[1]
    print('Casa: {} - {}'.format(c1,c2))
    print('Fora: {} - {}'.format(f1,f2))
    print('São iguais? (s/n)')
    r = input()
    if r == 's':
        return True
    else:
        return False

def checkMatch(j1,j2):
    global diciYaka
    c1 = j1.split('§')[0]
    c2 = j2.split('§')[0]
    f1 = j1.split('§')[1]
    f2 = j2.split('§')[1]
    if c1 not in diciYaka or c2 not in diciYaka or f1 not in diciYaka or f2 not in diciYaka:
        return False
    # check is 2 lists have at least 1 element in common
    elif any(i in diciYaka[c1] for i in diciYaka[c2]) and any(i in diciYaka[f1] for i in diciYaka[f2]):
        return True
    else:
        return False

def main():
    global diciYaka
    with open('leagues.json','r+') as f:
        dic = json.load(f)
    for j1 in dic['jogos']:
        adicionou = False
        quase = []
        for j2 in dic['jogos']:
            if j1 == j2:
                continue
            c1 = j1['jogo'].split('§')[0]
            c2 = j2['jogo'].split('§')[0]
            f1 = j1['jogo'].split('§')[1]
            f2 = j2['jogo'].split('§')[1]
            if checkMatch(j1['jogo'],j2['jogo']):
                adicionou = True
                addDicionario(c1,c2)
                addDicionario(f1,f2)
            else:
                rat =  yakari(j1['jogo'],j2['jogo'],0,0)
                if rat > 65:
                    adicionou = True
                    addDicionario(c1,c2)
                    addDicionario(f1,f2)
                elif rat > 50:
                    existe = False
                    for q in quase:
                        if checkMatch(j2['jogo'],q):
                            existe = True
                    if not existe:
                        quase.append(j2['jogo'])
        if not adicionou:
            for q in quase:
                if ask(q,j1['jogo']):
                    adicionou = True
                    c1 = j1['jogo'].split('§')[0]
                    c2 = q.split('§')[0]
                    f1 = j1['jogo'].split('§')[1]
                    f2 = q.split('§')[1]
                    addDicionario(c1,c2)
                    addDicionario(f1,f2)
        if not adicionou:
            c = j1['jogo'].split('§')[0]
            f = j1['jogo'].split('§')[1]
            diciYaka[c] = [c]
            diciYaka[f] = [f]
    with open('dicionario.json', 'w', encoding='utf-8') as f:
        json.dump(diciYaka, f, ensure_ascii=False, indent=4)

main()


