#건강기능식품 대상별 정보DB 서비스
#24925개
##runtime중 메모리수정
import pdb

import gevent.monkey
gevent.monkey.patch_all()
import requests
from lxml import etree
import gevent.pool
import gevent.queue
from bs4 import BeautifulSoup as BS
import sys
sys.path.insert(0, '../')
import async_data_crawler as main
import column


def getLink():
    baseUrl = 'http://apis.data.go.kr/1470000/HtfsTrgetInfoService/'
    urlList = 'getHtfsInfoList',

    for addUrl in urlList:
        # if addUrl == 'finish':
        #    flist = []
        #    flist.append('finish')
        #    main.queue.put(flist)
        #    break
        # key는 config.py 있는 변수, async_data_crwaler에서 가져옴, key와 numofrows는 필수
        # 필수 요청 메세지로 prdlst_nm 넣어줌( ' '(빈칸), '0' ~ '3000' 까지 존재)
        params = {'servicekey': main.key,'prdlst_nm':"", 'numOfRows': 100}

        # if addUrl != 'getDurPrdlstInfoList':
        #     params.update({'typeName': column.typeName[addUrl]})

        # Dictionary data -> url get string으로 바꿔줌
        params_str = "&".join("%s=%s" % (k, v) for k, v in params.items())




        requestUrl = baseUrl + addUrl

        print("뽑아보자~~~ params params_str requestUrl")


        # prdlst_nm = ' ',
        # for prdlst in range(0, 3000):
        #     params_str1 = params_str
        #     params_str1 += '&prdlst_nm=' + str(prdlst)
        #
        #     flist = []
        #     flist.append(addUrl)

        # request 파라미터에
        #리퀘하는 try문
        try:
            # request data
            getdata = requests.get(requestUrl, params=params_str)
        except:
            print('request error')

        #리퀘 받은거 lxml-xml로 파싱하는 try문
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
            print('총 개수: ', totalcount)

            #
            if totalcount != 0:
                page = int(totalcount / 100) + 1

                flist = []
                flist.append(addUrl)

                furl = []
                for i in range(page):
                    params_str2 = params_str
                    # request 파라미터에 pageno 추가
                    params_str2 += '&pageNo=' + str(i + 1)

                    furl.append(requestUrl + '?' + params_str2)
                flist.append(furl)
                print('flist를 뽑아보겠어요~~~~~~~~~~~')

                # queue 에 저장
                main.queue.put(flist)
        except:
            print('crwaling error : ', sys.exc_info()[1])


# queue init
if __name__ == "__main__":
    print("여기서 에러가 날까요? 메인 밑이야")
    main.pool.spawn(getLink).join()
    main.init()
