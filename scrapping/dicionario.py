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

diciYaka = {}    

# casa§fora
def yakari(j1,j2,s1,s2):
    c1 = normaliza(j1.split('§')[0])
    c2 = normaliza(j2.split('§')[0])
    return fuzz.ratio(c1,c2)
    
def main():
    with open('leagues.json','r+') as f:
        dic = json.load(f)
        for j1,j2 in dic['jogos']:
            rat =  yakari(j1['jogo'],j2['jogo'],0,0)
            if rat < 90:
                print('ok')
            else:
                print(j1['jogo'],j2['jogo'],rat)

