import selenium

from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

# 입력 데이터 받는 부분
quality = int(input("원하는 품질을 0, 10...80, 90 중 선택하여 입력해주세요: ")) // 10 + 1
check = 0
while not check:
    feature1 = int(input("치명 악세서리의 개수를 입력해주세요, ex)목걸이, 반지 2개, 귀걸이 2개가 치명에 해당된다면 5, 해당사항이 없으면 0입니다: "))
    feature2 = int(input("신속 악세서리의 개수를 입력해주세요, ex)목걸이에만 신속이 포함된다면 1, 해당사항이 없으면 0입니다: "))
    feature3 = int(input("특화 악세서리의 개수를 입력해주세요, ex)목걸이, 반지 1개, 귀걸이 1개가 특화에 해당된다면 3, 해당사항이 없으면 0입니다: "))
    check = int(input(f"치명 악세서리의 개수가 {feature1}개, 신속 악세서리의 개수가 {feature2}개,"
                      f" 특화 악세서리의 개수가 {feature3}개가 맞다면 1을,"
                      f" 다시 입력하고 싶으시다면 0을 입력해주세요: "))
print("시간이 좀 걸립니다, 잠시 기다려주세요...")

driver = webdriver.Chrome('chromedriver')
driver.implicitly_wait(5)

driver.get(url='https://lostark.game.onstove.com/Auction')

search_box = driver.find_element_by_id('txtItemName')

# driver.find_element_by_xpath('').click()
driver.find_element_by_xpath('//*[@id="selItemGrade"]/div[1]').click()
driver.find_element_by_xpath('//*[@id="selItemGrade"]/div[2]/label[7]').click()
driver.find_element_by_xpath('//*[@id="selItemTier"]/div[1]').click()
driver.find_element_by_xpath('//*[@id="selItemTier"]/div[2]/label[4]').click()
driver.find_element_by_xpath('//*[@id="lostark-wrapper"]/div/main/div/div[3]/div[2]/form/fieldset/div/div[5]/button[2]').click()
driver.implicitly_wait(5)

driver.find_element_by_xpath('//*[@id="selCategoryDetail"]/div[1]').click()
driver.find_element_by_xpath('//*[@id="selCategoryDetail"]/div[2]/label[10]').click()
# 품질을 입력받는다는 가정
driver.find_element_by_xpath('//*[@id="modal-deal-option"]/div/div/div[1]/div[1]/table/tbody/tr[4]/td[2]/div/div[1]').click()
driver.find_element_by_xpath(f'//*[@id="modal-deal-option"]/div/div/div[1]/div[1]/table/tbody/tr[4]/td[2]/div/div[2]/label[{quality}]').click()

# driver.close()
