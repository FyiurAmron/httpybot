import time
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions

REQ_APS = 100 # lame hack

options = ChromeOptions()
options.headless = True
for arg in [
  '--headless=new',
  '--use-angle=disabled',
  '--use-gl=swiftshader',
  '--disable-gpu',
  '--disable-gpu-sandbox',
  '--disable-extensions',
  '--disable-infobars',
  '--disable-notifications',
  '--disable-dev-shm-usage',
  '--start-maximized',
  '--no-sandbox'
  '--headless=new',
]:
  options.add_argument(arg)

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
now = datetime.datetime.now()
print(now)

chrome.switch_to.default_content()
chrome.switch_to.frame('main')

apsleft = chrome.find_element(By.ID, 'apsleft').text
apsleft = int(apsleft)
print( "APs left: (before)", apsleft )
if ( apsleft < REQ_APS ):
  print( "less than required", REQ_APS, "APs, terminating..." )
  chrome.quit()
  sys.exit()

chrome.find_element(By.LINK_TEXT, 'Land').click()

WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Black Market'))).click()

WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Hack Information'))).click()

WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Return to the Black Market')))
chrome.find_element(By.NAME, 'lookup_name').send_keys('Cras')
chrome.find_element(By.NAME, 'name_lookup').submit()

WebDriverWait(chrome, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Hack"]'))).click()

chrome.switch_to.default_content()
chrome.switch_to.frame('msgframe')

messageBox = WebDriverWait(chrome, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > table > tbody > tr > td[align="center"] > table > tbody > tr > td:nth-child(2) > font')))

print(messageBox.text)

now = datetime.datetime.now()
print(now)

chrome.switch_to.default_content()
chrome.switch_to.frame('menu')

chrome.find_element(By.CSS_SELECTOR, 'a[href="main.php"]').click()

chrome.switch_to.default_content()
chrome.switch_to.frame('main')

apsleft = WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.ID, 'apsleft')))
apsleft = int(apsleft)
print( "APs left: (after)", apsleft.text )

chrome.quit() # not really needed, but added for clarity

