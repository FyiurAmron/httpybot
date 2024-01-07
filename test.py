import sys
import time
import datetime
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions

MIN_APS = 4200

options = ChromeOptions()
options.headless = True
for arg in [
  '--headless=new',
  '--use-angle=disabled',
  '--disable-gpu',
  '--disable-gpu-sandbox',
  '--disable-extensions',
  '--disable-infobars',
  '--disable-notifications',
  '--disable-dev-shm-usage',
  '--start-maximized',
  '--no-sandbox'
]:
  options.add_argument(arg)

chrome = webdriver.Chrome(options=options)

def now():
  return datetime.datetime.now()

def human_delay():
  time.sleep(random.randint(1,3))

def switch_to_frame(frame_id):
  chrome.switch_to.default_content()
  chrome.switch_to.frame(frame_id)
  log( f'switched frame to "{frame_id}"' )

def log(text):
  print( f'{now()}: {text}' )  

def wait_until(until_condition):
  return WebDriverWait(chrome, 10).until(until_condition)

def human_form_fill(name, text):
  el = wait_until(EC.presence_of_element_located((By.NAME, name)))
  human_delay()
  el.send_keys(text)
  log( f'sent keys "{text}" to form field "{name}"' )   

def human_click(by, value, log_msg):
  el = wait_until(EC.presence_of_element_located((by, value)))
  human_delay()
  el.click()
  log( f'clicked {log_msg}' ) 

def human_link_click(link_text):
  human_click(By.LINK_TEXT, link_text, f'link "{link_text}"')

def human_selector_click(css_selector):
  human_click(By.CSS_SELECTOR, css_selector, f'CSS elem "{css_selector}"')

def human_menu_click(target_page):
  switch_to_frame('menu')
  human_click(By.CSS_SELECTOR, f'.menubutton > a[href="{target_page}.php"]', f'menu link "{target_page}"')
  switch_to_frame('main')

def get_text_by_selector(css_selector):
  return wait_until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector))).text

def get_int_by_selector(css_selector):
  return int(get_text_by_selector(css_selector))

# note that form.submit() is generally bad idea, and Pardus showcases that very effectively:
# e.g. direct form submit doesn't work due to JS onClick feeding password's MD5 hash to a hidden input field etc.

chrome.get('https://pardus.at/')
log(chrome.title)
assert 'Free Browser Game' in chrome.title

human_form_fill('acc', 'spamove@gmail.com')
human_form_fill('pw', 'p4rdu5')
human_selector_click('.loginbutton')

wait_until(EC.title_is('Pardus'))
assert chrome.current_url == 'https://orion.pardus.at/game.php'
log( 'login successful' )

switch_to_frame('main')

apsleft = get_int_by_selector('#apsleft')
log( f'APs left: {apsleft}' )
if ( apsleft < MIN_APS ):
  log( f'less than minimum {MIN_APS} APs, doing nothing and exiting...' )
  chrome.quit()
  sys.exit()

# ship may be or may be not docked

launch_ship = chrome.find_elements(By.CSS_SELECTOR, '[value="Launch Ship"]')
if len(launch_ship) > 0:
  log( 'ship is docked, commencing launch...' )
  human_delay()
  launch_ship[0].click()
  switch_to_frame('main') # probably required due to focus loss
  log( 'ship launched' )

human_link_click('Land')
human_link_click('Black Market')
human_link_click('Hack Information')

human_form_fill('lookup_name', 'a')
human_selector_click('[name="name_lookup"]')

while apsleft >= MIN_APS:
  log( f'APs left ({apsleft}) >= MIN_APS ({MIN_APS}), proceeding...' )
  human_selector_click('#doHackButton')
  switch_to_frame('msgframe')
  message = get_text_by_selector('body > table > tbody > tr > td[align="center"] > table > tbody > tr > td:nth-child(2) > font')
  log(message)
  switch_to_frame('main')
  apsleft = get_int_by_selector('table.messagestyle > tbody > tr > td > b')

log( f'APs left ({apsleft}) < MIN_APS ({MIN_APS}), exiting...' )
chrome.quit() # not really needed, but added for clarity
