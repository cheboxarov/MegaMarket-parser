import re

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
def pars(name, pages):
    option = Options()
    option.add_argument("--disable-infobars")
    browser = webdriver.Chrome()
    full_items = ''
    products = []
    for page in range(1, pages+1):
        print("Парсинг страницы "+ str(page))
        browser.get('https://megamarket.ru/catalog/page-'+str(page)+'/?q='+name)
        el = browser.find_elements(By.CLASS_NAME, "catalog-item-mobile.ddl_product")
        for i in range(1, 100):
            time.sleep(0.01)
            browser.execute_script("window.scrollTo(0, "+str(i)+"00)")
            print("Процесс парсинга "+str(i)+" / 100")
        for v in el:
            try:
                product = dict()
                price = ''
                bonus = ''
                title = ''
                price = v.find_element(By.CLASS_NAME, "item-price").text
                bonus = v.find_element(By.CLASS_NAME, "item-bonus").text
                title = v.find_element(By.CLASS_NAME, "item-title").text
                price = price.replace(" ", "")
                price = price.replace("₽", "")
                bonus = bonus.replace(" ", "")
                id = v.get_attribute("id")
                product['price'] = price
                product['bonus'] = bonus
                product['title'] = title
                product['id'] = id
                product['best_price'] = int(price)-int(bonus)
                product['procent'] = int(bonus) / int(price) * 100
                products.append(product)
            except:
                pass
        sorted_products = sorted(products, key=lambda x: x['procent'], reverse=True)
        writeFilePars(sorted_products, name+"_best_procent")
        sorted_products_price = sorted(products, key=lambda x: x['best_price'])
        writeFilePars(sorted_products_price, name + "_best_price")

def writeFilePars(products, name):
    full_items = ''
    for product in products:
        price = product['price']
        bonus = product['bonus']
        title = product['title']
        id = product['id']
        full_items += "ID: " + id + " "
        full_items += title + " Цена: " + price + " Бонусами вернут - " + bonus + " Процент бонуса: " + str(
            int(bonus) / int(price) * 100) + "% чистая цена - "+str(int(price)-int(bonus))+"\n"
    f = open(name + ".txt", "w", encoding="utf-8")
    f.write(full_items)

def main():
    name = input("Введите имя товара: ")
    pages = input("Введите кол-во страниц: ")
    pars(name, int(pages))

if __name__ == '__main__':
    main()