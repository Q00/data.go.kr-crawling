#runtime중 메모리수정
import gevent.monkey
gevent.monkey.patch_all()
import config
import column
import requests
import pandas as pd
from lxml import etree
import gevent.pool
import gevent.queue
from bs4 import BeautifulSoup as BS
import sys

#prepare worker
#pool : request용 worker ( 전체워커)
#pool_excel : excel용 worker ( 엑셀 워커)
pool = gevent.pool.Pool(15)
pool_excel = gevent.pool.Pool(15)
queue = gevent.queue.Queue()

#api key loading
key = config.go_data_api_key

#url list 이후에 좀더 일반화해서 편히할 예정
#해당 부분 csv파일을 만들어 넣었을때 자동으로 파싱할 수 있게  만들 예정
baseUrl = 'http://apis.data.go.kr/1470000/DURPrdlstInfoService/'
urlList = 'getDurPrdlstInfoList','getSeobangjeongPartitnAtentInfoList','getEfcyDplctInfoList','getOdsnAtentInfoList','getMdctnPdAtentInfoList','getCpctyAtentInfoList','getPwnmTabooInfoList','getSpcifyAgrdeTabooInfoList','getUsjntTabooInfoList'

main_row=0

def makeCSV(item):
    global main_row
    main_row+=1
    print(main_row)
    print(item)
    #global main_row
    #item을 하나씩 받아 csv파일로 무조건 add
    #if main_row ==1: 
    #    for child in item.children:
    #        print(child.name)
    #        if child != '\n' and child.name != 'TYPE_NAME':
    #            evalue = column.typeList[addUrl][child.name]
                #csv 파일 인덱싱 부분 추가 필요

    #csv 파일 body apeend
    #for child in item.children:
    #    if child != '\n' and child.name != 'TYPE_NAME':
    #        evalue = str(child.text)
                #csv 파일 apeend 부분 추가 필요


def getData():
    #가지고 있는 url만큼만 loop
    while True:
        try:
            #저장되어있는 link를 queue에서 가져옴
            #pool의 worker들이 link로 request 동기보다 n배 빠름
            if not queue.empty() :
                link = queue.get(timeout=0)
                if link != "":
                    getdata = requests.get(link)
                    soup = BS(getdata.text,'lxml-xml') 
                    #validation check
                    okflag = soup.find('resultCode')
                     
                    if okflag.text != '00':
                        print("okflag: ",okflag.text)
                        
                        raise ValueError('okcode is not 00')    
                    else:
                        #검색잘되면 엑셀 파싱
                        #pool map method vs pool map_async
                        #어떤것이 더 효율이 좋을지 결정필요
                        #pool 워커안에 pool넣을 수 있는지 확인 필요
                        pool_excel.map(makeCSV,soup.find_all('item'))


            #param이 다 추가된 link에 대해서 queue에 저장 getData()의 3번째줄에서 저장되어있는 link가져감
            
            for addUrl in urlList:
                for letter in range(ord('a'), ord('z')+1):
                    params = {'itemname': chr(letter), 'servicekey': key, 'numofrows':100}
                    if addUrl != 'getdurprdlstinfolist':
                        params.update({'typename' : column.typeName[addUrl]})
                    params_str = "&".join("%s=%s" % (k,v) for k,v in params.items())
                    requestUrl = baseUrl + addUrl
                    #print(requesturl)
                    try:
                        #request data
                        #print('데이터 가져오는중 검색한 알파벳 :', chr(letter))
                        getdata = requests.get(requestUrl, params=params_str)
                    except:
                        print('request error')
                    try:
                        soup = BS(getdata.text, 'lxml-xml') 
                    
                        #print(soup.prettify) 
                        #check page
                        totalcount = int(soup.find('totalCount').text)
                        print('총 개수: ',totalcount)
                        page = int(totalcount/100) + 1
                        #cell number parameter
                        print('페이지 : ',page)
                        for i in range(page):
                            params_str2 = params_str
                            params_str2+= '&pageno='+str(i+1)
                            #request again
                            queue.put(requestUrl+'?'+params_str2)
                            #print(requestUrl+params_str2)
             
                    except:
                        print('crwaling error : ',sys.exc_info()[1])
        except gevent.queue.Empty:
            break
    print('stop crwaling')

#queue init
queue.put("")
pool.spawn(getData)

#give worker pool
print('start crwaling')
#while not pool.free_count() == 15:
while True:
    gevent.sleep(0.1)
    for x in range(0, min(queue.qsize(), pool.free_count())):
        pool.spawn(getData)

#wait for everything complete
pool.join()
