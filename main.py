#adding library and package
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

#connecting database and table creation
conn = psycopg2.connect(database='digikala',
                        host="localhost",
                        port=5432,
                        user="postgres",
                        password="1234")
sql = conn.cursor()
# sql.execute('''CREATE TABLE asus(
#                 modul   VARCHAR(200),
#                 price   FLOAT,
#                 score   FLOAT
#                 );''')
# sql.execute('''CREATE TABLE msi(
#                 modul   VARCHAR(200),
#                 price   FLOAT,
#                 score   FLOAT
#                 );''')
# sql.execute('''CREATE TABLE lenovo(
#                 modul   VARCHAR(200),
#                 price   FLOAT,
#                 score   FLOAT
#                 );''')
# sql.execute('''CREATE TABLE hp(
#                 modul   VARCHAR(200),
#                 price   FLOAT,
#                 score   FLOAT
#                 );''')
# sql.execute('''CREATE TABLE acer(
#                 modul   VARCHAR(200),
#                 price   FLOAT,
#                 score   FLOAT
#                 );''')
# sql.execute('''CREATE TABLE apple(
#                 modul   VARCHAR(200),
#                 price   FLOAT,
#                 score   FLOAT
#                 );''')


#connecting to DigiKala
service = Service('D:\DigiKala\chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome()
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


# 1A) Apple page
apllebutton = WebDriverWait(driver, 30).until(EC.presence_of_element_located
                                                ((By.XPATH, '//*[@id="__next"]/div[1]/div[3]/div[3]/'
                                                            'div[5]/div/div[2]/span[1]/a/div')))
driver.execute_script("arguments[0].click();", apllebutton)



# 1B) Sorting
mostexpencive = WebDriverWait(driver, 40).until(EC.presence_of_element_located
                                                ((By.XPATH, '//*[@id="ProductListPagesWrapper"]/'
                                                            'section[1]/div[1]/div/div/div/div[2]/'
                                                            'span[6]'))).click()


# 1C) Available products
availablebutton = WebDriverWait(driver, 40).until(EC.presence_of_element_located
                                                ((By.XPATH, '//*[@id="ProductListPagesWrapper"]/'
                                                            'section[2]/div/div/div[1]/div[7]/div/'
                                                            'div[2]/div/div/label[2]/span[2]')))
driver.execute_script("arguments[0].click();", availablebutton)



# 1D) Scraping data
modullist = WebDriverWait(driver, 40).until(EC.presence_of_all_elements_located
                                            ((By.CLASS_NAME, 'ellipsis-2 text-body2-strong color-700'
                                                             ' styles_VerticalProductCard__productTitle'
                                                             '__6zjjN')






