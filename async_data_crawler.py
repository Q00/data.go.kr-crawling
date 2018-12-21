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
import importlib
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

#csv list
csv_list= []

#init file name
file_name = sys.argv[0][:-3]

def makeCSV(args):
    print(args)
    global main_row
    main_row+=1
    head_list=[]
    #if main_row == 1:
    #    head_list.append(add (v) for k,v in column.typeList[file_name].items)
    #    print(head_list)
    #    print('here makeCSV')


def getData():
    print('getdata')
    #가지고 있는 url만큼만 loop
    global error_count 
    error_log = open('./err.txt',mode='a')
    while not queue.empty():
            #저장되어있는 link를 queue에서 가져옴
            #pool의 worker들이 link로 request 동기보다 n배 빠름
                link = queue.get(timeout=0)
                if link[0] != "":
                    gevent.sleep(0.3)
                    getdata = requests.get(link[0])
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
                            args= []
                            
                            args.append(soup.find_all('item'))
                            args.append(link[1])
                            pool_excel.map(makeCSV,args)
                    
                    except:
                        error_log.write(link[0]+'\n')
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
        gevent.sleep(0.5)
        for x in range(0, min(queue.qsize(), pool.free_count())):
            pool.spawn(getData)

    #wait for everything complete
    pool.join()

