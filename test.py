from getData import *
from getRealasset import get_naver_realasset
from land import *
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import time


# area = '흑석동'
area = '동안구 평촌동'
trade = 'B1'  # (거래종류): all=전체, A1=매매, B1=전세, B2=월세, B3=단기임대
asset = 'A01%3AA03%3AA04'  # 아파트=A01, 주상복합=A03, 재건축=A04

a1 = '1159010500'  # 서울특별시 동작구 흑석동
a2 = '4117310300'  # 경기도 안양시 동안구 평촌동


if __name__ == '__main__':
    obj = MyLand()
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

    area_code = get_code(obj, area)
    print(area_code)
    df = pd.DataFrame()

    length = len(area_code)
    for i in range(length):
        print(i)
        area_cd = area_code.loc[:, '법정동코드'].values[i]

        for j in range(1, 200):
            time.sleep(5)
            df_tmp = get_naver_realasset(
                area_cd, trade=trade, hscp=asset, page=j)
            print(j)
            if len(df_tmp) <= 0:
                break
            df = df.append(df_tmp, ignore_index=True)
    
    print(df)
