from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from random import randint
from time import sleep
import os
import csv

class WebScraping:
    def __init__(self, driver) -> None:
        self.driver = driver
        self.driver.implicitly_wait(20)
        self.url = 'https://www.mercadolivre.com.br'
        self.campo_busca = '//input[@class="nav-search-input"]' #xpath
        self.title = '//h2[@class="ui-search-item__title"]' #xpath
        self.precos = '//div[1]/div/div/span[1]/span[2]' #xpath
        self.link = '//div[@class="ui-search-item__group ui-search-item__group--title"]//a[@class="ui-search-item__group__element ui-search-link"]' #xpath
        self.proxima_pagina = '//li[@class="andes-pagination__button andes-pagination__button--next"]'
    
    def _get_navegar(self):
        self.driver.get(self.url)
        sleep(randint(3, 5))


    def _get_busca(self, word='None'):
        teste = self.driver.find_element_by_xpath(self.campo_busca)
        sleep(randint(3, 5))
        teste.click()
        sleep(randint(3, 5))
        teste.send_keys(word)
        sleep(randint(3, 5))
        teste.send_keys(Keys.ENTER)


    def _get_scraping(self):
        sleep(randint(3, 5))
        titulos = self.driver.find_elements_by_xpath(self.title)
        sleep(randint(3, 5))
        precos = self.driver.find_elements_by_xpath(self.precos)
        sleep(randint(3, 5))
        links_produtos = []
        link = self.driver.find_elements_by_xpath(self.link)
        sleep(randint(3, 5))
        for teste in link:
            a = teste.get_attribute("href")
            links_produtos.append(a)
        self._save_get_all_data(titulos, precos, links_produtos)
    
    def _save_get_all_data(self, titulos, precos, links_produtos):
        for item in range(0, len(titulos)):
            dados = [
                titulos[item].text,
                precos[item].text,
                links_produtos[item],
            ]
            with open('mercado_livre.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(dados)
            
            """with open('mercado_livre.txt', 'a', newline='', encoding='utf-8') as arquivo:
                arquivo.write(dados[0] + ',' + dados[1] + ',' + dados[2] + os.linesep)"""

    def _get_proxima_pagina(self):
        sleep(randint(3, 5))
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(randint(3, 5))
        btn_seguinte = self.driver.find_element_by_xpath(self.proxima_pagina)
        btn_seguinte.click()

        

firefox = webdriver.Firefox()
obj = WebScraping(firefox )
obj._get_navegar()
obj._get_busca('ferramentas')
while True:
    obj._get_scraping()
    obj._get_proxima_pagina()
firefox.quit()
