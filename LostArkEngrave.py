import selenium
import itertools
import time
from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


def receive_input_data(engrave_dict):
    bad_engrave_dict = {"공격력 감소": 0, "공격속도 감소": 0, "방어력 감소": 0, "이동속도 감소": 0}

    print("이 프로그램은 각인 맞추기에 대한 기본적 지식이 있는 사람이 쓰는 것을 가정하고 만든 프로그램입니다.")
    print("터무니없는 어빌리티 스톤으로 33333각인을 맞춘다는 말도 안되는 경우는 체크해주지 않습니다.")
    print("현재 베타테스트 상태로 33333각인만 지원합니다.")
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
                            target_dic[i] *= 3
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
    engrave_case = [(9, 9)]  # 9, 9의 케이스를 찾기 위한 줄, 나중에는 없애야함
    for i in comb:
        for j in engrave_case:
            temp = [0, 0, 0, 0, 0]
            temp[i[0]], temp[i[1]] = j
            all_cases.append(temp)
    return all_cases


def find_all_sets():
    stone = [7, 0, 6, 0, 0]

    # 최소값을 계속 비교해주면서 처음에 잘라버릴 수 있을 것 같은데
    count = 0
    for q in tqdm(find_accessory_cases()):
        neck = q
        for w in itertools.combinations(find_accessory_cases(), 2):
            earring1, earring2 = w
            for e in itertools.combinations(find_accessory_cases(), 2):
                ring1, ring2 = e
                for r in find_book_cases():
                    check = 0
                    book = r
                    accessories = [neck, earring1, earring2, ring1, ring2]
                    total = [0, 0, 0, 0, 0]
                    for i in accessories:
                        for j in range(5):
                            total[j] += i[j]
                    for i in range(5):
                        total[i] += stone[i]
                        total[i] += book[i]
                    for i in range(4):
                        if total[i] < 15:
                            check = 1
                            break
                    # if check or total[4] < 5 or total[4] >= 10:
                    temp = [5, 6]
                    if check or total[4] not in temp:
                        continue
                    count += 1
                    print(accessories, book, total)
    print(count)


def auction_set(engrave_dict):
    driver = webdriver.Chrome('chromedriver')
    driver.implicitly_wait(5)

    driver.get(url='https://lostark.game.onstove.com/Auction')

    # 아이템 등급과 티어 설정
    driver.find_element_by_xpath('//*[@id="selItemGrade"]/div[1]').click()
    driver.find_element_by_xpath('//*[@id="selItemGrade"]/div[2]/label[7]').click()
    driver.find_element_by_xpath('//*[@id="selItemTier"]/div[1]').click()
    driver.find_element_by_xpath('//*[@id="selItemTier"]/div[2]/label[4]').click()
    driver.find_element_by_xpath('//*[@id="lostark-wrapper"]/div/main/div/div[3]/div[2]/form/fieldset/div/div[5]'
                                 '/button[2]').click()
    driver.implicitly_wait(5)

    return driver


def remove_comma(ret):
    return int(ret.replace(",", ""))


def auction_search(engrave_dict, driver, qual, neck1, neck2, ear1, ear2, rin1, rin2, target, ability_stone):
    def find_accessory_price():
        case = find_accessory_cases()
        comb = list(itertools.combinations([0, 1, 2, 3, 4], 2))
        print(comb)
        print(case)
        # comb는 10개, 5개씩 case에 속해있어서 50개, 각인을 고정해주고 engrave_case를 돌려주면 될 듯 싶은데?
        # 각인의 최소 수치로 검색하므로 경우의 수를 찾을 때 15를 넘는 경우를 스킵해줘도 될 듯 싶다, 어차피 각인 수치를 넘는 경우도
        # 최솟값으로 검색한다면 그 검색 결과에 포함되어 있으므로

    # 품질 설정
    driver.find_element_by_xpath('//*[@id="modal-deal-option"]/div/div/div[1]/div[1]/table/tbody/tr[4]/td[2]/div/'
                                 'div[1]').click()
    driver.find_element_by_xpath(f'//*[@id="modal-deal-option"]/div/div/div[1]/div[1]/table/tbody/tr[4]/td[2]/div/'
                                 f'div[2]/label[{qual}]').click()
    # 카테고리 설정
    battle_dict = {"치명": 2, "특화": 3, "신속": 5}
    for q in [(11, 1), (12, 1), (12, 2), (13, 1), (13, 2)]:
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
            print(neck1, neck2, end=" ")
        elif q[0] == 12:
            # 특성 1 설정
            driver.find_element_by_xpath('//*[@id="selEtc_0"]/div[1]').click()
            driver.find_element_by_xpath('//*[@id="selEtc_0"]/div[2]/label[2]').click()
            driver.find_element_by_xpath('//*[@id="selEtcSub_0"]/div[1]').click()
            if q[1] == 1:
                driver.find_element_by_xpath(f'//*[@id="selEtcSub_0"]/div[2]/label[{battle_dict[ear1]}]').click()
                print(ear1, end=" ")
            else:
                driver.find_element_by_xpath(f'//*[@id="selEtcSub_0"]/div[2]/label[{battle_dict[ear2]}]').click()
                print(ear2, end=" ")

        else:
            driver.find_element_by_xpath('//*[@id="selEtc_0"]/div[1]').click()
            driver.find_element_by_xpath('//*[@id="selEtc_0"]/div[2]/label[2]').click()
            driver.find_element_by_xpath('//*[@id="selEtcSub_0"]/div[1]').click()
            if q[1] == 1:
                driver.find_element_by_xpath(f'//*[@id="selEtcSub_0"]/div[2]/label[{battle_dict[rin1]}]').click()
                print(rin1, end=" ")
            else:
                driver.find_element_by_xpath(f'//*[@id="selEtcSub_0"]/div[2]/label[{battle_dict[rin2]}]').click()
                print(rin2, end=" ")
        # 각인1 설정
        for w in itertools.combinations(target.keys(), 2):
            driver.find_element_by_xpath('//*[@id="selEtc_2"]/div[1]').click()
            driver.find_element_by_xpath('//*[@id="selEtc_2"]/div[2]/label[3]').click()
            engrave1 = w[0]

            # 각인2 설정
            driver.find_element_by_xpath('//*[@id="selEtc_3"]/div[1]').click()
            driver.find_element_by_xpath('//*[@id="selEtc_3"]/div[2]/label[3]').click()
            engrave2 = w[1]

            # 최소 수치 설정
            price_list = []
            for i in [(3, 5), (5, 3)]:
                driver.find_element_by_xpath('//*[@id="selEtcSub_2"]/div[1]').click()
                driver.find_element_by_xpath(f'//*[@id="selEtcSub_2"]/div[2]/label[{engrave_dict[engrave1]}]').click()
                input_box = driver.find_element_by_id("txtEtcMin_2")
                input_box.send_keys(i[0])
                print(engrave1, i[0], end=" ")

                driver.find_element_by_xpath('//*[@id="selEtcSub_3"]/div[1]').click()
                driver.find_element_by_xpath(f'//*[@id="selEtcSub_3"]/div[2]/label[{engrave_dict[engrave2]}]').click()
                input_box = driver.find_element_by_id("txtEtcMin_3")
                input_box.send_keys(i[1])
                print(engrave2, i[1], end=" ")

                # 검색 버튼 클릭
                driver.find_element_by_xpath('//*[@id="modal-deal-option"]/div/div/div[2]/button[1]').click()
                # driver.find_element_by_xpath('//*[@id="BUY_PRICE"]').click(), 즉시 구매가 기준으로 정렬해주는 건데 안먹힌다
                # driver.implicitly_wait(5)
                time.sleep(1)  # 3000, 10000, 7000, 13000, 9000이어야 하는데 3000이 두번 들어오는 오류가 발생해서 넣어줌
                try:
                    ret = driver.find_element_by_xpath('//*[@id="auctionListTbody"]/tr[1]/td[5]/div/em')
                    # price_list.append(remove_comma(ret.text))
                    print(remove_comma(ret.text))
                except selenium.common.exceptions.NoSuchElementException:
                    print("매물 없음")
                driver.find_element_by_xpath(
                    '//*[@id="lostark-wrapper"]/div/main/div/div[3]/div[2]/form/fieldset/div/div[5]/button[2]').click()

        # driver.find_element_by_xpath('//*[@id="modal-deal-option"]/div/div/div[2]/button[1]').click()
        # driver.find_element_by_xpath('').click()

        # cases = find_accessory_cases()

        # if battle == "치명"
        cases = [3, 0, 5, 0, 0]

        # driver.close()


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
    # 1, '치명', '신속', '치명', '치명', '치명', '치명', {'원한': 9, '예리한 둔기': 9, '돌격대장': 9, '상급 소환사': 9, '넘치는 교감': 9}, {'원한': 7, '돌격대장': 6, '방어력 감소': 4}
    # auction_search(engrave_dic, auction_set(engrave_dic), *receive_input_data(engrave_dic))
    auction_search(engrave_dic, auction_set(engrave_dic), 1, '치명', '신속', '치명', '치명', '치명', '치명', {'원한': 9, '예리한 둔기': 9, '돌격대장': 9, '상급 소환사': 9, '넘치는 교감': 9}, {'원한': 7, '돌격대장': 6, '방어력 감소': 4})
    # find_min_set(engrave_dic)

"""
입력 예시
0
치명
신속
치명
치명
치명
치명
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
방어력 감소
4

"""
