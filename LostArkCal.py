import selenium
import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


def find_price(searchbox, xpath, target):
    searchbox.send_keys(target)
    searchbox.send_keys(Keys.RETURN)
    time.sleep(1)
    ret = searchbox.find_element_by_xpath(xpath)
    searchbox.clear()
    time.sleep(1.5)
    return ret.text


def find_all_price():
    driver = webdriver.Chrome('chromedriver')
    driver.implicitly_wait(5)

    driver.get(url='https://lostark.game.onstove.com/Market')

    search_box = driver.find_element_by_id('txtItemName')

    xpath = '//*[@id="tbodyItemList"]/tr/td[4]/div/em'
    target_list = ['수줍은 들꽃', '화사한 들꽃', '투박한 버섯', '싱싱한 버섯', '화려한 버섯',
                   '부드러운 목재', '튼튼한 목재',
                   '묵직한 철광석', '단단한 철광석',
                   '다듬은 생고기', '질긴 가죽', '칼다르 두툼한 생고기', '오레하 두툼한 생고기', '수렵의 결정',
                   '붉은 살 생선', '자연산 진주', '칼다르 태양 잉어', '오레하 태양 잉어', '낚시의 결정',
                   '고대 유물', '희귀한 유물', '칼다르 유물', '오레하 유물', '고고학의 결정']
    overlap_list = ['들꽃', '목재', '철광석', '두툼한 생고기', '생선']
    ret = {}
    for i in target_list:
        ret[i] = find_price(search_box, xpath, i)
    driver.find_element_by_xpath(
        '//*[@id="lostark-wrapper"]/div/main/div/div[2]/div[2]/form/fieldset/div/div[3]/div[2]/div/div[1]').click()
    driver.find_element_by_xpath(
        '//*[@id="lostark-wrapper"]/div/main/div/div[2]/div[2]/form/fieldset/div/div[3]/div[2]/div/div[2]/label[2]').click()
    for i in overlap_list:
        ret[i] = find_price(search_box, xpath, i)

    driver.switch_to.window(driver.window_handles[0])
    driver.close()

    return ret


if __name__ == "__main__":
    price_list = find_all_price()
    print(price_list)
    # 정리를 조금 해줘야 할 것 같은데 어떻게 제작 방법을 효율적으로 정리할지는 모르겠다



