import selenium
import pandas as pd
import time
import math

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
    time.sleep(0.3)
    try:
        ret = searchbox.find_element_by_xpath(xpath)
    except selenium.common.exceptions.NoSuchElementException:
        ret = 1000  # 거래소에 존재하지 않는 경우, 인기가 없는 아이템이라는 뜻이므로 가격을 그냥 왕창 올려서 우선순위에서 제외되게 함
        # 근데 지금은 안되는중
    searchbox.clear()
    time.sleep(0.3)
    if type(ret) != int:
        return int(ret.text)
    return ret


def find_all_price():
    options = webdriver.ChromeOptions()  # 크롬 옵션 객체 생성
    options.add_argument('headless')  # headless 모드 설정

    driver = webdriver.Chrome('chromedriver', options=options)
    driver.implicitly_wait(5)

    driver.get(url='https://lostark.game.onstove.com/Market')

    search_box = driver.find_element_by_id('txtItemName')

    xpath = '//*[@id="tbodyItemList"]/tr/td[4]/div/em'
    # 아이템 별 판매개수도 넣어줘야 계산할 수 있음
    item_dict = {'회복약': 1, '고급 회복약': 1, '정령의 회복약': 1, '빛나는 정령의 회복약': 1, '각성 물약': 1, '만능 물약': 1,
                 '빛나는 만능 물약': 1, '보호 물약': 1, '빛나는 보호 물약': 1, '천둥 물약': 1, '빛나는 천둥 물약': 1,
                 '아드로핀 물약': 1, '시간 정지 물약': 1, '성스러운 폭탄': 1, '빛나는 성스러운 폭탄': 1, '부식 폭탄': 1,
                 '빛나는 부식 폭탄': 1, '수면 폭탄': 1, '빛나는 수면 폭탄': 1, '파괴 폭탄': 1, '빛나는 파괴 폭탄': 1,
                 '페로몬 폭탄': 1, '섬광 수류탄': 1, '빛나는 섬광 수류탄': 1, '화염 수류탄': 1, '빛나는 화염 수류탄': 1,
                 '냉기 수류탄': 1, '빛나는 냉기 수류탄': 1, '전기 수류탄': 1, '빛나는 전기 수류탄': 1, '암흑 수류탄': 1,
                 '빛나는 암흑 수류탄': 1, '회오리 수류탄': 1, '빛나는 회오리 수류탄': 1, '점토 수류탄': 1, '빛나는 점토 수류탄': 1,
                 '위장 로브': 1, '빛나는 위장 로브': 1, '은신 로브': 1, '빛나는 은신 로브': 1, '신속 로브': 1, '빛나는 신속 로브': 1,
                 '신호탄': 1, '빛나는 신호탄': 1, '도발 허수아비': 1, '빛나는 도발 허수아비': 1, '모닥불': 1, '빛나는 모닥불': 1,
                 '진군의 깃발': 1, '빛나는 진군의 깃발': 1, '성스러운 부적': 1, '빛나는 성스러운 부적': 1, '루테란의 나팔': 1,
                 '정비소 이동 포탈 주문서': 1, '칼다르 융화 재료': 1,
                 '하급 오레하 융화 재료': 1, '중급 오레하 융화 재료': 1, '상급 오레하 융화 재료': 1}
    """
     '[일품] 장인의 노릇한 꼬치구이': 10, '[일품] 장인의 매콤한 스튜': 10,
                 '[일품] 장인의 폭신한 오믈렛': 10, '[일품] 장인의 마늘 스테이크 정식': 10,
                 '[일품] 달인의 바삭한 꼬치구이': 10, '[일품] 달인의 달콤한 스튜': 10, '[일품] 달인의 부드러운 오믈렛': 10,
                 '[일품] 장인의 버터 스테이크 정식': 10, '[일품] 명인의 쫄깃한 꼬치구이': 10, '[일품] 명인의 짭짤한 스튜': 10,
                 '[일품] 명인의 촉촉한 오믈렛': 10, '[일품] 명인의 허브 스테이크 정식': 10, 
    """
    # 정식 들어가면 10개단위
    ret = {}
    for i in item_dict:
        ret[i] = find_price(search_box, xpath, i) / item_dict[i]
    material_dict = {'수줍은 들꽃': 10, '화사한 들꽃': 10, '투박한 버섯': 100, '싱싱한 버섯': 10, '화려한 버섯': 10,
                     '부드러운 목재': 10, '튼튼한 목재': 10,
                     '묵직한 철광석': 10, '단단한 철광석': 10,
                     '다듬은 생고기': 10, '질긴 가죽': 10, '칼다르 두툼한 생고기': 10, '오레하 두툼한 생고기': 10, '수렵의 결정': 10,
                     '붉은 살 생선': 10, '자연산 진주': 10, '칼다르 태양 잉어': 10, '오레하 태양 잉어': 10, '낚시의 결정': 10,
                     '고대 유물': 100, '희귀한 유물': 10, '칼다르 유물': 10, '오레하 유물': 10, '고고학의 결정': 10}
    # 거래소에 존재하지 않는 매물은 어떻게 예외처리해주지?
    overlap_list = {'들꽃': 100, '목재': 100, '철광석': 100, '두툼한 생고기': 100, '생선': 100}

    for i in material_dict:
        ret[i] = find_price(search_box, xpath, i) / material_dict[i]
    driver.find_element_by_xpath(
        '//*[@id="lostark-wrapper"]/div/main/div/div[2]/div[2]/form/fieldset/div/div[3]/div[2]/div/div[1]').click()
    driver.find_element_by_xpath(
        '//*[@id="lostark-wrapper"]/div/main/div/div[2]/div[2]/form/fieldset/div/div[3]/div[2]/div/div[2]/label[2]').click()
    for i in overlap_list:
        ret[i] = find_price(search_box, xpath, i) / overlap_list[i]

    driver.switch_to.window(driver.window_handles[0])
    driver.close()
    return ret


def find_production_price(material_price_list, discount):
    data = pd.read_excel('영지 제작 아이템.xlsx')
    data = data.fillna(0)
    data = data.to_dict('index')
    total_production_cost = {}
    total_production_count = {}
    for i in range(len(data)):
        recipe = data[i]
        name = ''
        count = 0
        time_taken = 0
        energy = 0
        cost = 0
        for j in recipe:
            if j == '아이템':
                name = recipe[j]
                if "빛나는" in name:
                    temp = name.replace("빛나는 ", "")
                    cost += min(material_price_list[temp] * 3, total_production_cost[temp])
                # print(recipe[j], end=' ')
                continue
            elif j == '수량':
                count = recipe[j]
                total_production_count[name] = count
            elif j == '소요 시간':
                time_taken = recipe[j]
            elif j == '활동력':
                energy = recipe[j]
            elif j == '비용':
                cost += recipe[j] * (100 - discount) // 100
            elif recipe[j] != 0:
                # print(j, recipe[j], end=' ')
                cost += material_price_list[j] * recipe[j]
        if name in total_production_cost:
            total_production_cost[name] = min(total_production_cost[name], round(cost, 2))
        else:
            total_production_cost[name] = round(cost, 2)
    return total_production_cost, total_production_count


def find_benefit(production_cost, production_count, sell_cost):
    item_dict = {'회복약': 1, '고급 회복약': 1, '정령의 회복약': 1, '빛나는 정령의 회복약': 1, '각성 물약': 1, '만능 물약': 1,
                 '빛나는 만능 물약': 1, '보호 물약': 1, '빛나는 보호 물약': 1, '천둥 물약': 1, '빛나는 천둥 물약': 1,
                 '아드로핀 물약': 1, '시간 정지 물약': 1, '성스러운 폭탄': 1, '빛나는 성스러운 폭탄': 1, '부식 폭탄': 1,
                 '빛나는 부식 폭탄': 1, '수면 폭탄': 1, '빛나는 수면 폭탄': 1, '파괴 폭탄': 1, '빛나는 파괴 폭탄': 1,
                 '페로몬 폭탄': 1, '섬광 수류탄': 1, '빛나는 섬광 수류탄': 1, '화염 수류탄': 1, '빛나는 화염 수류탄': 1,
                 '냉기 수류탄': 1, '빛나는 냉기 수류탄': 1, '전기 수류탄': 1, '빛나는 전기 수류탄': 1, '암흑 수류탄': 1,
                 '빛나는 암흑 수류탄': 1, '회오리 수류탄': 1, '빛나는 회오리 수류탄': 1, '점토 수류탄': 1, '빛나는 점토 수류탄': 1,
                 '위장 로브': 1, '빛나는 위장 로브': 1, '은신 로브': 1, '빛나는 은신 로브': 1, '신속 로브': 1, '빛나는 신속 로브': 1,
                 '신호탄': 1, '빛나는 신호탄': 1, '도발 허수아비': 1, '빛나는 도발 허수아비': 1, '모닥불': 1, '빛나는 모닥불': 1,
                 '진군의 깃발': 1, '빛나는 진군의 깃발': 1, '성스러운 부적': 1, '빛나는 성스러운 부적': 1, '루테란의 나팔': 1,
                 '정비소 이동 포탈 주문서': 1, '칼다르 융화 재료': 1,
                 '하급 오레하 융화 재료': 1, '중급 오레하 융화 재료': 1, '상급 오레하 융화 재료': 1}
    """
     '[일품] 장인의 노릇한 꼬치구이': 10, '[일품] 장인의 매콤한 스튜': 10,
                 '[일품] 장인의 폭신한 오믈렛': 10, '[일품] 장인의 마늘 스테이크 정식': 10,
                 '[일품] 달인의 바삭한 꼬치구이': 10, '[일품] 달인의 달콤한 스튜': 10, '[일품] 달인의 부드러운 오믈렛': 10,
                 '[일품] 장인의 버터 스테이크 정식': 10, '[일품] 명인의 쫄깃한 꼬치구이': 10, '[일품] 명인의 짭짤한 스튜': 10,
                 '[일품] 명인의 촉촉한 오믈렛': 10, '[일품] 명인의 허브 스테이크 정식': 10, 
    """
    ret = {}
    for i in item_dict:
        ret[i] = int(production_count[i] * int(sell_cost[i] * 0.95) - production_cost[i])
    df = sorted(list(zip(ret.keys(), ret.values())), key=lambda x: x[1], reverse=True)
    df = pd.DataFrame(df, columns=['Name', 'Benefit'])
    print(df)
    return ret


if __name__ == "__main__":
    discount_rate = int(input("영지 특수 제작 할인률을 입력해주세요: "))
    item_price_dict = find_all_price()
    item_production_price_dict, item_production_count_dict = find_production_price(item_price_dict, discount_rate)
    find_benefit(item_production_price_dict, item_production_count_dict, item_price_dict)
    # 특수 제작 외에도 물약 할인률이라던지 그런것도 입력받는게 좋겠다


