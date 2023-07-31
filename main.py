#Adding Library And Package

import re
import psycopg2
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


#Functions

def scroll_to_bottom():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            WebDriverWait(driver, 5).until(
                lambda driver: driver.execute_script("return document.body.scrollHeight") > last_height)
            last_height = driver.execute_script("return document.body.scrollHeight")
        except:
            break


def move_year_to_end(text):
    year_pattern = re.compile(r'\b(20\d{2})\b')
    match = year_pattern.search(text)
    if match:
        text_without_year = year_pattern.sub('', text).strip()
        new_text = f"{text_without_year} {match.group(1)}"
        return new_text
    return text



def has_arabic_numbers(text):
    eastern_arabic_numerals = '۰۱۲۳۴۵۶۷۸۹'
    resault = False
    for char in text:
        if char in eastern_arabic_numerals or char == ',':
            resault = True
        else:
            return False
    return resault


def arabic_to_english_numbers(arabic_number):
    eastern_arabic_numerals = '۰۱۲۳۴۵۶۷۸۹'
    english_numerals = '0123456789'

    english_number = ''
    for char in arabic_number:
        if char in eastern_arabic_numerals:
            english_number += english_numerals[eastern_arabic_numerals.index(char)]
        elif char == '.':
            english_number += '.'
    return float(english_number)



#Connecting Database And Table Creation

conn = psycopg2.connect(database='digikala',
                        host="localhost",
                        port=5432,
                        user="postgres",
                        password="1234")
conn.autocommit = True
cursor = conn.cursor()
cursor.execute('''CREATE TABLE NOT EXISTS asus(
                modul   VARCHAR(200),
                price   FLOAT,
                score   FLOAT
                );''')
cursor.execute('''CREATE TABLE NOT EXISTS msi(
                modul   VARCHAR(200),
                price   FLOAT,
                score   FLOAT
                );''')
cursor.execute('''CREATE TABLE NOT EXISTS lenovo(
                modul   VARCHAR(200),
                price   FLOAT,
                score   FLOAT
                );''')
cursor.execute('''CREATE TABLE NOT EXISTS hp(
                modul   VARCHAR(200),
                price   FLOAT,
                score   FLOAT
                );''')
cursor.execute('''CREATE TABLE NOT EXISTS acer(
                modul   VARCHAR(200),
                price   FLOAT,
                score   FLOAT
                );''')
cursor.execute('''CREATE TABLE IF NOT EXISTS apple(
                modul   VARCHAR(200),
                price   FLOAT,
                score   FLOAT
                );''')


#Connecting To DigiKala

service = Service("D:\DigiKala\chromedriver.exe")
options = Options()
options.binary_location = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
driver = webdriver.Chrome(options=options, service=service)
driver.get('https://www.digikala.com/')
driver.maximize_window()
resp = requests.get('https://www.digikala.com/')
html = resp.text
bs = BeautifulSoup(html, 'html.parser')
#print(sidemenu.get_attribute('outerHTML'))




#Sidmenu

sidemenu = WebDriverWait(driver, 20).until(EC.presence_of_element_located
                                           ((By.XPATH, '//*[@id="base_layout_desktop_fixed_header"]'
                                                       '/header/nav/div[1]/div[1]/div[1]/div/span')))
hover = ActionChains(driver).move_to_element(sidemenu)
hover.perform()


#Digital Devices

ddmenu = WebDriverWait(driver, 20).until(EC.presence_of_element_located
                                         ((By.XPATH,
                                           '//*[@id="base_layout_desktop_fixed_header"]/header/nav/'
                                           'div[1]/div[1]/div[1]/div/div/div/div[1]/a[2]')))
hover = ActionChains(driver).move_to_element(ddmenu)
hover.perform()


# #Laptops

laptopbutton = WebDriverWait(driver, 20).until(EC.presence_of_element_located
                                               ((By.XPATH, '//*[@id="base_layout_desktop_fixed_header"]'
                                                           '/header/nav/div[1]/div[1]/div[1]/div/div/'
                                                           'div/div[2]/div[2]/div[1]/ul/a[44]')))
driver.execute_script("arguments[0].click();", laptopbutton)


# 1A) Apple Page

apllebutton = WebDriverWait(driver, 40).until(EC.presence_of_element_located
                                                ((By.XPATH, '//*[@id="__next"]/div[1]/div[3]/div[3]/'
                                                            'div[5]/div/div[2]/span[1]/a/div')))
driver.execute_script("arguments[0].click();", apllebutton)



# 1B) Sorting

mostexpencive = WebDriverWait(driver, 40).until(EC.presence_of_element_located
                                                ((By.XPATH, '//*[@id="ProductListPagesWrapper"]/'
                                                            'section[1]/div[1]/div/div/div/div[2]/'
                                                            'span[6]'))).click()


# 1C) Available Products

availablebutton = WebDriverWait(driver, 40).until(EC.presence_of_element_located
                                                ((By.XPATH, '//*[@id="ProductListPagesWrapper"]/'
                                                            'section[2]/div/div/div[1]/div[7]/div/'
                                                            'div[2]/div/div/label[2]/span[2]')))
driver.execute_script("arguments[0].click();", availablebutton)



# 1D) Scraping Laptop Moduls

time.sleep(20)
scroll_to_bottom()
moduls = driver.find_elements(By.TAG_NAME, 'h3')



# # 1E) Cleaning Moduls

moduls.pop()
persian_part = r'لپ تاپ [\d.]+ اینچ[ی]? اپل مدل '
list = []
for m in moduls:
    list.append(m.text)
modullist = [move_year_to_end(re.sub(persian_part, '', text)) for text in list]



# # 1F) Scraping Prices

pricelist = []
prices = driver.find_elements(By.TAG_NAME, 'span')
for x in prices:
    if has_arabic_numbers(x.text):
        pricelist.append(arabic_to_english_numbers(x.text))


# # 1F) Scraping Scores

scorelist = []
for i in moduls:
    driver.execute_script("arguments[0].click();", i)
    driver.switch_to.window(driver.window_handles[1])
    scroll_to_bottom()

    try:
        score = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[3]/div[3]/div[2]/div[2]/'
                                                            'div[2]/div[2]/div[1]/div[2]/div[1]/p[1]')
        scorelist.append(arabic_to_english_numbers(score.text))
    except:
        scorelist.append(0)

    driver.close()
    driver.switch_to.window(driver.window_handles[0])



# 1G) Adding Data To The Database

for (i, j, k) in zip(modullist, pricelist, scorelist):
    cursor.execute(
        '''INSERT INTO apple (modul, price, score) VALUES (%s, %s, %s);''', (i,j,k,)
    )











conn.commit()
conn.close()
