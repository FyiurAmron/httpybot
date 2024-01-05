from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://pardus.at/')
assert 'Free Browser Game' in browser.title
