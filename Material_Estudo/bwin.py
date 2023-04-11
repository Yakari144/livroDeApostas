from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Acesse a URL desejada
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)
try:
    driver.get('https://sports.bwin.pt/pt/sports/futebol-4/apostar/portugal-37/liga-portugal-bwin-102851')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "event__name")))
    html = driver.page_source
    driver.quit()
except Exception as e:
    print(e)
    driver.quit()

teste = open("bwin.html", "w")

teste.write(html)

# Feche o navegador da web
driver.quit()

# Imprima o HTML
print(html)
