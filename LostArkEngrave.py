import selenium
import itertools
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
    print("터무니없는 어빌리티 스톤으로 33333각인을 맞춘다는 말도 안되는 경우는 체크해주지 않습니다.\n")
    while True:
        try:
            qual = int(input("원하는 품질 하한선을 0, 10...80, 90 중 선택하여 입력해주세요: "))
            if qual % 10:
                raise ValueError
            break
        except ValueError:
            print("잘못 입력하셨습니다. 다시 입력해주세요.")

    while True:
        try:
            print("\n개수의 총 합은 목걸이를 2로 쳐서 6이어야 합니다.")
            feature_1 = int(input("치명 악세서리의 개수를 입력해주세요, ex)목걸이, 반지 2개, 귀걸이 2개가 치명에 해당된다면 5, 해당사항이 없으면 0입니다: "))
            feature_2 = int(input("신속 악세서리의 개수를 입력해주세요, ex)목걸이에만 신속이 포함된다면 1, 해당사항이 없으면 0입니다: "))
            feature_3 = int(input("특화 악세서리의 개수를 입력해주세요, ex)목걸이, 반지 1개, 귀걸이 1개가 특화에 해당된다면 3, 해당사항이 없으면 0입니다: "))
            if feature_1 + feature_2 + feature_3 != 6:
                print("악세서리의 총 개수가 6이 아닙니다. 다시 입력해주세요.")
                continue
            check = input(f"치명 악세서리의 개수가 {feature_1}개, 신속 악세서리의 개수가 {feature_2}개, 특화 악세서리의 개수가"
                          f" {feature_3}개가 맞다면 그냥 스페이스를, 다시 입력하고 싶으시다면 0을 입력해주세요: ")
            if check == "":
                break
            elif check == "0":
                pass
            else:
                while check != "":
                    print("잘못 입력하셨습니다.")
                    check = input(f"치명 악세서리의 개수가 {feature_1}개, 신속 악세서리의 개수가 {feature_2}개, 특화 악세서리의 개수가"
                                  f" {feature_3}개가 맞다면 그냥 스페이스를, 다시 입력하고 싶으시다면 0을 입력해주세요: ")
        except ValueError:
            print("잘못 입력하셨습니다. 다시 입력해주세요.")

    target_dic = {}
    while True:
        try:
            target = input("\n목표 각인을 입력해주세요, 정확한 이름으로 입력하셔야 합니다, ex)예리한 둔기(O), 예둔(X), 예리한둔기(X), "
                           "그만 입력하시려면 그냥 스페이스를, 처음부터 다시 입력하시려면 1을 입력해주세요: ")
            if target not in engrave_dict:
                if target == '':
                    print("목표 각인이", end=" ")
                    for i in target_dic:
                        print(f"[{i} {target_dic[i]}]", end=" ")
                    check = input("이 맞고 다음 단계로 넘어가고 싶다면 그냥 스페이스를, 추가로 입력하고 싶다면 1을,"
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

            print(f"현재 어빌리티 스톤의 스펙은 {temp1} {temp1_num}, {temp2} {temp2_num}, {temp3} {temp3_num}입니다.")
            check = input("입력 내용이 정확하다면 그냥 스페이스를, 잘못 입력해서 다시 입력하고 싶다면 1을 입력해주세요: ")
            if check == "":
                abil_stone = {temp1: temp1_num, temp2: temp2_num, temp3: temp3_num}
                break
            elif check == "1":
                continue
            else:
                while check == "" or check == "1":
                    input("잘못 입력하셨습니다. 입력한 내용이 정확하다면 그냥 스페이스를, 수정하고 싶으시다면 1을 입력해주세요: ")
        except ValueError:
            print("잘못 입력하셨습니다. 숫자로 입력해주세요.")
    print("시간이 좀 걸립니다, 잠시 기다려주세요...")
    return qual + 1, feature_1, feature_2, feature_3, target_dic, abil_stone


# quality, feature1, feature2, feature3, target_dict, ability_stone 인자
def all_possible_set():
    quality = 0
    feature1 = 5
    feature2 = 1
    feature3 = 0
    target_dict = {"원한": 15, "바리케이드": 15, "슈퍼 차지": 15, "고독한 기사": 15, "결투의 대가": 15}
    ability_stone = {'원한': 7, "슈퍼 차지": 7, "이동속도 감소": 4}
    total_temp = -24  # 전설 각인서를 두 종류 다 읽어서 12씩 박을 수 있다고 가정
    for i in target_dict:
        total_temp += target_dict[i]
    for i in ability_stone:
        if "감소" in i:
            continue
        total_temp -= ability_stone[i]
    if total_temp > 40:
        print("불가능한 경우의 수입니다.")
        return
    # 목걸이 귀걸이1 귀걸이2 반지1 반지2 어빌스톤 각인서
    # 각각의 요소는 2개의 각인을 가지고 있고 1개의 디버프를 가지고 있다, 각인서 제외
    # *지금 디버프까지 계산해서 돌려주기엔 무리가 있을 듯*
    # 엑세서리들은 (5,3), (4,3), (3,3)이 가능
    # 목걸이는 5C2(10)*5=50가지 가능


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
                    if check or total[4] < 5:
                        continue
                    count += 1
                    # print(accessories, stone, book, total)
    print(count)


def find_min_set(engrave_dict):
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

    # 카테고리 설정
    driver.find_element_by_xpath('//*[@id="selCategoryDetail"]/div[1]').click()
    driver.find_element_by_xpath('//*[@id="selCategoryDetail"]/div[2]/label[10]').click()
    # 품질 설정
    quality = 1
    driver.find_element_by_xpath('//*[@id="modal-deal-option"]/div/div/div[1]/div[1]/table/tbody/tr[4]/td[2]/div/'
                                 'div[1]').click()
    driver.find_element_by_xpath(f'//*[@id="modal-deal-option"]/div/div/div[1]/div[1]/table/tbody/tr[4]/td[2]/div/'
                                 f'div[2]/label[{quality}]').click()
    # 전투 특성 설정
    driver.find_element_by_xpath('//*[@id="selEtc_0"]/div[1]').click()
    driver.find_element_by_xpath('//*[@id="selEtc_0"]/div[2]/label[2]').click()
    battle_dict = {"치명": 2, "특화": 3, "신속": 5}
    battle = "치명"
    driver.find_element_by_xpath('//*[@id="selEtcSub_0"]/div[1]').click()
    driver.find_element_by_xpath(f'//*[@id="selEtcSub_0"]/div[2]/label[{battle_dict[battle]}]').click()

    # 각인1 설정
    driver.find_element_by_xpath('//*[@id="selEtc_1"]/div[1]').click()
    driver.find_element_by_xpath('//*[@id="selEtc_1"]/div[2]/label[3]').click()
    engrave1 = "원한"
    driver.find_element_by_xpath('//*[@id="selEtcSub_1"]/div[1]').click()
    driver.find_element_by_xpath(f'//*[@id="selEtcSub_1"]/div[2]/label[{engrave_dict[engrave1]}]').click()

    # 각인2 설정
    driver.find_element_by_xpath('//*[@id="selEtc_2"]/div[1]').click()
    driver.find_element_by_xpath('//*[@id="selEtc_2"]/div[2]/label[3]').click()
    engrave2 = "돌격대장"
    driver.find_element_by_xpath('//*[@id="selEtcSub_2"]/div[1]').click()
    driver.find_element_by_xpath(f'//*[@id="selEtcSub_2"]/div[2]/label[{engrave_dict[engrave2]}]').click()

    # 각인 수치 설정
    input_box = driver.find_element_by_id("txtEtcMin_0")
    input_box.send_keys(5)
    driver.find_element_by_xpath('').click()

    # driver.find_element_by_xpath('//*[@id="modal-deal-option"]/div/div/div[2]/button[1]').click()
    # driver.find_element_by_xpath('').click()


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
    find_min_set(engrave_dic)
