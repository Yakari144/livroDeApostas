from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
#options.add_argument('headless')
driver = webdriver.Chrome(options=options)

# Acesse a URL desejada
driver.get('https://sports.bwin.pt/pt/sports/futebol-4/apostar/portugal-37/liga-portugal-bwin-102851')

# Aguarde até que o elemento "main-content" seja carregado
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "participant")))

# Obtenha o HTML da página da web
html = driver.page_source

# Salve o HTML em um arquivo
with open('bwin2.html', 'w', encoding="utf-8") as f:
    f.write(html)

# Feche o navegador da web
driver.quit()


