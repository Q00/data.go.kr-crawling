import config
import bs4
import openpyxl

#api key loading
key = config.go_data_api_key

#excel open
wb = openpyxl.Workbook()
ws = wb.active

#make cell head

#get Data
baseUrl = 'http://apis.data.go.kr/1470000/DURPrdlstInfoService'
urlList = 'getDurPrdlstInfoList','getSeobangjeongPartitnAtentInfoList','getEfcyDplctInfoList','getOdsnAtentInfoList','getMdctnPdAtentInfoList','getCpctyAtentInfoList','getPwnmTabooInfoList','getSpcifyAgrdeTabooInfoList','getUsjntTabooInfoList'



