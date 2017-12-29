import os
import datetime
import sys
import numpy as np
import pandas as pd
import xlsxwriter
from getRealasset import get_naver_realasset
from getAreaCode import get_areacode


def get_code(gui, area):
    df_areacode = get_areacode()
    gui.progress['value'] = 10
    area_code = df_areacode[df_areacode['법정동명'].str.contains(area)]
    gui.progress['value'] = 20
    return area_code

def makeData(gui, area_code, trade, asset):
    now = datetime.datetime.now()
    area_name = ''
    area = ''
    data = pd.DataFrame()
    length = len(area_code)
    for i in range(length):
        area_nm = area_code.loc[:, '법정동명'].values[i]
        area_cd = area_code.loc[:, '법정동코드'].values[i]
        area = area_nm + ' (' + area_cd + ')' + ' [' + str(i+1) + '/' + str(length) + ']'
        gui.areamsg.set('%s' % (area))
        area_name = area_name + '_' + area_nm
        for j in range(1,100):
            df_tmp = get_naver_realasset(area_cd, trade=trade, hscp=asset, page=j)
            if len(df_tmp) <= 0:
                break
            data = data.append(df_tmp, ignore_index=True)
        gui.progress['value'] = 20 + 70 * i/length 
    fileName = now.strftime('%Y-%m-%d') + area_name + '.xlsx'
    return data, fileName

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


def get_Naver_Data(gui, area, trade, asset, folder):
    try:
        # Display progress bar
        gui.progress['value'] = 0
        gui.progress['maximum'] = 100

        # Get information
        area_code = get_code(gui, area)
        
        # df.to_excel(saveFileName, sheet_name='Sheet1', header=True)
        # Make directory if there is not directory and valify directory path.
        try:
            os.path.isdir(folder)
        except:
            os.makedirs(folder)
            gui.statusmsg.set('There is not folder. We make a folder.....')

        # Call back making contents and saving a file using function method.
        gui.statusmsg.set('Start Scrawling..')
        data_file, saveFileName = makeData(gui, area_code, trade, asset)
        gui.stitlemsg.set('%s' % (saveFileName))

        saveExcel(gui, folder, saveFileName, data_file)

        if gui.flag:
            gui.statusmsg.set('Scrawling Complete!!')
        else:
            gui.statusmsg.set('Scrawling Canceled by User!')

    except:
        gui.statusmsg.set('Errors Scrawling')
        gui.progress.stop()
        return
    
