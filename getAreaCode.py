import pandas as pd


def get_areacode():
    '''
    법정동 코드 추출
    기본 DATA 소스 : https://www.code.go.kr/ 행정표준코드 관리시스템 에서 다운
    '.txt' 파일 다운 url : https://goo.gl/tM6r3v
    '''
    df_areacode = pd.read_csv('https://goo.gl/tM6r3v',
                              sep='\t', dtype={'법정동코드': str, '법정동명': str})
    df_areacode = df_areacode[df_areacode['폐지여부'] == '존재']
    df_areacode = df_areacode[['법정동코드', '법정동명']]
    return df_areacode


def get_province():
    '''
    시/도 법정코드 추출
    '\d{2}0{8}' : 임의정수 2개, 숫자 0이 8개 
    '3611000000' : 세종특별자치시 
    '''
    df_areacode = get_areacode()
    df_province = df_areacode[df_areacode['법정동코드'].str.contains(
        '\d{2}0{8}|36110{6}')]
    return df_province


def get_county():
    '''
    구/군 법정코드 추출
    '\d{5}0{5}' : 임의정수 5개, 숫자 0이 5개 
    '''
    df_areacode = get_areacode()
    df_county = df_areacode[df_areacode['법정동코드'].str.contains('\d{5}0{5}')]
    return df_county
