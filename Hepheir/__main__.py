import json

from requests import request


_raw_json_request = '''
{\"firstCategory\":\"200000\",\"secondCategory\":\"0\",\"classNo\":\"\",\"itemTier\":\"3\",\"itemGrade\":\"5\",\"itemLevelMin\":\"0\",\"itemLevelMax\":\"1600\",\"itemName\":\"\",\"gradeQuality\":\"\",\"skillOptionList\":[{\"firstOption\":\"\",\"secondOption\":\"\",\"minValue\":\"\",\"maxValue\":\"\"},{\"firstOption\":\"\",\"secondOption\":\"\",\"minValue\":\"\",\"maxValue\":\"\"},{\"firstOption\":\"\",\"secondOption\":\"\",\"minValue\":\"\",\"maxValue\":\"\"}],\"etcOptionList\":[{\"firstOption\":\"2\",\"secondOption\":\"18\",\"minValue\":\"\",\"maxValue\":\"\"},{\"firstOption\":\"\",\"secondOption\":\"\",\"minValue\":\"\",\"maxValue\":\"\"},{\"firstOption\":\"\",\"secondOption\":\"\",\"minValue\":\"\",\"maxValue\":\"\"},{\"firstOption\":\"\",\"secondOption\":\"\",\"minValue\":\"\",\"maxValue\":\"\"}],\"pageNo\":2}
'''


def main():
    response = request(
        method='POST',
        url='https://lostark.game.onstove.com/Auction/GetAuctionListV2',
        headers = {
            'Content-Type': 'text/html; charset=utf-8'
        },
        data={
            'request': json.loads(_raw_json_request.strip()),
            'pushKey': None,
            'tooltipData': '',
        }
    )
    with open('test.html', 'w', encoding='utf-8') as f:
        f.write(response.text)


if __name__ == '__main__':
    main()
