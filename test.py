from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
