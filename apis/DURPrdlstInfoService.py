#runtime중 메모리수정
import gevent.monkey
gevent.monkey.patch_all()
import requests
from lxml import etree
import gevent.pool
import gevent.queue
from bs4 import BeautifulSoup as BS
import sys
sys.path.insert(0,'../')
import async_data_crawler as main
import column

def getLink():
    print('getlink') 
    
    baseUrl = 'http://apis.data.go.kr/1470000/DURPrdlstInfoService/'
    urlList = 'getDurPrdlstInfoList','getSeobangjeongPartitnAtentInfoList','getEfcyDplctInfoList','getOdsnAtentInfoList','getMdctnPdAtentInfoList','getCpctyAtentInfoList','getPwnmTabooInfoList','getSpcifyAgrdeTabooInfoList','getUsjntTabooInfoList'


    for addUrl in urlList:
        for letter in range(ord('a'), ord('z')+1):
            #key는 config.py 있는 변수, async_data_crwaler에서 가져옴, key와 numofrows는 필수
            params = {'itemname': chr(letter), 'servicekey': main.key, 'numOfRows':100}
            if addUrl != 'getdurprdlstinfolist':
                params.update({'typename' : column.typeName[addUrl]}) 
            #Dictionary data -> url get string으로 바꿔줌
            params_str = "&".join("%s=%s" % (k,v) for k,v in params.items()) 
            requestUrl = baseUrl + addUrl
            #print(requesturl)
            try:
                #request data
                print('데이터 가져오는중 검색한 알파벳 :', chr(letter))
                getdata = requests.get(requestUrl, params=params_str)
            except:
                print('request error')
            try:
                #response data xml 로 파싱
                soup = BS(getdata.text, 'lxml-xml') 
            
                #print(soup.prettify) 
                #check page
                try:
                    #totalcount 파악
                    totalcount = int(soup.find('totalCount').text)
                except:
                    print('검색결과없음')
                    totalcount=0
                #print('총 개수: ',totalcount)
                if totalcount!=0:
                    #page 계산
                    page = int(totalcount/100) + 1
                    #page 별로 루프
                    for i in range(page):
                        params_str2 = params_str
                        #request 파라미터에 pageno 추가
                        params_str2+= '&pageno='+str(i+1)
                        
                        flist = []
                        furl = requestUrl+'?'+params_str2
                        flist.append(furl)
                        flist.append(addUrl)
                        #queue 에 저장
                        main.queue.put(flist)
     
            except:
                print('crwaling error : ',sys.exc_info()[1])
            break
        break

#queue init
if __name__ == "__main__":
    main.pool.spawn(getLink).join()

    main.init()
