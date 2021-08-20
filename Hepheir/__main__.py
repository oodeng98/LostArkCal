from requests import Request, Session


QUERY = {
    "request[firstCategory]": "20000", # 카테고리
    "request[secondCategory]": "0",
    # 20000, 0 은 장신구를 선택하기 위한 값임. (전체 선택하려면 위 값 둘다 빈 문자열로 변경)

    "request[classNo]": "",
    "request[itemTier]": "",
    "request[itemGrade]": "",

    # 아이템 레벨
    "request[itemLevelMin]": "0",
    "request[itemLevelMax]": "1600",


    "request[itemName]": "",
    "request[gradeQuality]": "",

    # 스킬 상세 옵션
    "request[skillOptionList][0][firstOption]": "",
    "request[skillOptionList][0][secondOption]": "",
    "request[skillOptionList][0][minValue]": "",
    "request[skillOptionList][0][maxValue]": "",

    "request[skillOptionList][1][firstOption]": "",
    "request[skillOptionList][1][secondOption]": "",
    "request[skillOptionList][1][minValue]": "",
    "request[skillOptionList][1][maxValue]": "",

    "request[skillOptionList][2][firstOption]": "",
    "request[skillOptionList][2][secondOption]": "",
    "request[skillOptionList][2][minValue]": "",
    "request[skillOptionList][2][maxValue]": "",

    # 기타 상세 옵션
    "request[etcOptionList][0][firstOption]": "",
    "request[etcOptionList][0][secondOption]": "",
    "request[etcOptionList][0][minValue]": "",
    "request[etcOptionList][0][maxValue]": "",

    "request[etcOptionList][1][firstOption]": "",
    "request[etcOptionList][1][secondOption]": "",
    "request[etcOptionList][1][minValue]": "",
    "request[etcOptionList][1][maxValue]": "",

    "request[etcOptionList][2][firstOption]": "",
    "request[etcOptionList][2][secondOption]": "",
    "request[etcOptionList][2][minValue]": "",
    "request[etcOptionList][2][maxValue]": "",

    "request[etcOptionList][3][firstOption]": "",
    "request[etcOptionList][3][secondOption]": "",
    "request[etcOptionList][3][minValue]": "",
    "request[etcOptionList][3][maxValue]": ""
}


def main(kwargs):
    session = Session()
    request = Request(
        method='POST',
        url='https://lostark.game.onstove.com/Auction/GetAuctionListV2',
        headers={
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        },
        data=kwargs
    )

    response = session.send(request.prepare())
    return response.text


if __name__ == '__main__':
    main(QUERY)
