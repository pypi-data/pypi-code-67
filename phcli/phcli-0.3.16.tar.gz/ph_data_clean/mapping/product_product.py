def mapping():
    return [
        {
            "col_name": "COMPANY",
            "col_desc": "数据公司",
            "candidate": [],
            "type": "String",
            "not_null": False,
        },
        {
            "col_name": "SOURCE",
            "col_desc": "数据来源",
            "candidate": [],
            "type": "String",
            "not_null": False,
        },
        {
            "col_name": "TAG",
            "col_desc": "文件标识",
            "candidate": ['_TAG', '_Tag'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "PACK_ID",
            "col_desc": "产品的唯一标识符",
            "candidate": ['PACK_ID'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "MOLE_NAME_EN",
            "col_desc": "英文分子名",
            "candidate": ['MOLE_NAME_EN'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "MOLE_NAME_CH",
            "col_desc": "中文分子名",
            "candidate": ['MOLE_NAME_CH'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "PROD_DESC",
            "col_desc": "产品描述",
            "candidate": ['PROD_DESC'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "PROD_NAME_CH",
            "col_desc": "中文产品名",
            "candidate": ['PROD_NAME_CH'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "CORP_NAME_EN",
            "col_desc": "英文公司名",
            "candidate": ['CORP_NAME_EN'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "CORP_NAME_CH",
            "col_desc": "中文公司名",
            "candidate": ['CORP_NAME_CH'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "MNF_NAME_EN",
            "col_desc": "英文厂家名",
            "candidate": ["MNF_NAME_EN"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "MNF_NAME_CH",
            "col_desc": "中文厂家名",
            "candidate": ['MNF_NAME_CH'],
            "type": "Integer",
            "not_null": True,
        },
        {
            "col_name": "PCK_DESC",
            "col_desc": "包装和规格",
            "candidate": ['PCK_DESC'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "DOSAGE",
            "col_desc": "剂型",
            "candidate": ['DOSAGE'],
            "type": "Integer",
            "not_null": True,
        },
        {
            "col_name": "SPEC",
            "col_desc": "规格",
            "candidate": ["SPEC"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "PACK",
            "col_desc": "包装",
            "candidate": ['PACK'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "NFC1",
            "col_desc": "给药途径一级分类",
            "candidate": ["NFC1"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "NFC1_NAME",
            "col_desc": "给药途径一级分类",
            "candidate": ['NFC1_NAME'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "NFC1_NAME_CH",
            "col_desc": "给药途径一级分类",
            "candidate": ['NFC1_NAME_CH'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "NFC12",
            "col_desc": "给药途径二级分类",
            "candidate": ['NFC12'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "NFC12_NAME",
            "col_desc": "给药途径二级分类",
            "candidate": ['NFC12_NAME'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "NFC12_NAME_CH",
            "col_desc": "给药途径二级分类",
            "candidate": ['NFC12_NAME_CH'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "NFC123",
            "col_desc": "给药途径三级分类",
            "candidate": ['NFC123'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "NFC123_NAME",
            "col_desc": "给药途径三级分类",
            "candidate": ['NFC123_NAME'],
            "type": "Double",
            "not_null": True,
        },
        {
            "col_name": "CORP_ID",
            "col_desc": "公司名ID",
            "candidate": ["CORP_ID"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "MNF_TYPE",
            "col_desc": "生产厂商类型",
            "candidate": ["MNF_TYPE"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "MNF_TYPE_NAME",
            "col_desc": "生产厂商类型名",
            "candidate": ['MNF_TYPE_NAME'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "MNF_TYPE_NAME_CH",
            "col_desc": "中文生产厂商类型名",
            "candidate": ['MNF_TYPE_NAME_CH'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "MNF_ID",
            "col_desc": "生产厂商ID",
            "candidate": ['MNF_ID'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "ATC1_CODE",
            "col_desc": "药品一级分类",
            "candidate": ["ATC1_CODE"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "ATC1_DESC",
            "col_desc": "药品一级分类",
            "candidate": ["ATC1_DESC"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "ATC2_CODE",
            "col_desc": "药品二级分类",
            "candidate": ["ATC2_CODE"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "ATC2_DESC",
            "col_desc": "药品二级分类",
            "candidate": ["ATC2_DESC"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "ATC3_CODE",
            "col_desc": "药品三级分类",
            "candidate": ["ATC3_CODE"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "ATC3_DESC",
            "col_desc": "药品三级分类",
            "candidate": ["ATC3_DESC"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "ATC4_CODE",
            "col_desc": "药品四级分类",
            "candidate": ["ATC4_CODE"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "ATC4_DESC",
            "col_desc": "药品四级分类",
            "candidate": ["ATC4_DESC"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "ATC1",
            "col_desc": "药品一级分类",
            "candidate": ["ATC1"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "ATC2",
            "col_desc": "药品二级分类",
            "candidate": ["ATC2"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "ATC3",
            "col_desc": "药品三级分类",
            "candidate": ["ATC3"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "ATC4",
            "col_desc": "药品四级分类",
            "candidate": ["ATC4"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "REMARK",
            "col_desc": "更新标识",
            "candidate": ["REMARK"],
            "type": "String",
            "not_null": False,
        },
    ]
