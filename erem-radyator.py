from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
from bs4 import BeautifulSoup

option = webdriver.ChromeOptions()
option.add_argument("start-maximized")
option.add_experimental_option("detach",True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=option)

def create_price_list(category_url):
    login()
    get_products(category_url)

def login():
    url = "https://www.b2b-eremgroup.com/LOGIN.aspx"
    with open("password.txt", 'r', newline='') as file:
        username = file.readline()
        print(username)
        password = file.readline()
        print(password)
    
    driver.get(url)
    time.sleep(1)
    driver.find_element("name", "ctl00$body$EMAIL").send_keys(username)
    time.sleep(1)
    driver.find_element("name", "ctl00$body$PASSWORD").send_keys(password)
    time.sleep(1)
    driver.find_element("name", "ctl00$body$REMEMBERME").click()
    time.sleep(2)
    driver.find_element("name", "ctl00$body$btnLogin").click()
    time.sleep(3)
    
def get_products(category_url):
    with open("baymak_radyator.csv", 'w', newline='') as file:
        for x in range(1, 6):
            driver.get(category_url+f"{x}") 
            time.sleep(1)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            products = soup.find_all("div",{"class": "product"})

            for product in products:
                writer = csv.writer(file)
                writer.writerow([product.find_next("h6",{"class": "product_title"}).string, product.find_next("span",{"class": "price"}).string])

baymak_radyator_url = "https://www.b2b-eremgroup.com/PRODUCT.aspx?LIST=1&TRENDING=&NEWARRIVAL=&BESTSELLER=&FEATURED=&SPECIALOFFER=&DEALOFDAY=&TOPRATED=&CAT1=Radyat%C3%B6r%20Grubu&CAT2=&BRAND=&WORD=&FILTER=ER05.02-2066%2cER05.03-2049%2cER05.03-2052%2cER05.05-2083&PAGE="

create_price_list(baymak_radyator_url)
