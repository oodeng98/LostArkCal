import selenium
import itertools
import time
import copy
from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from multiprocessing import Pool
#test massage

def receive_input_data(engrave_dict):
    bad_engrave_dict = {"공격력 감소": 0, "공격속도 감소": 0, "방어력 감소": 0, "이동속도 감소": 0}

    print("이 프로그램은 각인 맞추기에 대한 기본적 지식이 있는 사람이 쓰는 것을 가정하고 만든 프로그램입니다.")
    print("터무니없는 어빌리티 스톤으로 33333각인을 맞춘다는 말도 안되는 경우는 체크해주지 않습니다.")
    print("현재 베타테스트 상태로 33333각인만 지원합니다.")
    print("선택과 투자, 그리고 과금은 모두 사용자의 책임입니다. 서비스 지원 업체는 해당 부분은 보상하지 않습니다.")
    while True:
        try:
            qual = int(input("원하는 품질 하한선을 0, 10...80, 90 중 선택하여 입력해주세요: "))
            if qual % 10:
                raise ValueError
            break
        except ValueError:
            print("잘못 입력하셨습니다. 다시 입력해주세요.")

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
            print("잘못 입력하셨습니다. 다시 입력해주세요.")

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
                temp1 = input("잘못 입력하셨거나 목표 각인에 해당하지 않는 각인입니다. 다시 입력해주세요.")
            temp1_num = int(input(f"{temp1} 각인의 어빌리티 스톤 수치를 입력해주세요: "))

            for i in target_dic:
                if i == temp1:
                    continue
                print(f"[{i}]", end=" ")
            temp2 = input("중 어빌리티 스톤의 두번째에 존재하는 각인을 입력해주세요: ")
            while temp2 not in target_dic:
                temp2 = input("잘못 입력하셨거나 목표 각인에 해당하지 않는 각인입니다. 다시 입력해주세요.")
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
                    input("잘못 입력하셨습니다. 입력한 내용이 정확하다면 그냥 스페이스를, 수정하고 싶으시다면 1을 입력해주세요: ")
        except ValueError:
            print("잘못 입력하셨습니다. 숫자로 입력해주세요.")
    print("시간이 좀 걸립니다, 잠시 기다려주세요...")

    return qual + 1, neck1, neck2, ear1, ear2, rin1, rin2, target_dic, ability_stone


def find_accessory_cases():
    all_cases = []
    comb = list(itertools.combinations([0, 1, 2, 3, 4], 2))
    engrave_case = [(3, 3), (3, 4), (4, 3), (3, 5), (5, 3)]
    for i in comb:
        for j in engrave_case:
            temp = [0, 0, 0, 0, 0]
            temp[i[0]], temp[i[1]] = j
            all_cases.append(temp)
    return all_cases


def find_book_cases():
    all_cases = []
    comb = list(itertools.combinations([0, 1, 2, 3, 4], 2))
    # engrave_case = [(9, 9), (9, 12), (12, 9), (12, 12)]
    engrave_case = [(12, 9), (9, 12)]  # 12, 9의 케이스를 찾기 위한 줄, 나중에는 없애야함
    for i in comb:
        for j in engrave_case:
            temp = [0, 0, 0, 0, 0]
            temp[i[0]], temp[i[1]] = j
            all_cases.append(temp)
    return all_cases


def find_min_set(necklace, earring1, earring2, ring1, ring2):
    # 각인 효과1, 각인 수치1, 각인 효과2, 각인 수치2, 가격
    # 치명 신속 목걸이
    """necklace = [(('원한', 3), ('예리한 둔기', 5), 15000),
                (('원한', 5), ('예리한 둔기', 3), 1000),
                (('원한', 3), ('돌격대장', 5), 7000),
                (('원한', 5), ('돌격대장', 3), 5000),
                (('원한', 3), ('상급 소환사', 5), 55000),
                (('원한', 5), ('상급 소환사', 3), 1000000),
                (('원한', 3), ('넘치는 교감', 5), 50000),
                (('원한', 5), ('넘치는 교감', 3), 50000),
                (('예리한 둔기', 3), ('돌격대장', 5), 20000),
                (('예리한 둔기', 5), ('돌격대장', 3), 23000),
                (('예리한 둔기', 3), ('상급 소환사', 5), 1000000),
                (('예리한 둔기', 5), ('상급 소환사', 3), 50000),
                (('예리한 둔기', 3), ('넘치는 교감', 5), 130000),
                (('예리한 둔기', 5), ('넘치는 교감', 3), 30000),
                (('돌격대장', 3), ('상급 소환사', 5), 90000),
                (('돌격대장', 5), ('상급 소환사', 3), 40000),
                (('돌격대장', 3), ('넘치는 교감', 5), 1000000),
                (('돌격대장', 5), ('넘치는 교감', 3), 1000000)]
    # 치명 귀걸이
    earring1 = [(('원한', 3), ('예리한 둔기', 5), 10000),
                (('원한', 5), ('예리한 둔기', 3), 1000),
                (('원한', 3), ('돌격대장', 5), 800),
                (('원한', 5), ('돌격대장', 3), 50),
                (('원한', 3), ('상급 소환사', 5), 7500),
                (('원한', 5), ('상급 소환사', 3), 90000),
                (('원한', 3), ('넘치는 교감', 5), 35000),
                (('원한', 5), ('넘치는 교감', 3), 24000),
                (('예리한 둔기', 3), ('돌격대장', 5), 1),
                (('예리한 둔기', 5), ('돌격대장', 3), 100),
                (('예리한 둔기', 3), ('상급 소환사', 5), 6500),
                (('예리한 둔기', 5), ('상급 소환사', 3), 35000),
                (('예리한 둔기', 3), ('넘치는 교감', 5), 56000),
                (('예리한 둔기', 5), ('넘치는 교감', 3), 15000),
                (('돌격대장', 3), ('상급 소환사', 5), 10000),
                (('돌격대장', 5), ('상급 소환사', 3), 50000),
                (('돌격대장', 3), ('넘치는 교감', 5), 25000),
                (('돌격대장', 5), ('넘치는 교감', 3), 13000)]
    # 신속 귀걸이
    earring2 = [(('원한', 3), ('예리한 둔기', 5), 5000),
                (('원한', 5), ('예리한 둔기', 3), 4000),
                (('원한', 3), ('돌격대장', 5), 3499),
                (('원한', 5), ('돌격대장', 3), 1),
                (('원한', 3), ('상급 소환사', 5), 15000),
                (('원한', 5), ('상급 소환사', 3), 20000),
                (('원한', 3), ('넘치는 교감', 5), 65000),
                (('원한', 5), ('넘치는 교감', 3), 6500),
                (('예리한 둔기', 3), ('돌격대장', 5), 100),
                (('예리한 둔기', 5), ('돌격대장', 3), 2),
                (('예리한 둔기', 3), ('상급 소환사', 5), 10000),
                (('예리한 둔기', 5), ('상급 소환사', 3), 25000),
                (('예리한 둔기', 3), ('넘치는 교감', 5), 50000),
                (('예리한 둔기', 5), ('넘치는 교감', 3), 6000),
                (('돌격대장', 3), ('상급 소환사', 5), 100),
                (('돌격대장', 5), ('상급 소환사', 3), 30000),
                (('돌격대장', 3), ('넘치는 교감', 5), 30000),
                (('돌격대장', 5), ('넘치는 교감', 3), 35555)]
    # 치명 반지
    ring1 = [(('원한', 3), ('예리한 둔기', 5), 1000),
             (('원한', 5), ('예리한 둔기', 3), 1050),
             (('원한', 3), ('돌격대장', 5), 50),
             (('원한', 5), ('돌격대장', 3), 500),
             (('원한', 3), ('상급 소환사', 5), 15000),
             (('원한', 5), ('상급 소환사', 3), 60000),
             (('원한', 3), ('넘치는 교감', 5), 45000),
             (('원한', 5), ('넘치는 교감', 3), 10),
             (('예리한 둔기', 3), ('돌격대장', 5), 1),
             (('예리한 둔기', 5), ('돌격대장', 3), 500),
             (('예리한 둔기', 3), ('상급 소환사', 5), 20000),
             (('예리한 둔기', 5), ('상급 소환사', 3), 30000),
             (('예리한 둔기', 3), ('넘치는 교감', 5), 20000),
             (('예리한 둔기', 5), ('넘치는 교감', 3), 15000),
             (('돌격대장', 3), ('상급 소환사', 5), 10000),
             (('돌격대장', 5), ('상급 소환사', 3), 54000),
             (('돌격대장', 3), ('넘치는 교감', 5), 35000),
             (('돌격대장', 5), ('넘치는 교감', 3), 15000)]
    # 신속 반지
    ring2 = [(('원한', 3), ('예리한 둔기', 5), 8000),
             (('원한', 5), ('예리한 둔기', 3), 2205),
             (('원한', 3), ('돌격대장', 5), 105),
             (('원한', 5), ('돌격대장', 3), 1000),
             (('원한', 3), ('상급 소환사', 5), 10000),
             (('원한', 5), ('상급 소환사', 3), 50000),
             (('원한', 3), ('넘치는 교감', 5), 50000),
             (('원한', 5), ('넘치는 교감', 3), 30000),
             (('예리한 둔기', 3), ('돌격대장', 5), 4500),
             (('예리한 둔기', 5), ('돌격대장', 3), 1),
             (('예리한 둔기', 3), ('상급 소환사', 5), 10000),
             (('예리한 둔기', 5), ('상급 소환사', 3), 60000),
             (('예리한 둔기', 3), ('넘치는 교감', 5), 30000),
             (('예리한 둔기', 5), ('넘치는 교감', 3), 7000),
             (('돌격대장', 3), ('상급 소환사', 5), 45000),
             (('돌격대장', 5), ('상급 소환사', 3), 45000),
             (('돌격대장', 3), ('넘치는 교감', 5), 20000),
             (('돌격대장', 5), ('넘치는 교감', 3), 29999)]"""
    book_case = itertools.combinations(["돌격대장", '상급 소환사', '넘치는 교감'], 2)  # 어빌리티 스톤에 들어있지 않은 각인들

    necklace.sort(key=lambda x: x[2])
    earring1.sort(key=lambda x: x[2])
    earring2.sort(key=lambda x: x[2])
    ring1.sort(key=lambda x: x[2])
    ring2.sort(key=lambda x: x[2])
    total = []
    for y in tqdm(book_case):
        for u in [(9, 12), (12, 9)]:
            test = {"원한": 7, "예리한 둔기": 0, "돌격대장": 7, "상급 소환사": 0, "넘치는 교감": 0}
            test[y[0]] += u[0]
            test[y[1]] += u[1]
            for q in necklace:
                temp1 = over_15_check(test, q)
                if type(temp1) == int:
                    continue
                for w in earring1:
                    temp2 = over_15_check(temp1, w)
                    if type(temp2) == int:
                        continue
                    for e in earring2:
                        temp3 = over_15_check(temp2, e)
                        if type(temp3) == int:
                            continue
                        for r in ring1:
                            temp4 = over_15_check(temp3, r)
                            if type(temp4) == int:
                                continue
                            for t in ring2:
                                temp5 = over_15_check(temp4, t)
                                if type(temp5) != int:
                                    total.append((y, u, q, w, e, r, t, q[-1] + w[-1] + e[-1] + r[-1] + t[-1]))

    total.sort(key=lambda x: x[-1])
    for i in range(10):
        print(total[i])


def auction_set(engrave_dict):
    # 창이 열리지 않고 수행하게 하는 코드. 단, 이 코드를 사용하면 프로그램을 종료할 때 driver.quit()를 꼭 사용해줘야 한다
    options = webdriver.ChromeOptions()  # 크롬 옵션 객체 생성
    # options.add_argument('headless')  # headless 모드 설정

    driver = webdriver.Chrome('chromedriver', options=options)
    driver.get(url='https://lostark.game.onstove.com/Auction')

    driver.implicitly_wait(2.5)

    # 아이템 등급과 티어 설정
    driver.find_element_by_xpath('//*[@id="selItemGrade"]/div[1]').click()
    driver.find_element_by_xpath('//*[@id="selItemGrade"]/div[2]/label[7]').click()
    driver.find_element_by_xpath('//*[@id="selItemTier"]/div[1]').click()
    driver.find_element_by_xpath('//*[@id="selItemTier"]/div[2]/label[4]').click()

    return driver


def remove_comma(ret):
    return int(ret.replace(",", ""))


def auction_search(engrave_dict, qual, neck1, neck2, ear1, ear2, rin1, rin2, target, ability_stone):
    # 카테고리 설정
    _neck = []
    _ear1 = []
    _ear2 = []
    _rin1 = []
    _rin2 = []
    battle_dict = {"치명": 2, "특화": 3, "신속": 5}
    for q in [(11, 1), (12, 1), (12, 2), (13, 1), (13, 2)]:
        driver = auction_set(engrave_dict)
        # 품질 설정
        driver.find_element_by_xpath('//*[@id="lostark-wrapper"]/div/main/div/div[3]/div[2]/form/fieldset/div/div[5]'
                                     '/button[2]').click()
        driver.find_element_by_xpath('//*[@id="modal-deal-option"]/div/div/div[1]/div[1]/table/tbody/tr[4]/td[2]/div/'
                                     'div[1]').click()
        driver.find_element_by_xpath(f'//*[@id="modal-deal-option"]/div/div/div[1]/div[1]/table/tbody/tr[4]/td[2]/div/'
                                     f'div[2]/label[{qual}]').click()
        driver.find_element_by_xpath('//*[@id="selCategoryDetail"]/div[1]').click()
        driver.find_element_by_xpath(f'//*[@id="selCategoryDetail"]/div[2]/label[{q[0]}]').click()

        # 전투 특성 설정
        # 목걸이용 전투 특성 설정
        if q[0] == 11:
            # 특성 1 설정
            driver.find_element_by_xpath('//*[@id="selEtc_0"]/div[1]').click()
            driver.find_element_by_xpath('//*[@id="selEtc_0"]/div[2]/label[2]').click()
            driver.find_element_by_xpath('//*[@id="selEtcSub_0"]/div[1]').click()
            driver.find_element_by_xpath(f'//*[@id="selEtcSub_0"]/div[2]/label[{battle_dict[neck1]}]').click()
            # 특성 2 설정
            driver.find_element_by_xpath('//*[@id="selEtc_1"]/div[1]').click()
            driver.find_element_by_xpath('//*[@id="selEtc_1"]/div[2]/label[2]').click()
            driver.find_element_by_xpath('//*[@id="selEtcSub_1"]/div[1]').click()
            driver.find_element_by_xpath(f'//*[@id="selEtcSub_1"]/div[2]/label[{battle_dict[neck2]}]').click()
            print(f'{neck1} {neck2} 목걸이')
        elif q[0] == 12:
            # 특성 1 설정
            driver.find_element_by_xpath('//*[@id="selEtc_0"]/div[1]').click()
            driver.find_element_by_xpath('//*[@id="selEtc_0"]/div[2]/label[2]').click()
            driver.find_element_by_xpath('//*[@id="selEtcSub_0"]/div[1]').click()
            if q[1] == 1:
                driver.find_element_by_xpath(f'//*[@id="selEtcSub_0"]/div[2]/label[{battle_dict[ear1]}]').click()
                print(f'{ear1} 귀걸이')
            else:
                if ear1 == ear2:
                    continue
                driver.find_element_by_xpath(f'//*[@id="selEtcSub_0"]/div[2]/label[{battle_dict[ear2]}]').click()
                print(f'{ear2} 귀걸이')
        else:
            driver.find_element_by_xpath('//*[@id="selEtc_0"]/div[1]').click()
            driver.find_element_by_xpath('//*[@id="selEtc_0"]/div[2]/label[2]').click()
            driver.find_element_by_xpath('//*[@id="selEtcSub_0"]/div[1]').click()
            if q[1] == 1:
                driver.find_element_by_xpath(f'//*[@id="selEtcSub_0"]/div[2]/label[{battle_dict[rin1]}]').click()
                print(f'{rin1} 반지')
            else:
                if rin1 == rin2:
                    continue
                driver.find_element_by_xpath(f'//*[@id="selEtcSub_0"]/div[2]/label[{battle_dict[rin2]}]').click()
                print(f'{rin2} 반지')
        # 각인1 설정
        driver.find_element_by_xpath('//*[@id="selEtc_2"]/div[1]').click()
        driver.find_element_by_xpath('//*[@id="selEtc_2"]/div[2]/label[3]').click()

        # 각인2 설정
        driver.find_element_by_xpath('//*[@id="selEtc_3"]/div[1]').click()
        driver.find_element_by_xpath('//*[@id="selEtc_3"]/div[2]/label[3]').click()

        for w in itertools.combinations(target.keys(), 2):
            engrave1 = w[0]
            engrave2 = w[1]
            # 최소 수치 설정
            for i in [(3, 5), (5, 3)]:
                driver.find_element_by_xpath('//*[@id="selEtcSub_2"]/div[1]').click()
                driver.find_element_by_xpath(f'//*[@id="selEtcSub_2"]/div[2]/label[{engrave_dict[engrave1]}]').click()
                input_box = driver.find_element_by_id("txtEtcMin_2")
                input_box.send_keys(i[0])

                driver.find_element_by_xpath('//*[@id="selEtcSub_3"]/div[1]').click()
                driver.find_element_by_xpath(f'//*[@id="selEtcSub_3"]/div[2]/label[{engrave_dict[engrave2]}]').click()
                input_box = driver.find_element_by_id("txtEtcMin_3")
                input_box.send_keys(i[1])

                # 검색 버튼 클릭
                driver.find_element_by_xpath('//*[@id="modal-deal-option"]/div/div/div[2]/button[1]').click()
                # driver.find_element_by_xpath('//*[@id="BUY_PRICE"]').click(), 즉시 구매가 기준으로 정렬해주는 건데 안먹힌다
                try:
                    time.sleep(1)
                    ret = driver.find_element_by_xpath('//*[@id="auctionListTbody"]/tr[1]/td[5]/div/em')
                    ret = remove_comma(ret.text)
                    if ret == 0:
                        raise AttributeError
                except (selenium.common.exceptions.NoSuchElementException, AttributeError):
                    try:
                        print("아무것도 없음, 재검색")
                        ret = 1000000
                        driver.find_element_by_xpath('//*[@id="btnSearch"]').click()
                        ret = driver.find_element_by_xpath('//*[@id="auctionListTbody"]/tr[1]/td[5]/div/em')
                        ret = remove_comma(ret.text)
                    except (selenium.common.exceptions.NoSuchElementException, AttributeError):
                        ret = 1000000
                    # print(remove_comma(ret.text))
                print(f"(('{engrave1}', {i[0]}), ('{engrave2}', {i[1]}), {ret}), ")
                if q[0] == 11:
                    _neck.append(((engrave1, i[0]), (engrave2, i[1]), ret))
                elif q[0] == 12:
                    if q[1] == 1:
                        _ear1.append(((engrave1, i[0]), (engrave2, i[1]), ret))
                    else:
                        _ear2.append(((engrave1, i[0]), (engrave2, i[1]), ret))
                else:
                    if q[1] == 1:
                        _rin1.append(((engrave1, i[0]), (engrave2, i[1]), ret))
                    else:
                        _rin2.append(((engrave1, i[0]), (engrave2, i[1]), ret))
                    driver.find_element_by_xpath('//*[@id="btnSearch"]').click()
                try:
                    driver.find_element_by_xpath(
                        '//*[@id="lostark-wrapper"]/div/main/div/div[3]/div[2]/form/fieldset/div/div[5]/button[2]').click()
                except selenium.common.exceptions.ElementClickInterceptedException:
                    time.sleep(2)
                    driver.find_element_by_xpath(
                        '//*[@id="lostark-wrapper"]/div/main/div/div[3]/div[2]/form/fieldset/div/div[5]/button[2]').click()
        driver.quit()
    return _neck, _ear1, _ear2, _rin1, _rin2


def over_15_check(engrave, new):
    temp = copy.copy(engrave)
    temp[new[0][0]] += new[0][1]
    temp[new[1][0]] += new[1][1]
    for i in temp:
        if temp[i] >= 16:
            return 0
    return temp


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
                   "절제": 63, "정기 흡수": 64, "정밀 단도": 65, "죽음의 습격": 66, "중갑 착용": 67, "중력 수련": 68, "진실된 용맹": 69,
                   "진화의 유산": 70, "질량 증가": 71, "초심": 72, "최대 마나 증가": 73, "추진력": 74, "축복의 오라": 75, "충격 단련": 76,
                   "타격의 대가": 77, "탈출의 명수": 78, "폭발물 전문가": 79, "피스메이커": 80, "핸드거너": 81, "화력 강화": 82,
                   "황제의 칙령": 83, "황후의 은총": 84}
    # auction_search(engrave_dic, *receive_input_data(engrave_dic))
    print(auction_search(engrave_dic, 1, '치명', '신속', '치명', '신속', '치명', '신속', {'원한': 15, '예리한 둔기': 15, '돌격대장': 15, '상급 소환사': 15, '넘치는 교감': 15}, {'원한': 7, '돌격대장': 6, '공격력 감소': 4}))


"""
입력 예시
0
치명
신속
치명
신속
치명
신속
원한
3
예리한 둔기
3
돌격대장
3
상급 소환사
3
넘치는 교감
3


원한
7
돌격대장
6
공격력 감소
4

"""
