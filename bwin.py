from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(options=options)
# Acesse a URL desejada
driver.get('https://sports.bwin.pt/pt/sports/futebol-4/apostar/portugal-37/liga-portugal-bwin-102851')

# Obtenha o HTML da página da web
html = driver.page_source

teste = open("bwin.html", "w")

teste.write(html)

# Feche o navegador da web
driver.quit()

# Imprima o HTML
print(html)
