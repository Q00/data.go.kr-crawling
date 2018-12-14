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
#baseUrl = 'http://apis.data.go.kr/1470000/DURPrdlstInfoService/'
#baseUrl = 'http://apis.data.go.kr/1470000/DURPrdlstInfoService/'
#baseUrl = 'http://apis.data.go.kr/1470000/DURPrdlstInfoService/'
#baseUrl = 'http://apis.data.go.kr/1470000/DURPrdlstInfoService/'
#baseUrl = 'http://apis.data.go.kr/1470000/DURPrdlstInfoService/'
#baseUrl = 'http://apis.data.go.kr/1470000/DURPrdlstInfoService/'
urlList = 'getDurPrdlstInfoList','getSeobangjeongPartitnAtentInfoList','getEfcyDplctInfoList','getOdsnAtentInfoList','getMdctnPdAtentInfoList','getCpctyAtentInfoList','getPwnmTabooInfoList','getSpcifyAgrdeTabooInfoList','getUsjntTabooInfoList'
