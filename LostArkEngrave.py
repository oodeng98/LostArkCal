import selenium

from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


def receive_input_data():
    engrave_dict = {"각성": 1, "갈증": 2, "강령술": 3, "강화 무기": 4, "강화 방패": 5, "결투의 대가": 6, "고독한 기사": 7, "광기": 8,
                    "광전사의 비기": 9, "구슬동자": 10, "굳은 의지": 11, "극의: 체술": 12, "급소 타격": 13, "기습의 대가": 14, "긴급구조": 15,
                    "넘치는 교감": 16, "달의 소리": 17, "달인의 저력": 18, "돌격대장": 19, "두 번째 동료": 20, "마나 효율 증가": 21,
                    "마나의 흐름": 22, "멈출 수 없는 충동": 23, "바리케이드": 24, "버스트": 25, "번개의 분노": 26, "부러진 뼈": 27,
                    "분노의 망치": 28, "분쇄의 주먹": 29, "불굴": 30, "사냥의 시간": 31, "상급 소환사": 32, "선수필승": 33, "세맥타통": 34,
                    "속전속결": 35, "슈퍼 차지": 36, "승부사": 37, "시선 집중": 38, "실드 관통": 39, "심판자": 40, "아드레날린": 41,
                    "아르데타인의 기술": 42, "안정된 상태": 43, "약자 무시": 44, "에테르 포식자": 45, "여신의 가호": 46, "역천지체": 47,
                    "연속 포격": 48, "예리한 둔기": 49, "오의 강화": 50, "오의난무": 51, "완벽한 억제": 52, "원한": 53, "위기 모면": 54,
                    "일격필살": 55, "잔재된 기운": 56, "저주받은 인형": 57, "전문의": 58, "전투 태세": 59, "절실한 구원": 60, "절정": 61,
                    "절제": 62, "정기 흡수": 63, "정밀 단도": 64, "죽음의 습격": 65, "중갑 착용": 66, "중력 수련": 67, "진실된 용맹": 68,
                    "진화의 유산": 69, "질량 증가": 70, "초심": 71, "최대 마나 증가": 72, "추진력": 73, "축복의 오라": 74, "충격 단련": 75,
                    "타격의 대가": 76, "탈출의 명수": 77, "폭발물 전문가": 78, "피스메이커": 79, "핸드거너": 80, "화력 강화": 81,
                    "황제의 칙령": 82, "황후의 은총": 83}
    bad_engrave_dict = {"공격력 감소": 0, "공격속도 감소": 0, "방어력 감소": 0, "이동속도 감소": 0}

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
                ability_stone = {temp1: temp1_num, temp2: temp2_num, temp3: temp3_num}
                break
            elif check == "1":
                continue
            else:
                while check == "" or check == "1":
                    input("잘못 입력하셨습니다. 입력한 내용이 정확하다면 그냥 스페이스를, 수정하고 싶으시다면 1을 입력해주세요: ")
        except ValueError:
            print("잘못 입력하셨습니다. 숫자로 입력해주세요.")

    while True:
        try:
            print("\n현재 읽은 각인, 혹은 읽어야 하는 각인을 입력해주세요.")
            for i in target_dic:
                print(f"[{i}]", end=" ")
            temp1 = input("중 읽은 각인을 입력해주세요: ")
            while temp1 not in target_dic:
                temp1 = input("잘못 입력하셨거나 목표 각인에 해당하지 않는 각인입니다. 다시 입력해주세요.")
            temp1_num = int(input(f"{temp1} 각인의 보유 각인 수치를 입력해주세요: "))
            if temp1_num % 3:
                print("각인 수치는 3으로 나눠지는 숫자입니다. 다시 입력해주세요")
                continue

            for i in target_dic:
                if i == temp1:
                    continue
                print(f"[{i}]", end=" ")
            temp2 = input("중 읽은 각인을 입력해주세요: ")
            while temp2 not in target_dic:
                temp2 = input("잘못 입력하셨거나 목표 각인에 해당하지 않는 각인입니다. 다시 입력해주세요.")
            if temp1 == temp2:
                print("다른 종류의 각인을 입력해야 합니다. 처음부터 다시 입력해주세요.")
                continue
            temp2_num = int(input(f"{temp2} 각인의 어빌리티 스톤 수치를 입력해주세요: "))
            if temp2_num % 3:
                print("각인 수치는 3으로 나눠지는 숫자입니다. 다시 입력해주세요")
                continue

            print(f"현재 보유중인 각인 수치는 {temp1} {temp1_num}, {temp2} {temp2_num}입니다. ")
            check = input("입력 내용이 정확하다면 그냥 스페이스를, 잘못 입력해서 다시 입력하고 싶다면 1을 입력해주세요: ")
            if check == "":
                book_engrave = {temp1: temp1_num, temp2: temp2_num}
                break
            elif check == "1":
                continue
            else:
                while check == "" or check == "1":
                    input("잘못 입력하셨습니다. 입력한 내용이 정확하다면 그냥 스페이스를, 수정하고 싶으시다면 1을 입력해주세요: ")
        except ValueError:
            print("각인 수치는 숫자로 입력해야합니다. 다시 입력해주세요.")

    print("시간이 좀 걸립니다, 잠시 기다려주세요...")
    return qual + 1, feature_1, feature_2, feature_3, target_dic, ability_stone, book_engrave


def find_min_set(quality, feature1, feature2, feature3, target_dict):
    quality = 8
    feature1 = 5
    feature2 = 1
    feature3 = 0
    target_dict = {"예리한 둔기": 3, "원한": 3, "돌격대장": 3, "상급 소환사": 3, "넘치는 교감": 1}
    driver = webdriver.Chrome('chromedriver')
    driver.implicitly_wait(5)

    driver.get(url='https://lostark.game.onstove.com/Auction')

    search_box = driver.find_element_by_id('txtItemName')

    # driver.find_element_by_xpath('').click()
    driver.find_element_by_xpath('//*[@id="selItemGrade"]/div[1]').click()
    driver.find_element_by_xpath('//*[@id="selItemGrade"]/div[2]/label[7]').click()
    driver.find_element_by_xpath('//*[@id="selItemTier"]/div[1]').click()
    driver.find_element_by_xpath('//*[@id="selItemTier"]/div[2]/label[4]').click()
    driver.find_element_by_xpath('//*[@id="lostark-wrapper"]/div/main/div/div[3]/div[2]/form/fieldset/div/div[5]'
                                 '/button[2]').click()
    driver.implicitly_wait(5)

    driver.find_element_by_xpath('//*[@id="selCategoryDetail"]/div[1]').click()
    driver.find_element_by_xpath('//*[@id="selCategoryDetail"]/div[2]/label[10]').click()
    # 품질을 입력받는다는 가정
    driver.find_element_by_xpath('//*[@id="modal-deal-option"]/div/div/div[1]/div[1]/table/tbody/tr[4]/td[2]/div/'
                                 'div[1]').click()
    driver.find_element_by_xpath(f'//*[@id="modal-deal-option"]/div/div/div[1]/div[1]/table/tbody/tr[4]/td[2]/div/'
                                 f'div[2]/label[{quality}]').click()


    # driver.close()


if __name__ == "__main__":
    find_min_set(receive_input_data())
