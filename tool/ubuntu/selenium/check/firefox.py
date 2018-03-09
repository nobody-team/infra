# coding:utf-8
import time

from pyvirtualdisplay import Display
from selenium import webdriver

display = Display(visible=0, size=(800, 800))
display.start()
driver = webdriver.Firefox()
driver.get('https://www.google.com.sg/')
time.sleep(5)
title = driver.title
print(title.encode('utf-8'))
driver.close()
display.stop()
