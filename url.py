import gevent.monkey
gevent.monkey.patch_all()
import base64
import requests
from bs4 import BeautifulSoup as BS
import json

def main():
    string = 'https://www.data.go.kr/pubn/lab/gui/IrosDevGuide/selectReqResPrmList.do'
    #inputString = input('추가할 url : ')
    with open('url.txt','a') as ufile:
        ufile.write(string+'\n')
    getData(string)

def getData(inputString):
    #param data oprtinSeqNo 와 dur 유형 매칭 필요
    paramData = {"publicDataDetailPk":"uddi:fa2ebf2c-6453-4f9d-bd89-ef8e3c77e19f","paramtrSe":"2","oprtinSeqNo":16752}
    headers = {'Accept':'application/json, text/plain, */*'}
    getdata = requests.post(inputString,headers=headers, data=json.dumps(paramData))
    json_data = json.loads(getdata.text) 
    for column in range(6,len(json_data['RESULT_RE_LIST']+1):
        with open('column_auto.py','a') as columnpy:
            columnpy.write(json_data['RESULT_RE_LIST'])

 
    print(getdata.text)

main()

#txt = base64.b64decode(string) 
#txt.decode()
#print(txt)
