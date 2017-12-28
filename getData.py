import os
import datetime
import sys
import numpy as np
import pandas as pd
import xlsxwriter
from getRealasset import get_naver_realasset
from getAreaCode import get_code


def makeFileName(area_code):
    now = datetime.datetime.now()
    area_name = ''
    if len(area_code.index) <= 1:
        area_name = area_code.loc[:,'법정동명'].values[0]
    else:
        for i in range(len(area_code.index)):
            area_name = area_name + '_' + area_code.loc[:, '법정동명'].values[i]
            area = area_code.loc[:, '법정동코드'].values[i-1]
            print(area)
    fileName = now.strftime('%Y-%m-%d') + area_name + '.xlsx'
    return fileName

def makeData(area_code):
    data = pd.DataFrame()
    length = len(area_code)
    for i in range(length):
        area = area_code.loc[:, '법정동코드'].values[i]
        for j in range(1,100):
            df_tmp = get_naver_realasset(area, j)
            if len(df_tmp) <= 0:
                break
            data = data.append(df_tmp, ignore_index=True)
    return data

def saveExcel(gui, folder, filename, content):
    saveFile = folder + '/' + filename
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    try:
        writer = pd.ExcelWriter(saveFile, engine='xlsxwriter')
    except:
        gui.statusmsg("SORRY: We don't open a file. Please Check a filename(%s) in folder." %(filename))
        return

    # Convert the dataframe to an XlsxWriter Excel object. Note that we turn off
    # the default header and skip one row to allow us to insert a user defined
    # header.
    content.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False)

    # Get the xlsxwriter workbook and worksheet objects.
    workbook  = writer.book
    worksheet = writer.sheets['Sheet1']

    # Add a header format.
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#D7E4BC',
        'border': 1})

    # Write the column headers with the defined format.
    for col_num, value in enumerate(content.columns.values):
        worksheet.write(0, col_num + 1, value, header_format)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    gui.progress['value'] = 100


def get_Naver_Data(gui, area, folder):
    try:
        area_code = get_code(area)
        saveFileName = makeFileName(area_code)
        gui.stitlemsg.set('%s' % (saveFileName))
        
        gui.statusmsg.set('Start Scrawling..')

        # df.to_excel(saveFileName, sheet_name='Sheet1', header=True)
        # Make directory if there is not directory and valify directory path.
        try:
            os.path.isdir(folder)
        except:
            os.makedirs(folder)
            gui.statusmsg.set('There is not folder. We make a folder.....')

        # Display progress bar
        gui.progress['value'] = 0
        gui.progress['maximum'] = 100

        # Call back making contents and saving a file using function method.
        data_file = makeData(area_code)
        # data_file = pd.DataFrame(np.random.randint(low=0, high=10, size=(5,5)), columns=['a','b','c','d','e'])
        saveExcel(gui, folder, saveFileName, data_file)

        if gui.flag:
            gui.statusmsg.set('Scrawling Complete!!')
        else:
            gui.statusmsg.set('Scrawling Canceled by User!')

    except:
        gui.statusmsg.set('Errors Scrawling')
        return
    
