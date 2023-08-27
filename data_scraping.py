# I) Adding Library And Package

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


# II) Functions

# 1.Clicking On An Element
# This function operates by obtaining the XPath of a designated element and then employing a waiting 
# period of 40 seconds to ensure the full loading of the said element. Subsequently, it proceeds to 
# execute the clicking action on the targeted element.

def clicking(xpath):
    button = WebDriverWait(driver, 40).until(EC.presence_of_element_located
                                         ((By.XPATH, xpath)))
    driver.execute_script("arguments[0].click();", button)



# 2.Hover Mouse Action
# This function operates by obtaining the XPath of a designated element and then employing a waiting 
# period of 40 seconds to ensure the full loading of the said element. Subsequently, it proceeds to 
# execute the mouse hovering action on the targeted element.

def hover(xpath):
    button = WebDriverWait(driver, 40).until(EC.presence_of_element_located
                                         ((By.XPATH, xpath)))
    hover = ActionChains(driver).move_to_element(button)
    hover.perform()



# 3.Database Table Creation

def table_creation(table_name):
    cursor.execute('''CREATE TABLE IF NOT EXISTS {} (
                modul   VARCHAR(200),
                price   FLOAT,
                score   FLOAT
                );''' .format(table_name))
    
    
    


# 4.Scroll To Bottom

def scroll_to_bottom(scroll_pause_time):
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        time.sleep(10)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


# 5.Move Year To End
# The laptop models are presently featuring the release year at the onset of their designations;
# However, it is imperative that the year be positioned at the conclusion of the model name string.

def move_year_to_end(text):

    # Checking if string includes year

    year_pattern = re.compile(r'\b(20\d{2})\b')
    match = year_pattern.search(text)
    if match:

        # If it has, relocate it to the termination of said string

        text_without_year = year_pattern.sub('', text).strip()
        new_text = f"{text_without_year} {match.group(1)}"
        return new_text
    return text



# 6.Check If A String Has Arabic Number Or Not
# Creating a list of Arabic numerals, traversing a given string, and subsequently verifying the occurrence
# of matches between the enumerated numerals and the content of the string.

def has_arabic_numbers(text):
    eastern_arabic_numerals = '۰۱۲۳۴۵۶۷۸۹'
    resault = False
    for char in text:
        if char in eastern_arabic_numerals or char == ',':
            resault = True
        else:
            return False
    return resault



# 7.Changing Arabic Numbers To English Numbers
# We iterate through the input string, associating each character with one of the elements from a set
# containing Arabic numerals. Subsequently, we index the specified Arabic numeral with its corresponding English
# numeral. These matched English numerals are then replaced within a new string.

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



# 8.Sorting Products

def sorting():
    
    # Sorting the products from the most expensive to the cheapest
    clicking('//*[@id="ProductListPagesWrapper"]/section[1]/div[1]/div/div/div/div[2]/span[6]')
    
    # Showing only available products
    clicking('//*[@id="ProductListPagesWrapper"]/section[2]/div/div/div[1]/div[7]/div/div[2]/div/div/label[2]/span[2]')




# 9.Model Scarping
# Finding the elements with tag name h3 AKA laptops' model

def model_scraping():
    scroll_to_bottom(15)
    models = []
    models = driver.find_elements(By.TAG_NAME, 'h3')
    models.pop()
    
    return models



# 10.Scraping And Cleaning Prices
# Identify elements with the tag name "span". Among these "span" tags, the ones containing Arabic numerals correspond to 
# the prices of laptops. By using the "has Arabic number" function, we can selectively gather the prices and compile them into 
# the list. Subsequently, utilizing the "Arabic to English" function, we can convert the Arabic numerals to their
#  English counterparts.

def price_scraping():
    pricelist = []
    prices = driver.find_elements(By.TAG_NAME, 'span')
    for x in prices:
        if has_arabic_numbers(x.text) and ',' in x.text:
            pricelist.append(arabic_to_english_numbers(x.text))
        elif x.text == 'ناموجود':
            pricelist.append(None)
    
    return pricelist



# 11.Scraping And Cleaning Scores
# To scraping the scores of laptops, it is necessary to sequentially click on each element within the 'models' list,
# which will lead to the opening of individual pages for each laptop. Subsequently, the scores are to be extracted
# from the respective pages. If the score element is available, it should be collected and converted to an English numeral 
# using the "Arabic to English" function. In the event that no score is available, indicating that no ratings have 
# been assigned to the laptop, a value of 0 should be appended.

def score_scraping(models):
    scorelist = []
    for i in range(len(models)):
        xpath = '//*[@id="ProductListPagesWrapper"]/section[1]/div[2]/div[{}]/a/div/article/div[2]/div[2]/div[3]/div[2]/p'.format(i+1)
        try:
            score = driver.find_element(By.XPATH, xpath)
            scorelist.append(arabic_to_english_numbers(score.text))
        except:
            scorelist.append(None)

    
    return scorelist



# 12.Adding Data To The Database

def add_to_dataset(brand, modellist, pricelist, scorelist):
    for (i, j, k) in zip(modellist, pricelist, scorelist):
        cursor.execute(
            '''INSERT INTO {} (modul, price, score) VALUES (%s, %s, %s);'''.format(brand), (i,j,k,)
        )



# 13. Checking Element Existence

def element_existence(xpath):
    try:
        element  = WebDriverWait(driver, 10).until(EC.presence_of_element_located
                                         ((By.XPATH, xpath)))
        return True
    except:
        return False




# III) Connecting Database And Table Creation

conn = psycopg2.connect(database='digikala',
                        host="localhost",
                        port=5432,
                        user="postgres",
                        password="1234")
conn.autocommit = True
cursor = conn.cursor()



# IV) Connecting To DigiKala

service = Service("D:\DigiKala\chromedriver.exe")
options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.binary_location = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
driver = webdriver.Chrome(options=options, service=service)
driver.get('https://www.digikala.com/')
driver.maximize_window()
resp = requests.get('https://www.digikala.com/')
html = resp.text
bs = BeautifulSoup(html, 'html.parser')



# V) Data Scraping
# Sidmenu
# Opening the side-menu by holding the mouse over it

hover ('//*[@id="base_layout_desktop_fixed_header"]/header/nav/div[1]/div[1]'
       '/div[1]/div/span') # Side-menu Xpath



# Digital Devices
# Opening the digital products menu

hover ('//*[@id="base_layout_desktop_fixed_header"]/header/nav/div[1]/'
       'div[1]/div[1]/div/div/div/div[1]/a[2]') # Digital Devices Xpath


# Laptops
# Opening the Laptop page

clicking ('//*[@id="base_layout_desktop_fixed_header"]/header/nav/div[1]'
          '/div[1]/div[1]/div/div/div/div[2]/div[2]/'
          'div[1]/ul/a[6]') # Laptop's button Xpath




# 1) Apple
# 1A) Creating Apple Products Table


table_creation('apple')



# 1B) Apple Page
# Clicking on Apple products button

clicking ('//*[@id="__next"]/div[1]/div[3]/div[3]/div[5]'
          '/div/div[2]/span[1]/a/div') # Apple's button Xpath




# 1C) Sorting
# Sorting the products from the most expensive to the cheapest and showing only available products

sorting()



# 1D) Scraping And Cleaning Models
# The laptop model names consist of the phrase "لپ تاپ اپل مدل x اینچی," and our specific requirement is to extract 
# only the value denoted by 'x.' Using Regex, we can eliminate the surplus portion. Subsequently, 
# by utilizing the "move year to end" function, the release year section is repositioned to the end of the string.

persian_part = r'[آ-ی]'
models = model_scraping()
modellist = [(re.sub(persian_part, '', text.text)) for text in models]



# 1E) Scraping Prices

pricelist = price_scraping()



# 1F) Scraping Scores

scorelist = score_scraping(models)



# 1G) Adding Data To The Database

add_to_dataset('apple', modellist, pricelist, scorelist)



# Back To The Laptops Page
driver.back()

# 2) Acer
# 2A) Creating Acer Products Table

table_creation('acer')



# 2B) Acer Page
# Clicking on Acer products button

clicking ('//*[@id="__next"]/div[1]/div[3]/div[3]/div'
          '[5]/div/div[2]/span[2]/a') # Acer's button Xpath




# 2C) Sorting
# Sorting the products from the most expensive to the cheapest and showing only available products

sorting()



# 2D) Scraping And Cleaning Models
# The laptop model names consist of the phrase "لپ تاپ ایسر مدل x اینچی - کاستوم شده" and our specific requirement is to extract 
# only the value denoted by 'x.' Using Regex, we can eliminate the surplus portion.

persian_part = r'[آ-ی]'
models = model_scraping()
modellist = [(re.sub(persian_part, '', text.text)) for text in models]




# 2E) Scraping Prices

pricelist = price_scraping()



# 2F) Scraping Scores
scorelist = score_scraping(models)



# 2G) Adding Data To The Database

add_to_dataset('acer', modellist, pricelist, scorelist)



# Back To The Laptops Page
driver.back()



# 3) Asus
# 3A) Creating Asus Products Table

table_creation('asus')



# 3B) Asus Page
# Clicking on Asus products button

clicking ('//*[@id="__next"]/div[1]/div[3]/div[3]/div[5]'
          '/div/div[2]/span[3]/a') # Asus's button Xpath




# 3C) Sorting
# Sorting the products from the most expensive to the cheapest and showing only available products

sorting()



# 3D) Scraping And Cleaning Models
# The laptop model names consist of the phrase "لپ تاپ ایسوس مدل x اینچی - کاستوم شده" and our specific requirement is to extract 
# only the value denoted by 'x.' Using Regex, we can eliminate the surplus portion.

persian_part = r'[آ-ی]'
first_page = '//*[@id="ProductListPagesWrapper"]/section[1]/div[2]/div[201]/div/div[3]'
other_pages = '//*[@id="ProductListPagesWrapper"]/section[1]/div[2]/div[21]/div/div[3]'
modellist = []
pricelist = []
scorelist = []
while True:
    
    model_elements = model_scraping()
    modellist.append(re.sub(persian_part, '', i.text)for i in model_elements)

    # 3E) Scraping Prices
    
    price_elements = price_scraping()
    pricelist.append(j for j in price_elements)
    
    # 3F) Scraping Scores
    
    score_elements = score_scraping(model_elements)
    scorelist.append(k for k in score_elements)
    
    if element_existence(first_page):
        clicking(first_page)
        
    elif element_existence(other_pages):
        clicking(other_pages)
        
    else:
        break



# 3G) Adding Data To The Database

add_to_dataset('asus', modellist, pricelist, scorelist)



# Back To The Laptops Page
driver.back()



# 4) HP
# 4A) Creating HP Products Table

table_creation('hp')



# 4B) HP Page
# Clicking on HP products button

clicking ('//*[@id="__next"]/div[1]/div[3]/div[3]/div[5]'
          '/div/div[2]/span[4]/a') # HP's button Xpath




# 4C) Sorting
# Sorting the products from the most expensive to the cheapest and showing only available products

sorting()



# 4D) Scraping And Cleaning Models
# The laptop model names consist of the phrase "لپ تاپ اچ پی مدل x اینچی - کاستوم شده" and our specific requirement is to extract 
# only the value denoted by 'x.' Using Regex, we can eliminate the surplus portion.

persian_part = r'[آ-ی]'
models = model_scraping()
modellist = [(re.sub(persian_part, '', text.text)) for text in models]




# 4E) Scraping Prices

pricelist = price_scraping()



# 4F) Scraping Scores
scorelist = score_scraping(models)



# 4G) Adding Data To The Database

add_to_dataset('hp', modellist, pricelist, scorelist)



# Back To The Laptops Page
driver.back()



# 5) Lenovo
# 5A) Creating Lenovo Products Table

table_creation('lenovo')



# 5B) Lenovo Page
# Clicking on Lenovo products button

clicking ('//*[@id="__next"]/div[1]/div[3]/div[3]/div[5]'
          '/div/div[2]/span[5]/a') # Lenovo's button Xpath




# 5C) Sorting
# Sorting the products from the most expensive to the cheapest and showing only available products

sorting()



# 5D) Scraping And Cleaning Models
# The laptop model names consist of the phrase "لپ تاپ لنوو مدل x اینچی - کاستوم شده" and our specific requirement is to extract 
# only the value denoted by 'x.' Using Regex, we can eliminate the surplus portion.

persian_part = r'[آ-ی]'
first_page = '//*[@id="ProductListPagesWrapper"]/section[1]/div[2]/div[201]/div/div[3]'
other_pages = '//*[@id="ProductListPagesWrapper"]/section[1]/div[2]/div[21]/div/div[3]'
modellist = []
pricelist = []
scorelist = []
while True:
    
    model_elements = model_scraping()
    modellist.append(re.sub(persian_part, '', i.text)for i in model_elements)

    # 5E) Scraping Prices
    
    price_elements = price_scraping()
    pricelist.append(j for j in price_elements)
    
    # 5F) Scraping Scores
    
    score_elements = score_scraping(model_elements)
    scorelist.append(k for k in score_elements)
    
    if element_existence(first_page):
        clicking(first_page)
        
    elif element_existence(other_pages):
        clicking(other_pages)
        
    else:
        break



# 5G) Adding Data To The Database

add_to_dataset('lenovo', modellist, pricelist, scorelist)



# # Back To The Laptops Page
# driver.back()



# 6) MSI
# 6A) Creating MSI Products Table

table_creation('msi')



# 6B) MSI Page
# Clicking on MSI products button

clicking ('//*[@id="__next"]/div[1]/div[3]/div[3]/div[5]'
          '/div/div[2]/span[6]/a') # MSI's button Xpath




# 6C) Sorting
# Sorting the products from the most expensive to the cheapest and showing only available products

sorting()



# 6D) Scraping And Cleaning Models
# The laptop model names consist of the phrase "لپ تاپ ام اس آی مدل x اینچی - کاستوم شده" and our specific requirement is to extract 
# only the value denoted by 'x.' Using Regex, we can eliminate the surplus portion.

persian_part = r'[آ-ی]'
models = model_scraping()
modellist = [(re.sub(persian_part, '', text.text)) for text in models]




# 6E) Scraping Prices

pricelist = price_scraping()



# 6F) Scraping Scores
scorelist = score_scraping(models)



# 6G) Adding Data To The Database

add_to_dataset('msi', modellist, pricelist, scorelist)



# Back To The Laptops Page
driver.back()


conn.commit()
conn.close()
