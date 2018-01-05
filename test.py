from getData import *
from getRealasset import get_naver_realasset
from land import *
import requests
from datetime import datetime
from bs4 import BeautifulSoup

area = '흑석동'

a1 = '1159010500'
a2 = '2920012400'


def realasset(area_code, asset='A01', trade='A1', hscp='', page=1):

    url = 'http://land.naver.com/article/articleList.nhn?' \
        + 'rletTypeCd=' + asset \
        + '&tradeTypeCd=' + trade \
        + '&hscpTypeCd=' + hscp \
        + '&cortarNo=' + area_code \
        + '&page=' + str(page)

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    table = soup.find('table')
    trs = table.tbody.find_all('tr')
    if '등록된 매물이 없습니다' in trs[0].text:
        return pd.DataFrame()

    value_list = []

    # 거래, 종류, 확인일자, 매물명, 면적(㎡), 층, 매물가(만원), 연락처
    for tr in trs[::2]:
        tds = tr.find_all('td')
        cols = [' '.join(td.text.strip().split()) for td in tds]

        if '_thumb_image' not in tds[3]['class']:  # 현장확인 날짜와 이미지가 없는 행
            cols.insert(3, '')

        # print(cols)
        거래 = cols[0]
        종류 = cols[1]
        확인일자 = datetime.strptime(cols[2], '%y.%m.%d.')
        현장확인 = cols[3]
        매물명 = cols[4]
        면적 = cols[5]
        공급면적 = re.findall('공급면적(.*?)㎡', 면적)[0].replace(',', '')
        전용면적 = re.findall('전용면적(.*?)㎡', 면적)[0].replace(',', '')
        공급면적 = float(공급면적)
        전용면적 = float(전용면적)
        층 = cols[6]
        if cols[7].find('호가일뿐 실거래가로확인된 금액이 아닙니다') >= 0:
            pass  # 단순호가 별도 처리하고자 하면 내용 추가
        # 월세 data 내 '/' 로 인해 파싱 에러 발생 -> 수정 필요
        try:
            매물가 = int(cols[7].split(' ')[0].replace(',', ''))
        except ValueError:
            매물가 = str(cols[7].split(' ')[0].replace(',', ''))
        # 매물가 = int(cols[7].split(' ')[0].replace(',', ''))
        연락처 = cols[8]

        value_list.append([거래, 종류, 확인일자, 현장확인, 매물명, 공급면적, 전용면적, 층, 매물가, 연락처])

    cols = ['거래', '종류', '확인일자', '현장확인', '매물명',
            '공급면적', '전용면적', '층', '매물가', '연락처']
    df = pd.DataFrame(value_list, columns=cols)
    return df


if __name__ == '__main__':
    # obj = MyLand()
    # asset = obj.getAsset()
    # trade = obj.radVar.get()
    # print(trade, asset)

    # obj.checkVar1.set(value=1)
    # obj.checkVar2.set(value=0)
    # asset = obj.getAsset()
    # print(asset)

    # area_code = get_code(obj, area)
    # print(area_code)

    # a3 = area_code.loc[:, '법정동코드'].values[0]
    # a4 = area_code.loc[:, '법정동코드'].values[0]
    
    # df = pd.DataFrame()
    # for i in range(1, 100):
    #     df_tmp = get_naver_realasset(a1, page=i)
    #     if len(df_tmp) <= 0:
    #         break
    #     df = df.append(df_tmp, ignore_index=True)

    # print(df)

    # data, filename = makeData(obj, area_code, trade, asset)
    # print(data)
    # print(filename)

    # a1 = '1159010500'
    area_code = '1162010100'
    trade = 'B2'
    asset = 'A01%3AA03%3AA04'
    
    df = realasset(area_code, trade=trade, hscp=asset)
    df = get_naver_realasset(area_code, trade=trade, hscp=asset)

    print(df)
