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

typeList= {
    "getEfcyDplctInfoList":{
      "DUR_SEQ": "DUR\uc77c\ub828\ubc88\ud638",
      "EFFECT_NAME": "\ud6a8\ub2a5",
      "INGR_CODE": "DUR\uc131\ubd84\ucf54\ub4dc",
      "INGR_NAME": "\uc131\ubd84\uba85",
      "INGR_ENG_NAME": "DUR\uc131\ubd84(\uc601\ubb38)",
      "FORM_CODE_NAME": "\uc81c\ud615\uad6c\ubd84",
      "MIX": "\ub2e8\uc77c/\ubcf5\ud569",
      "MIX_INGR": "\ubcf5\ud569\uc81c",
      "ITEM_SEQ": "\ud488\ubaa9\uae30\uc900\ucf54\ub4dc",
      "ITEM_NAME": "\ud488\ubaa9\uba85",
      "ITEM_PERMIT_DATE": "\ud488\ubaa9\ud5c8\uac00\uc77c\uc790",
      "CHART": "\uc131\uc0c1",
      "ENTP_NAME": "\uc5c5\uccb4\uba85",
      "FORM_CODE": "\uc81c\ud615\uad6c\ubd84\ucf54\ub4dc",
      "FORM_NAME": "\uc81c\ud615",
      "ETC_OTC_CODE": "\uc804\ubb38\uc77c\ubc18 \uad6c\ubd84\ucf54\ub4dc",
      "ETC_OTC_NAME": "\uc804\ubb38/\uc77c\ubc18",
      "CLASS_CODE": "\uc57d\ud6a8\ubd84\ub958\ucf54\ub4dc",
      "CLASS_NAME": "\uc57d\ud6a8\ubd84\ub958",
      "MAIN_INGR": "\uc8fc\uc131\ubd84",
      "NOTIFICATION_DATE": "\uace0\uc2dc\uc77c\uc790",
      "PROHBT_CONTENT": "\uae08\uae30\ub0b4\uc6a9",
      "REMARK": "\ube44\uace0",
      "INGR_ENG_NAME_FULL": "DUR\uc131\ubd84\uc0c1\uc138\uba85",
      "CHANGE_DATE": "\ubcc0\uacbd\uc77c\uc790"
    },
    "getMajorCmpnNmCdList": {
        'divNm': '분류명',
        'fomnTpCdNm': '제형구분명',
        'gnlNm': '일반명',
        'gnlNmCd': '일반명코드',
        'injcPthCdNm': '투여경로명',
        'iqtyTxt': '함량내용',
        'meftDivNo': '약효분류번호',
        'unit': '단위'
        },
    "getHtfsInfoList":{
        "PRDLST_NM": "\uc81c\ud488\uba85",
        "PRMS_DT": "\ub4f1\ub85d\uc77c\uc790",
        "DISPOS": "\uc131\uc0c1",
        "NTK_MTHD": "\uc12d\ucde8\ub7c9/\uc12d\ucde8\ubc29\ubc95",
        "CSTDY_MTHD": "\ubcf4\uc874 \ubc0f \uc720\ud1b5\uae30\uc900",
        "IFTKN_ATNT_MATR_CN": "\uc12d\ucde8\uc2dc \uc8fc\uc758\uc0ac\ud56d",
        "PRIMARY_FNCLTY": "\uae30\ub2a5\uc131 \ub0b4\uc6a9",
        "STDR_STND": "\uae30\uc900\ubc0f\uaddc\uaca9",
        "BSSH_NM": "\uc218\uc785\uc5c5\uccb4",
        "GU_PRDLST_MNF_MANAGE_NO": "\ud488\ubaa9\uc81c\uc870\uad00\ub9ac\ubc88\ud638"
        }
}
print(typeList)
