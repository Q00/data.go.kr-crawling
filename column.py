typeName = {
        'getDurPrdlstInfoList' : 'DUR품목정보', 
        'getSeobangjeongPartitnAtentInfoList' : '분할주의',
        'getEfcyDplctInfoList' : '효능군중복',
        'getOdsnAtentInfoList' : '노인주의',
        'getMdctnPdAtentInfoList' : '투여기간주의',
        'getCpctyAtentInfoList' : '용량주의',
        'getPwnmTabooInfoList' : '임부금기',
        'getSpcifyAgrdeTabooInfoList' : '특정연령대금기',
        'getUsjntTabooInfoList' : '병용금기'}

typeName_reverse = dict(zip(typeName.values(),typeName.keys()))

baseUrl = 'http://apis.data.go.kr/1470000/DURPrdlstInfoService/'
urlList = 'getDurPrdlstInfoList','getSeobangjeongPartitnAtentInfoList','getEfcyDplctInfoList','getOdsnAtentInfoList','getMdctnPdAtentInfoList','getCpctyAtentInfoList','getPwnmTabooInfoList','getSpcifyAgrdeTabooInfoList','getUsjntTabooInfoList'


#엑셀 헤드 인덱스 크롤링할때 쓰는데이터
paramData = {"publicDataDetailPk":"uddi:fa2ebf2c-6453-4f9d-bd89-ef8e3c77e19f","paramtrSe":"2","oprtinSeqNo":16752}
