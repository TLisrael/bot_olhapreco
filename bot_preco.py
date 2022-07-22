from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from time import sleep
import pandas as pandinha

"""
Inicialmente era pra ser um bot para monitorar os preços da cadeira
Pichau Mancer Tyr, mas como os inputs da pichau são aleatórios, 
resolvi partir para a Amazon e fazer um bot para monitorar o preço
de um monitor que preciso comprar.
Fui aprimorando para mais itens que quero adquirir e adicionei [ou tentei]
adicionar excel.
"""

options = Options()
options.add_argument("--headless") # Rodar em segundo plano

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=options
                          )

driver.get('https://www.amazon.com.br/')
produtos = ['Monitor AOC 23,8', 'Mouse Gamer Redragon Cobra',
            'Suporte MXT Bi-Articulado para 2 monitores 13" à 32"']

valores = list()  # Ou []
data = list()

for produto in produtos:
    busca_produto = driver.find_element(By.ID, 'twotabsearchtextbox')

    busca_produto.send_keys(produto)
    sleep(0.5)

    busca_produto.send_keys(Keys.ENTER)
    sleep(0.5)

    valor_prod_span = driver.find_element(
        By.XPATH, '//span[@class="a-price-whole"]')
    fracao_prod_span = driver.find_element(
        By.XPATH, '//span[@class="a-price-fraction"]')
    preco_produto = valor_prod_span.text
    centavos_produto = fracao_prod_span.text

    valores.append(preco_produto)

    data.append(datetime.now().strftime(
        '%d/%m/%Y %H:%M:%S'))  # Formatando datas;
    remove_produto = driver.find_element(By.ID, 'twotabsearchtextbox')
    remove_produto.send_keys(Keys.BACKSPACE * 30)

dados = {
    'Produto': produtos,
    'Preço': valores,
    'Data e Hora': data,
}
# Criando data frame e excel.
frame = pandinha.DataFrame(dados)
frame.to_excel('preco.xlsx', index=False)
