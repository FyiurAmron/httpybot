from selenium import webdriver

options = ChromeOptions()
options.headless = True
chrome = webdriver.Chrome(options=options)

chrome.get('https://pardus.at/')
assert 'Free Browser Game' in chrome.title
