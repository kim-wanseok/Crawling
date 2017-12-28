import pandas as pd


def get_areacode():
    df_areacode = pd.read_csv('https://goo.gl/tM6r3v',
                              sep='\t', dtype={'법정동코드': str, '법정동명': str})
    df_areacode = df_areacode[df_areacode['폐지여부'] == '존재']
    df_areacode = df_areacode[['법정동코드', '법정동명']]
    return df_areacode


def get_province():
    df_areacode = get_areacode()
    df_province = df_areacode[df_areacode['법정동코드'].str.contains(
        '\d{2}0{8}|36110{6}')]
    return df_province

def get_code(area):
    df_areacode = get_areacode()
    area_code = df_areacode[df_areacode['법정동명'].str.contains(area)]
    return area_code
