from selenium import webdriver


browser = webdriver.Firefox()

browser.get("http://mysite.com:8000")

assert "The install worked successfully! Congratulations!" == browser.title
