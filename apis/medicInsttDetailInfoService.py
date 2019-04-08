#의료기관별 상세정보 서비스

#runtime중 메모리수정
import gevent.monkey
gevent.monkey.patch_all()
import requests
from lxml import etree
import gevent.pool
import gevent.queue
from bs4 import BeautifulSoup as BS
import ykiho
import sys
sys.path.insert(0, '../')
import async_data_crawler as main
import column
import time

start_time = time.time()


def getLink():
    baseUrl = 'http://apis.data.go.kr/B551182/medicInsttDetailInfoService/'
    urlList = 'getFacilityInfo', 'getDetailInfo', 'getMdlrtSbjectInfoList', 'getTransportInfoList', 'getMedicalEquipmentInfoList', 'getCgffdAddiInfoList', 'getNursigGradeInfoList', 'getSpclMdlrtInfoList', 'getSpcHospAppnFieldList',
    ykihoLIst = ykiho.ykihoList
    for ykiho_for in ykihoLIst :
        for addUrl in urlList:
            # if addUrl == 'finish':
            #    flist = []
            #    flist.append('finish')
            #    main.queue.put(flist)
            #    break
            # key는 config.py 있는 변수, async_data_crwaler에서 가져옴, key와 numofrows는 필수

            params = {'servicekey': main.key,'ykiho' : ykiho_for, 'numOfRows': 1}
            print(addUrl + '\n\n')

            # if addUrl != 'getDurPrdlstInfoList':
            #     params.update({'typeName': column.typeName[addUrl]})

            # Dictionary data -> url get string으로 바꿔줌
            params_str = "&".join("%s=%s" % (k, v) for k, v in params.items())

            requestUrl = baseUrl + addUrl
            print('requestUrl' + requestUrl)
            while True:
                try:
                    # request data
                    getdata = requests.get(requestUrl, params=params_str)
                    print('getdata----')
                except:
                    print('request error or no conection')
                    pass
                else:
                    print('breakkkkkkkkkk')
                    break
            try:
                # response data xml 로 파싱
                soup = BS(getdata.text, 'lxml-xml')

                # print(soup.prettify)
                # check page
                try:
                    # totalcount 파악
                    totalcount = int(soup.find('totalCount').text)
                except:
                    print('검색결과없음')
                    totalcount = 0
                print(ykiho_for)
                print( time.gmtime())
                print('총 개수: ', totalcount)

                if totalcount != 0:
                    page = int(totalcount / 5000) + 1
                    flist = []
                    flist.append(addUrl)

                    furl = []
                    for i in range(page):
                        params_str2 = params_str
                        # request 파라미터에 pageno 추가
                        params_str2 += '&pageNo=' + str(i + 1)

                        furl.append(requestUrl + '?' + params_str2)
                    flist.append(furl)
                    # ('flist를 뽑아보겠어요~~~~~~~~~~~', flist)
                    # queue 에 저장
                    main.queue.put(flist)
            except:
                print('crwaling error : ', sys.exc_info()[1])
print("--- %s seconds ---" % (time.time() - start_time))


# queue init
if __name__ == "__main__":
    main.pool.spawn(getLink).join()

    main.init()
