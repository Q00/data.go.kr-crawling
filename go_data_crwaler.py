#-*- coding: utf-8 -*-
import config
import column
import openpyxl
import requests 
import urllib
from bs4 import BeautifulSoup as BS
from lxml import etree

#api key loading
key = config.go_data_api_key
#print(key)
#excel open
wb = openpyxl.Workbook()
ws = wb.active

#make cell head

#get Data
baseUrl = 'http://apis.data.go.kr/1470000/DURPrdlstInfoService/'
urlList = 'getDurPrdlstInfoList','getSeobangjeongPartitnAtentInfoList','getEfcyDplctInfoList','getOdsnAtentInfoList','getMdctnPdAtentInfoList','getCpctyAtentInfoList','getPwnmTabooInfoList','getSpcifyAgrdeTabooInfoList','getUsjntTabooInfoList'

for addUrl in urlList:
    #a~z loop
    for letter in range(ord('a'), ord('z')+1):
        params = {'itemName': chr(letter), 'Servicekey': key, 'numOfRows':1}
        params_str = "&".join("%s=%s" % (k,v) for k,v in params.items())
        requesturl = baseUrl + addUrl
        #print(requesturl)
        try:
            getdata = requests.get(requesturl, params=params_str)
        except:
            print('request error')
        try:
            soup = BS(getdata.text, 'lxml-xml') 
            #print(soup.prettify)
            okflag = soup.find('resultCode')
            if okflag.text != '00':
                print(okflag.text)
                raise ValueError('okcode is not 00')    
            else:
                totalCount = int(soup.find('totalCount').text)
                page = int(totalCount/100) + 1
                #print(page)
                for item in soup.find_all('item'):
                    #print(item)
                    main_row = 1 
                    cell_num = 1
                    for child in item.children:
                        if child != '\n':
                            print(child.name)
                            #print(child.contents)
                            #print(column.getDurPrdlstInfoList[child.name])
                            #엑셀 헤드 부분
                            ws.cell(1,cell_num).value = column.getDurPrdlstInfoList[child.name]
        except ValueError as error:
            print(error) 
        break
    break


