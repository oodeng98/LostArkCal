import selenium
import pandas as pd

from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


driver = webdriver.Chrome('chromedriver')
driver.implicitly_wait(5)

driver.get(url='https://lostark.game.onstove.com/Market')

search_box = driver.find_element_by_id('txtItemName')

search_box.send_keys('진주')  # 키보드 입력해주는 코드
search_box.send_keys(Keys.RETURN)

name = driver.find_element_by_xpath('//*[@id="tbodyItemList"]/tr[1]/td[3]/div/em')
print(name.text)



