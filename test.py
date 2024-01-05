from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
chrome = webdriver.Chrome(options=options)

chrome.get('https://pardus.at/')
assert 'Free Browser Game' in chrome.title
