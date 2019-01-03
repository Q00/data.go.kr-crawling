#runtime중 메모리수정
import gevent.monkey
gevent.monkey.patch_all()
try:
    from gevent.coros import BoundedSemaphore
except:
    from gevent.lock import BoundedSemaphore 
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
pool_conn = gevent.pool.Pool(15)
queue = gevent.queue.Queue()
sem = BoundedSemaphore(1)
#api key loading
key = config.go_data_api_key
error_count =0

#csv list
excel_file_name=''
result_list= None

def multi_wrapper(args):
    return make_row(*args)

def make_row(item, name):
    global queue 
    global excel_file_name
    try:
        #csv index
        dfcols_eng = list(column.typeList[name].keys())
        dfcols = list(column.typeList[name].values())
        
        row_df_xml = pd.DataFrame([[item[0].find(api_column).text for api_column in dfcols_eng]],columns=dfcols)
        
        for idx,sitem in enumerate(item):
            if idx ==1 :
                continue
            add_df = pd.DataFrame([[sitem.find(api_column).text for api_column in dfcols_eng]],columns=dfcols)

            row_df_xml = pd.concat([row_df_xml,add_df], sort=False)
            
        return row_df_xml
            
            
    except Exception as e:
        print(e)
        raise ValueError('FAIL MULTI PROCESSING') 

def connect_api(seperate):
    global error_count 
    error_log = open('./err.txt',mode='a')
    getdata = requests.get(seperate)
    soup = BS(getdata.text,'lxml-xml') 
    okflag = soup.find('resultCode')
    try:
        if okflag.text != '00':
            print("okflag: ",okflag.text)
            
            raise ValueError('okcode is not 00')    
        else:
            item_list = soup.find_all('item')

    except Exception as e:
        error_log.write(link[0]+'\n')
        error_log.write('==================================\n')
        error_count+=1
        error_log.write(str(error_count)+'\n')
        print("request throw error :", e)
        queue.put(link)
    print('total error ', error_count)
    error_log.close()
    return item_list

def getData():
    #가지고 있는 url만큼만 loop
    global excel_file_name
    global result_list
    #저장되어있는 link를 queue에서 가져옴
    #pool의 worker들이 link로 request 동기보다 n배 빠름
    link = queue.get(timeout=0)
    item_list = pool_conn.map(connect_api,link[1])
    sem.acquire() 
    if excel_file_name != link[0]:
        print('엑셀파일 네임 :',excel_file_name)
        print('link   ',link[0])
        if excel_file_name:
            print('create csv=========================================================================')
            if result_list is not None:
                df_total = result_list 
                df_total.to_csv('csv/'+column.typeName[excel_file_name]+'.csv',mode='a',encoding='ms949', index=False)
                result_list = None
            print('finish=============================================================================')
            excel_file_name = link[0]
        else:
            excel_file_name = link[0]
    datas = pool_excel.map(multi_wrapper,[(item, link[0]) for item in item_list])
    #data return 
    for data in datas:
        if result_list is not None:
            result_list = pd.concat([result_list, data],sort=False)
        else:
            result_list = data
    sem.release()
    print(len(result_list))
        

    print('stop crwaling')
    print('total error ', error_count)

def init():

    #give worker pool
    print('start crwaling')
    while not queue.empty() :
        gevent.sleep(0.5)
        for x in range(0, min(queue.qsize(), pool.free_count())):
            print('worker is going to work qsize ', queue.qsize())
            pool.spawn(getData)
    #wait for everything complete
    pool.join()

