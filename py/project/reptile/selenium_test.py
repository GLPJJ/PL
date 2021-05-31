from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time 
import urllib.request
import numpy as np

driver = webdriver.Chrome()
driver.get("https://www.baidu.com")



element_xw = driver.find_element_by_xpath('//*[@id="u1"]/a[1]')
element_xw.click()
time.sleep(1)
driver.back()
time.sleep(1)
driver.forward()
time.sleep(1)
driver.back()

# //*[@id="setf"]
element_szy = driver.find_element_by_xpath('//*[@id="setf"]')
element_szy.click()

# driver.window_handles 包含了当前打开的标签页
driver.switch_to.window(driver.window_handles[1]) #切换到第二个窗口
driver.close() #把当前窗口关掉