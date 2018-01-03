from getData import *
from getRealasset import get_naver_realasset
from getAreaCode import get_code
from land import *

# area = '흑석동'

# area_code = get_code(area)
# print(area_code)

# a1 = '1159010500'
# a2 = '2920012400'

# a3 = area_code.loc[:, '법정동코드'].values[0]
# a4 = area_code.loc[:, '법정동코드'].values[0]

# df = pd.DataFrame()
# for i in range(1,100):
#     df_tmp = get_naver_realasset(a1, page=i)
#     if len(df_tmp) <=0:
#         break
#     df = df.append(df_tmp, ignore_index=True)

# print(df)

if __name__ == '__main__':
    obj = MyLand()
    asset = obj.getAsset()
    trade = obj.radVar.get()
    print(trade, asset)

    # obj.checkVar1.set(value=1)
    # obj.checkVar2.set(value=0)
    # asset = obj.getAsset()
    # print(asset)
    area = '흑석동'

    area_code = get_code(obj, area)
    print(area_code)

    data, filename = makeData(obj, area_code, trade, asset)
    print(data)
    print(filename)

    # a1 = '1159010500'
    # df = get_naver_realasset(area_code, trade=trade, hscp=asset)

    # print(df)
