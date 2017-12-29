import re
import numpy as np
import pandas as pd
import requests
from datetime import datetime
from bs4 import BeautifulSoup


def get_naver_realasset(area_code, asset='A01', trade='A1', hscp='', page=1):
    '''
    rletTypeCd: A01=아파트, A02=오피스텔, B01=분양권, 주택=C03, 토지=E03, 원룸=C01,
                상가=D02, 사무실=D01, 공장=E02, 재개발=F01, 건물=D03
    tradeTypeCd (거래종류): all=전체, A1=매매, B1=전세, B2=월세, B3=단기임대
    hscpTypeCd (매물종류): 아파트=A01, 주상복합=A03, 재건축=A04 (복수 선택 가능)
    cortarNo(법정동코드): (예: 1168010600 서울시, 강남구, 대치동)
    '''
    if hscp == '':
        hscp = 'A01%3AA03%3AA04'
    else:
        hscp = hscp

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
        매물가 = int(cols[7].split(' ')[0].replace(',', ''))  # 월세 data 내 '/' 로 인해 파싱 에러 발생 -> 수정 필요
        연락처 = cols[8]

        value_list.append([거래, 종류, 확인일자, 현장확인, 매물명, 공급면적, 전용면적, 층, 매물가, 연락처])

    cols = ['거래', '종류', '확인일자', '현장확인', '매물명',
            '공급면적', '전용면적', '층', '매물가', '연락처']
    df = pd.DataFrame(value_list, columns=cols)
    return df
