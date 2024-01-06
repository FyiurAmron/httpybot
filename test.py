from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.headless = True
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
options.add_argument('--disable-infobars')
options.add_argument('--disable-notifications')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--start-maximized')
options.add_argument('--headless')
options.add_argument('--no-sandbox')

chrome = webdriver.Chrome(options=options)

chrome.get('https://pardus.at/')
print(chrome.title)
assert 'Free Browser Game' in chrome.title
chrome.find_element(By.NAME, 'acc').send_keys('spamove@gmail.com')
chrome.find_element(By.NAME, 'pw').send_keys('qzwxec')
# form submit doesn't work due to JS magic feeding password's MD5 hash to a hidden input field
chrome.find_element(By.CLASS_NAME, 'loginbutton').click()

WebDriverWait(chrome, 10).until(EC.title_is('Pardus'))
assert chrome.current_url == 'https://orion.pardus.at/game.php'

chrome.switch_to.frame('main')

apsleft = chrome.find_element(By.ID, 'apsleft').text
print( "APs left: (before)", apsleft )

chrome.find_element(By.LINK_TEXT, 'Land').click()

WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Black Market'))).click()

WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Hack Information'))).click()

WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Return to the Black Market')))
chrome.find_element(By.NAME, 'lookup_name').send_keys('Cras')
chrome.find_element(By.NAME, 'name_lookup').submit()

WebDriverWait(chrome, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Hack"]'))).click()

chrome.switch_to.frame('msgframe')

messageBox = WebDriverWait(chrome, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > table > tbody > tr > td[align="center"] > table > tbody > tr > td:nth-child(2) > font')))

print(messageBox.text)

chrome.switch_to.frame('menu')

chrome.find_element(By.CSS_SELECTOR, 'a[href="main.php"]').click()

chrome.switch_to.frame('main')

apsleft = WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.ID, 'apsleft')))
print( "APs left: (after)", apsleft )
