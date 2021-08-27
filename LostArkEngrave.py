import selenium
import itertools
import time
import copy
from requests import Request, Session
import webbrowser
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from Hepheir.__main__ import main as search_key
from Hepheir.__main__ import QUERY


class ACCESSORY:
    def __init__(self, name):
        self.name = name
    total_data: BeautifulSoup
    effect = {}
    price_low: int
    price_buy: int


def find_price(target, zero_list):
    _target = copy.deepcopy(target)
    options = webdriver.ChromeOptions()  # 크롬 옵션 객체 생성
    options.add_argument('headless')  # headless 모드 설정

    driver = webdriver.Chrome('chromedriver', options=options)
    driver.implicitly_wait(5)

    driver.get(url='https://lostark.game.onstove.com/Market')
    driver.find_element_by_name('user_id').send_keys("oodeng98@gmail.com")
    driver.find_element_by_name('user_pwd').send_keys("lostarkengrave24")
    driver.find_element_by_xpath('//*[@id="idLogin"]/div[3]/button').click()

    search_box = driver.find_element_by_id('txtItemName')
    driver.find_element_by_xpath(
        '//*[@id="lostark-wrapper"]/div/main/div/div[2]/div[2]/form/fieldset/div/div[3]/div[2]/div/div[1]').click()
    driver.find_element_by_xpath(
        '//*[@id="lostark-wrapper"]/div/main/div/div[2]/div[2]/form/fieldset/div/div[3]/div[2]/div/div[2]/label[6]').click()

    for i in _target:
        if i in zero_list:
            _target[i] = 0
            continue
        search_box.send_keys(i)
        search_box.send_keys(Keys.RETURN)
        time.sleep(0.3)
        try:
            ret = driver.find_element_by_xpath('//*[@id="tbodyItemList"]/tr/td[3]/div/em')
        except selenium.common.exceptions.NoSuchElementException:
            ret = 100000

        search_box.clear()
        time.sleep(0.3)
        if type(ret) != int:
            _target[i] = remove_comma(ret.text)
        else:
            _target[i] = ret
    driver.quit()
    print(_target)
    return _target


def receive_input_data(engrave_dict):
    bad_engrave_dict = {"공격력 감소": 0, "공격속도 감소": 0, "방어력 감소": 0, "이동속도 감소": 0}

    print("이 프로그램은 각인 맞추기에 대한 기본적 지식이 있는 사람이 쓰는 것을 가정하고 만든 프로그램입니다.")
    print("터무니없는 어빌리티 스톤으로 33333각인을 맞춘다는 말도 안되는 경우는 체크해주지 않습니다.")
    print("현재 베타테스트 상태로 33333각인만 지원합니다.")
    print("선택과 투자, 그리고 과금은 모두 사용자의 책임입니다. 서비스 지원 업체는 해당 부분은 보상하지 않습니다.")
    while True:
        try:
            neck_qual = int(input("목걸이의 품질 하한선을 0, 10...80, 90 중 선택하여 입력해주세요: "))
            earring_qual = int(input("귀걸이의 품질 하한선을 0, 10...80, 90 중 선택하여 입력해주세요: "))
            ring_qual = int(input("반지의 품질 하한선을 0, 10...80, 90 중 선택하여 입력해주세요: "))
            if neck_qual % 10 or earring_qual % 10 or ring_qual % 10:
                raise ValueError
            neck_qual = neck_qual // 10 + 1
            earring_qual = earring_qual // 10 + 1
            ring_qual = ring_qual // 10 + 1
            break
        except ValueError:
            print("잘못 입력하셨습니다. 다시 입력해주세요: ")

    while True:
        print("모든 전투특성 입력은 치명, 신속, 특화 이 세가지 중 한가지입니다. 다른 경우는 고려하지 않습니다.")
        neck1 = input("목걸이의 첫번째 전투특성을 입력해주세요: ")
        neck2 = input("목걸이의 두번째 전투특성을 입력해주세요: ")
        ear1 = input("첫번째 귀걸이의 전투특성을 입력해주세요: ")
        ear2 = input("두번째 귀걸이의 전투특성을 입력해주세요: ")
        rin1 = input("첫번째 반지의 전투특성을 입력해주세요: ")
        rin2 = input("두번째 반지의 전투특성을 입력해주세요: ")
        if not {neck1, neck2, ear1, ear2, rin1, rin2} - {'치명', '신속', '특화'}:
            break
        else:
            print("잘못 입력하셨습니다. 다시 입력해주세요: ")

    target_dic = {}
    while True:
        try:
            target = input("\n목표 각인을 입력해주세요, 정확한 이름으로 입력하셔야 합니다, ex)예리한 둔기(O), 예둔(X), 예리한둔기(X), "
                           "그만 입력하시려면 그냥 엔터를, 처음부터 다시 입력하시려면 1을 입력해주세요: ")
            if target not in engrave_dict:
                if target == '':
                    print("목표 각인이", end=" ")
                    for i in target_dic:
                        print(f"[{i} {target_dic[i]}]", end=" ")
                    check = input("이 맞고 다음 단계로 넘어가고 싶다면 그냥 엔터를, 추가로 입력하고 싶다면 1을,"
                                  " 입력이 잘못되서 처음부터 입력하고싶다면 2를 입력해주세요: ")
                    if check == '':
                        for i in target_dic:
                            target_dic[i] *= 5
                        break
                elif target == '1':
                    target_dic = {}
                    continue
                else:
                    while target not in engrave_dict:
                        target = input("잘못 입력하셨습니다, 정확한 이름을 찾아서 다시 입력해주세요, 특수기호 또한 포함입니다: ")
            else:
                target_dic[target] = int(input(f"{target} 각인의 목표 수치를 1,2,3 중 정해주세요: "))
        except ValueError:
            pass

    while True:
        try:
            print("\n현재 보유중인 어빌리티 스톤의 스펙을 입력해주세요.")
            for i in target_dic:
                print(f"[{i}]", end=" ")
            temp1 = input("중 어빌리티 스톤의 맨 위에 존재하는 각인을 입력해주세요: ")
            while temp1 not in target_dic:
                temp1 = input("잘못 입력하셨거나 목표 각인에 해당하지 않는 각인입니다. 다시 입력해주세요: ")
            temp1_num = int(input(f"{temp1} 각인의 어빌리티 스톤 수치를 입력해주세요: "))

            for i in target_dic:
                if i == temp1:
                    continue
                print(f"[{i}]", end=" ")
            temp2 = input("중 어빌리티 스톤의 두번째에 존재하는 각인을 입력해주세요: ")
            while temp2 not in target_dic:
                temp2 = input("잘못 입력하셨거나 목표 각인에 해당하지 않는 각인입니다. 다시 입력해주세요: ")
            if temp1 == temp2:
                print("어빌리티 스톤의 두 각인은 같을 수 없습니다. 처음부터 다시 입력해주세요.")
                continue
            temp2_num = int(input(f"{temp2} 각인의 어빌리티 스톤 수치를 입력해주세요: "))

            for i in bad_engrave_dict:
                print(f"[{i}]", end=" ")
            temp3 = input("중 어빌리티 스톤의 세번째에 존재하는 디버프 각인을 입력해주세요: ")
            while temp3 not in bad_engrave_dict:
                temp3 = input("잘못 입력하셨거나 디버프 각인에 해당하지 않는 각인입니다. 다시 입력해주세요.")
            temp3_num = int(input(f"{temp3} 각인의 어빌리티 스톤 수치를 입력해주세요: "))
            ability_stone = {temp1: temp1_num, temp2: temp2_num, temp3: temp3_num}

            print(f"현재 어빌리티 스톤의 스펙은 {temp1} {temp1_num}, {temp2} {temp2_num}, {temp3} {temp3_num}입니다.")
            check = input("입력 내용이 정확하다면 그냥 엔터를, 잘못 입력해서 다시 입력하고 싶다면 1을 입력해주세요: ")
            if check == "":
                break
            elif check == "1":
                continue
            else:
                while check == "" or check == "1":
                    input("잘못 입력하셨습니다. 입력한 내용이 정확하다면 그냥 엔터를, 수정하고 싶으시다면 1을 입력해주세요: ")
        except ValueError:
            print("잘못 입력하셨습니다. 숫자로 입력해주세요.")
    already_read = []
    while True:
        for i in target_dic:
            if i in already_read:
                continue
            print(f"[{i}]", end=" ")
        temp = input("중 이미 읽은 전설 각인서를 입력해주세요. 입력하신 각인서는 20장 모두 읽은 것으로 간주합니다,"
                     " 다 입력했다면 그냥 엔터를 입력해주세요: ")
        if temp == "":
            break
        elif temp not in target_dic:
            print("잘못 입력하셨습니다, 목표 각인 중 이미 읽은 전설 각인서를 입력해주세요.")
            continue
        already_read.append(temp)

    print("시간이 좀 걸립니다, 잠시 기다려주세요...")

    return neck_qual, earring_qual, ring_qual, neck1, neck2, ear1, ear2, rin1, rin2, target_dic, ability_stone, already_read


def find_min_set(necklace, earring1, earring2, ring1, ring2, target, ab_stone, book_price):
    book_case = itertools.combinations(set(target.keys()) - set(ab_stone.keys()), 2)  # 어빌리티 스톤에 들어있지 않은 각인들
    read_book = [(9, 12), (12, 9), (12, 12)]
    default = {}
    for i in target:
        if i in ab_stone:
            default[i] = ab_stone[i]
        else:
            default[i] = 0
    necklace.sort(key=lambda x: x.price_low)
    earring1.sort(key=lambda x: x.price_low)
    earring2.sort(key=lambda x: x.price_low)
    ring1.sort(key=lambda x: x.price_low)
    ring2.sort(key=lambda x: x.price_low)
    total = []
    min_price = 1000000  # 나중에 최저가를 넘으면 바로 반복문을 멈추는 기능도 넣으면 더 빨라질듯
    for y in book_case:
        for u in read_book:
            price = 0
            test = copy.deepcopy(default)
            test[y[0]] += u[0]
            test[y[1]] += u[1]
            if u[0] == 12:
                price += book_price[y[0]] * 20
            if u[1] == 12:
                price += book_price[y[1]] * 20
            for q in necklace:
                temp1, price1 = stop_check(test, q, price)
                if type(temp1) == int or min_price < price1:
                    continue
                for w in earring1:
                    temp2, price2 = stop_check(temp1, w, price1)
                    if type(temp2) == int or min_price < price2:
                        continue
                    for e in earring2:
                        temp3, price3 = stop_check(temp2, e, price2)
                        if type(temp3) == int or min_price < price3:
                            continue
                        for r in ring1:
                            temp4, price4 = stop_check(temp3, r, price3)
                            if type(temp4) == int or min_price < price4:
                                continue
                            for t in ring2:
                                check = 0
                                temp5, price5 = stop_check(temp4, t, price4)
                                if type(temp5) != int or min_price < price5:
                                    for i in temp5:
                                        if temp5[i] != 15:
                                            check = 1
                                            break
                                    if not check:
                                        total.append((y, u, price, q, w, e, r, t, price5))
                                        min_price = min(min_price, price5)
                                        # min_price를 구하는 순간 디버프를 고려한 새로운 min_price를 구해내고 그걸로 min_price를 바꾸는 방법은?
                                        # 일단 지금은 단 하나의 경우의 수를 구하는 프로그램임
    total.sort(key=lambda x: x[-1])
    print(total)


def auction_set():
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')

    driver = webdriver.Chrome('chromedriver', options=options)
    driver.get(url='https://lostark.game.onstove.com/Auction')
    driver.implicitly_wait(1)

    driver.find_element_by_name('user_id').send_keys("oodeng98@gmail.com")
    driver.find_element_by_name('user_pwd').send_keys("lostarkengrave24\n")

    try:
        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#lostark-wrapper > div > main > div > div.deal > div.deal-contents > form > fieldset > div > div.bt > button.button.button--deal-detail')))
    finally:
        driver.find_element_by_css_selector('#selItemTier > div.lui-select__title').click()
        driver.find_element_by_css_selector('#selItemTier > div.lui-select__option > label:nth-child(4)').click()
        driver.find_element_by_css_selector('#selItemGrade > div.lui-select__title').click()
        driver.find_element_by_css_selector('#selItemGrade > div.lui-select__option > label:nth-child(7)').click()
        driver.find_element_by_css_selector(
            '#lostark-wrapper > div > main > div > div.deal > div.deal-contents > form > fieldset > div > div.bt > button.button.button--deal-detail').click()
    return driver


def common_set(driver, q):
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#selCategoryDetail > div.lui-select__title')))
    finally:
        driver.find_element_by_css_selector('#selCategoryDetail > div.lui-select__title').click()
        driver.find_element_by_css_selector(
            f'#selCategoryDetail > div.lui-select__option > label:nth-child({q[0]})').click()
        driver.find_element_by_css_selector('#selEtc_0 > div.lui-select__title').click()
        driver.find_element_by_css_selector('#selEtc_0 > div.lui-select__option > label:nth-child(2)').click()
        driver.find_element_by_css_selector('#selEtc_2 > div.lui-select__title').click()
        driver.find_element_by_css_selector('#selEtc_2 > div.lui-select__option > label:nth-child(3)').click()
        driver.find_element_by_css_selector('#selEtc_3 > div.lui-select__title').click()
        driver.find_element_by_css_selector('#selEtc_3 > div.lui-select__option > label:nth-child(3)').click()
        driver.find_element_by_css_selector(
            '#modal-deal-option > div > div > div.lui-modal__content > div:nth-child(2) > table > tbody > '
            'tr:nth-child(4) > td:nth-child(4) > div > div.lui-select__title').click()

def remove_comma(ret):
    return int(ret.replace(",", ""))


def auction_search(engrave_dict, neck_qual, earring_qual, ring_qual, neck1, neck2, ear1, ear2, rin1, rin2, target):
    # 카테고리 설정
    driver = auction_set()
    deal_option = {"치명": 2, "특화": 3, "신속": 5}
    data = []
    for q in [(11, 1), (12, 1), (12, 2), (13, 1), (13, 2)]:
        common_set(driver, q)
        temp_list = []
        if q[0] == 11:
            driver.find_element_by_css_selector(
                f'#modal-deal-option > div > div > div.lui-modal__content > div:nth-child(2) > table > tbody > '
                f'tr:nth-child(4) > td:nth-child(4) > div > div.lui-select__option > label:nth-child('
                f'{neck_qual})').click()
            driver.find_element_by_css_selector('#selEtcSub_0 > div.lui-select__title').click()
            driver.find_element_by_css_selector(
                f'#selEtcSub_0 > div.lui-select__option > label:nth-child({deal_option[neck1]})').click()
            driver.find_element_by_css_selector('#selEtc_1 > div.lui-select__title').click()
            driver.find_element_by_css_selector('#selEtc_1 > div.lui-select__option > label:nth-child(2)').click()
            driver.find_element_by_css_selector('#selEtcSub_1 > div.lui-select__title').click()
            driver.find_element_by_css_selector(
                f'#selEtcSub_1 > div.lui-select__option > label:nth-child({deal_option[neck2]})').click()
        elif q[0] == 12:
            option = ear1
            if q == (12, 2):
                option = ear2
                if ear1 == ear2:
                    data.append(data[-1])
                    continue
            driver.find_element_by_css_selector(
                f'#modal-deal-option > div > div > div.lui-modal__content > div:nth-child(2) > table > tbody > '
                f'tr:nth-child(4) > td:nth-child(4) > div > div.lui-select__option > label:nth-child('
                f'{earring_qual})').click()
            driver.find_element_by_css_selector('#selEtcSub_0 > div.lui-select__title').click()
            driver.find_element_by_css_selector(
                f'#selEtcSub_0 > div.lui-select__option > label:nth-child({deal_option[option]})').click()
        else:
            option = rin1
            if q == (13, 2):
                option = rin2
                if rin1 == rin2:
                    data.append(data[-1])
                    continue
            driver.find_element_by_css_selector(
                f'#modal-deal-option > div > div > div.lui-modal__content > div:nth-child(2) > table > tbody > '
                f'tr:nth-child(4) > td:nth-child(4) > div > div.lui-select__option > label:nth-child('
                f'{ring_qual})').click()
            driver.find_element_by_css_selector('#selEtcSub_0 > div.lui-select__title').click()
            driver.find_element_by_css_selector(
                f'#selEtcSub_0 > div.lui-select__option > label:nth-child({deal_option[option]})').click()
        for w in itertools.combinations(target.keys(), 2):
            engrave1 = w[0]
            engrave2 = w[1]
            # 최소 수치 설정
            for i in [(3, 5), (5, 3), (3, 4), (4, 3), (3, 3)]:
                driver.find_element_by_css_selector('#selEtcSub_2 > div.lui-select__title').click()
                driver.find_element_by_css_selector(
                    f'#selEtcSub_2 > div.lui-select__option > label:nth-child({engrave_dict[engrave1]})').click()
                driver.find_element_by_css_selector('#selEtcSub_3 > div.lui-select__title').click()
                driver.find_element_by_css_selector(
                    f'#selEtcSub_3 > div.lui-select__option > label:nth-child({engrave_dict[engrave2]})').click()
                if i[0] != 3:
                    driver.find_element_by_id('txtEtcMin_2').send_keys(i[0])
                if i[1] != 3:
                    driver.find_element_by_id('txtEtcMin_3').send_keys(i[1])
                driver.find_element_by_css_selector(
                    '#modal-deal-option > div > div > div.lui-modal__button > button.lui-modal__search').click()
                try:
                    element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '#auctionListTbody > tr:nth-child(1) > td:nth-child(5) > div > em')))
                    print(element.text)
                finally:
                    driver.find_element_by_css_selector('#lostark-wrapper > div > main > div > div.deal > div.deal-contents > form > fieldset > div > div.bt > button.button.button--deal-detail').click()
                try:
                    element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '#selCategoryDetail > div.lui-select__title')))
                finally:
                    pass
        data.append(temp_list)
    return *data, target
# 최저가를 찾는 부분까지 동일하게 만들고, 최저가를 찾으면 해당 페이지들에서 다시 디버프를 고려한 새로운 최저가를 찾은 후
# 새로운 최저가보다 낮은 기존 최저가를 가지고 있는 조합에서 또 그 과정을 반복해주면 찾을 수 있을 듯


def stop_check(engrave, new, previous_price):
    temp = copy.copy(engrave)
    index = list(new.effect.keys())
    temp[index[0]] += new.effect[index[0]]
    temp[index[1]] += new.effect[index[1]]
    new_price = previous_price + new.price_low
    for i in temp:
        if temp[i] >= 16:
            return 0
    return temp, new_price


def login():
    session = Session()
    request = Request(
        method='POST',
        url='https://member.onstove.com/auth/singin',
        headers={
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        },
        data={
            "user_id": "oodeng98@gmail.com",
            "user_pwd": "lostarkengrave24",
            "forever": "false",
            "redirect_url": "https://lostark.game.onstove.com/Auction",
            "inflow_path": "LOST_ARK",
            "game_no": "45"
        }
    )
    login_response = session.send(request.prepare())
    print(login_response.text)
    temp = QUERY
    response = search_key(temp)
    with open('test.html', 'w', encoding='utf-8') as f:
        f.write(response)
    return response.text


if __name__ == "__main__":
    engrave_dic = {"각성": 2, "갈증": 3, "강령술": 4, "강화 무기": 5, "강화 방패": 6, "결투의 대가": 7, "고독한 기사": 8, "광기": 9,
                   "광전사의 비기": 10, "구슬동자": 11, "굳은 의지": 12, "극의: 체술": 13, "급소 타격": 14, "기습의 대가": 15, "긴급구조": 16,
                   "넘치는 교감": 17, "달의 소리": 18, "달인의 저력": 19, "돌격대장": 20, "두 번째 동료": 21, "마나 효율 증가": 22,
                   "마나의 흐름": 23, "멈출 수 없는 충동": 24, "바리케이드": 25, "버스트": 26, "번개의 분노": 27, "부러진 뼈": 28,
                   "분노의 망치": 29, "분쇄의 주먹": 30, "불굴": 31, "사냥의 시간": 32, "상급 소환사": 33, "선수필승": 34, "세맥타통": 35,
                   "속전속결": 36, "슈퍼 차지": 37, "승부사": 38, "시선 집중": 39, "실드 관통": 40, "심판자": 41, "아드레날린": 42,
                   "아르데타인의 기술": 43, "안정된 상태": 44, "약자 무시": 45, "에테르 포식자": 46, "여신의 가호": 47, "역천지체": 48,
                   "연속 포격": 49, "예리한 둔기": 50, "오의 강화": 51, "오의난무": 52, "완벽한 억제": 53, "원한": 54, "위기 모면": 55,
                   "일격필살": 56, "잔재된 기운": 57, "저주받은 인형": 58, "전문의": 59, "전투 태세": 60, "절실한 구원": 61, "절정": 62,
                   "절제": 63, "점화": 64, "정기 흡수": 65, "정밀 단도": 66, "죽음의 습격": 67, "중갑 착용": 68, "중력 수련": 69, "진실된 용맹": 70,
                   "진화의 유산": 71, "질량 증가": 72, "초심": 73, "최대 마나 증가": 74, "추진력": 75, "축복의 오라": 76, "충격 단련": 77,
                   "타격의 대가": 78, "탈출의 명수": 79, "폭발물 전문가": 80, "피스메이커": 81, "핸드거너": 82, "화력 강화": 83,
                   "황제의 칙령": 84, "황후의 은총": 85}
    # qual1, qual2, qual3, a2, a3, a4, a5, a6, a7, a8, a9, a10 = receive_input_data(engrave_dic)
    # find_min_set(*auction_search(engrave_dic, qual1, qual2, qual3, a2, a3, a4, a5, a6, a7, a8), a9, find_price(a8, a10))
    auction_search(engrave_dic, 2, 2, 2, "치명", "신속", "치명", "치명", "치명", "치명", {"원한": 15, "슈퍼 차지": 15, "바리케이드": 15, "결투의 대가": 15, "고독한 기사": 15})


# 33각인을 먼저 검색한 다음 없으면 그 다음 검색들도 안해줘도 되는데?
# 로스트아크 전투정보실에서 가져와야되나?
# 이제 디버프 각인도 고려해봐야함
