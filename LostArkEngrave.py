import selenium

from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


def receive_input_data():
    engrave_dict = {"각성": 0, "갈증": 0, "강령술": 0, "강화 무기": 0, "강화 방패": 0, "결투의 대가": 0, "고독한 기사": 0, "광기": 0,
                    "광전사의 비기": 0, "구슬동자": 0, "굳은 의지": 0, "극의: 체술": 0, "급소 타격": 0, "기습의 대가": 0, "긴급구조": 0,
                    "넘치는 교감": 0, "달의 소리": 0, "달인의 저력": 0, "돌격대장": 0, "두 번째 동료": 0, "마나 효율 증가": 0,
                    "마나의 흐름": 0, "멈출 수 없는 충동": 0, "바리케이드": 0, "버스트": 0, "번개의 분노": 0, "부러진 뼈": 0,
                    "분노의 망치": 0, "분쇄의 주먹": 0, "불굴": 0, "사냥의 시간": 0, "상급 소환사": 0, "선수필승": 0, "세맥타통": 0,
                    "속전속결": 0, "슈퍼 차지": 0, "승부사": 0, "시선 집중": 0, "실드 관통": 0, "심판자": 0, "아드레날린": 0,
                    "아르데타인의 기술": 0, "안정된 상태": 0, "약자 무시": 0, "에테르 포식자": 0, "여신의 가호": 0, "역천지체": 0,
                    "연속 포격": 0, "예리한 둔기": 0, "오의 강화": 0, "오의난무": 0, "완벽한 억제": 0, "원한": 0, "위기 모면": 0,
                    "일격필살": 0, "잔재된 기운": 0, "저주받은 인형": 0, "전문의": 0, "전투 태세": 0, "절실한 구원": 0, "절정": 0,
                    "절제": 0, "정기 흡수": 0, "정밀 단도": 0, "죽음의 습격": 0, "중갑 착용": 0, "중력 수련": 0, "진실된 용맹": 0,
                    "진화의 유산": 0, "질량 증가": 0, "초심": 0, "최대 마나 증가": 0, "추진력": 0, "축복의 오라": 0, "충격 단련": 0,
                    "타격의 대가": 0, "탈출의 명수": 0, "폭발물 전문가": 0, "피스메이커": 0, "핸드거너": 0, "화력 강화": 0,
                    "황제의 칙령": 0, "황후의 은총": 0}

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
            if feature_1 + feature_2 + feature_3 > 6:
                print("악세서리의 총 개수가 6을 초과하였습니다. 다시 입력해주세요.")
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
            target = input("목표 각인을 입력해주세요, 정확한 이름으로 입력하셔야 합니다, ex)예리한 둔기(O), 예둔(X), 예리한둔기(X), "
                           "그만 입력하시려면 그냥 스페이스를, 처음부터 다시 입력하시려면 1을 입력해주세요: ")
            if target not in engrave_dict:
                if target == '':
                    print("목표 각인이", end=" ")
                    for i in target_dic:
                        print(f"[{i} {target_dic[i]}]", end=" ")
                    check = input("이 맞고 다음 단계로 넘어가고 싶다면 그냥 스페이스를, 추가로 입력하고 싶다면 1을,"
                                  " 입력이 잘못되서 처음부터 입력하고싶다면 2를 입력해주세요: ")
                    if check == '':
                        print("시간이 좀 걸립니다, 잠시 기다려주세요...")
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

    return qual + 1, feature_1, feature_2, feature_3, target_dic


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
