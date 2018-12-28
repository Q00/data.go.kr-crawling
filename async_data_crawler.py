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
excel_file_name=''

#init file name
file_name = sys.argv[0][:-3]

df_xml = None
def makeROW(item, name):
    
    global main_row
    global excel_file_name
    global df_xml
    try:
        
        print('makeROW')
        if excel_file_name != name:
            if excel_file_name:
                df_xml.to_csv(excel_file_name+'.csv',mode='w')
            excel_file_name = name
            print('here')
            dfcols = list(column.typeList[name].keys())
            print(item.find(api_column).text for api_column in dfcols)
            print(dfcols)
            #dataframe init
            df_xml = pd.DataFrame(columns=dfcols)
            print('here1')
            dx_xml = df_xml.append(
                    pd.Series([item.find(api_column).text for api_column in dfcols], index = dfcols),
                    ignore_index=True)
            
            print('here2')
        else:
            print('else1')
            print(item.find(api_column).text for api_column in dfcols)
            print(df_xml)
            dx_xml = df_xml.append(
                    pd.Series([item.find(api_column).text for api_column in dfcols], index = dfcols),
                    ignore_index=True)
            
    except:
        raise ValueError('FAIL MULTI PROCESSING') 
    main_row+=1

    
def getData():
    #가지고 있는 url만큼만 loop
    global error_count 
    error_log = open('./err.txt',mode='a')
    while not queue.empty():
        #저장되어있는 link를 queue에서 가져옴
        #pool의 worker들이 link로 request 동기보다 n배 빠름
            link = queue.get(timeout=0)
            if link[0] != "":
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
                        item_list = soup.find_all('item')
                        pool_excel.map([makeROW(item, link[1]) for item in item_list])
                        print('go row')
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

