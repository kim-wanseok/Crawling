from getData import *
from getRealasset import get_naver_realasset
from getAreaCode import get_code


area = '흑석동'

area_code = get_code(area)
print(area_code)

a1 = '1159010500'
a2 = '2920012400'

a3 = area_code.loc[:, '법정동코드'].values[0]
a4 = area_code.loc[:, '법정동코드'].values[0]

df = pd.DataFrame()
for i in range(1,100):
    df_tmp = get_naver_realasset(a1, i)
    if len(df_tmp) <=0:
        break
    df = df.append(df_tmp, ignore_index=True)

print(df)