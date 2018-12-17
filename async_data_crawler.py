#runtime중 메모리수정
import gevent.monkey
gevent.monkey.patch_all()
import config
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
error_count =0
main_row=0
#url list 이후에 좀더 일반화해서 편히할 예정
#해당 부분 csv파일을 만들어 넣었을때 자동으로 파싱할 수 있게  만들 예정
baseUrl = 'http://apis.data.go.kr/1470000/DURPrdlstInfoService/'

def makeCSV(item):
    global main_row
    main_row+=1
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
    global error_count 
    error_log = open('./err.txt',mode='a')
    while not queue.empty():
            #저장되어있는 link를 queue에서 가져옴
            #pool의 worker들이 link로 request 동기보다 n배 빠름
                link = queue.get(timeout=0)
                if link != "":
                    gevent.sleep(0.3)
                    getdata = requests.get(link)
                    soup = BS(getdata.text,'lxml-xml') 
                    #validation check
                    okflag = soup.find('resultCode')
                    try:
                        if okflag.text != '00':
                            print("okflag: ",okflag.text)
                            
                            raise ValueError('okcode is not 00')    
                        else:
                            #검색잘되면 엑셀 파싱
                            #pool map method vs pool map_async
                            #어떤것이 더 효율이 좋을지 결정필요
                            print(len(soup.find_all('item')))
                            pool_excel.map(makeCSV,soup.find_all('item'))
                    
                    except:
                        error_log.write(link+'\n')
                        error_log.write('==================================\n')
                        error_count+=1
                        error_log.write(str(error_count)+'\n')
                        queue.put(link)

    print('stop crwaling')
    print(main_row)
    error_log.close()

def init():

    #queue init
    #main.queue.put("")
    #main.pool.spawn(getLink).join()

    #give worker pool
    print('start crwaling')
    #while not pool.free_count() == 15:
    while not queue.empty() :
        gevent.sleep(0.8)
        for x in range(0, min(queue.qsize(), pool.free_count())):
            pool.spawn(getData)

    #wait for everything complete
    pool.join()

