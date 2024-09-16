#-*- coding: utf-8 -*-
import requests
import os
import certifi
from bs4 import BeautifulSoup

# Function to search for a word in the HTML content
def search_word_in_html(content, word):
    soup = BeautifulSoup(content, 'html.parser')
    text = soup.get_text()
    if word in text:
        print(f"Word '{word}' found in the HTML content.")
    else:
        print(f"Word '{word}' not found in the HTML content.")



os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

session = requests.Session()

# URL for the login endpoint
login_url = "https://www.seoul.go.kr/member/userlogin/login.do"

id = 'bona405'
pw = 'jong8576!@'


headers_0 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7,vi;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://yeyak.seoul.go.kr',
    'Referer': 'https://yeyak.seoul.go.kr/',
    'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}
payload_0 = {
    'div': 'mem',
    'SITE_GB': 'GB009',
    'refresh_url': 'https://yeyak.seoul.go.kr/web/loginEnd.do?ru=aHR0cHM6Ly95ZXlhay5zZW91bC5nby5rci93ZWIvbWFpbi5kbw==',
    'isExternal': 'Y',
    'userid': id,
    'userpwd': pw
}


response = session.post(url=login_url, data=payload_0)

search_word = '로그아웃'  
if response.status_code == 200:
    print("Login successful")
    soup = BeautifulSoup(response.content, 'html.parser')
    # print(soup.prettify())
    search_word_in_html(response.content, search_word)

cookies = session.cookies
# print(session.cookies.get_dict())


payload_insertform = {
    "file_id": "",
    "sysToday": "20240906",
    "rsv_svc_id": "S210216140014448077",
    "grp_code": "",
    "resve_unit_seq": "",
    "resve_unit_seq2": "",
    "use_time_unit_code": "B402",
    "tme_ty_code": "TM02",
    "wait_posbl_co": 0,
    "use_stdr_rcept_daycnt": 14,
    "use_stdr_rcept_time": 14,
    "rsvde_stdr_rcept_daycnt": 1,
    "rsvde_stdr_rcept_time": 23,
    "sltYear": 2024,
    "sltMonth": 9,
    "sltDay": 7,
    "yyyymm": "202409",
    "yyyy": 2024,
    "mm": 9,
    "dd": 7,
    "useYear": "",
    "useMonth": "",
    "useDay": "",
    "useDe": "20240916",
    "calCheck": "N",
    "unitCheck": "N",
    "count": 0,
    "rsv_counts": "",
    "rsv_counte": "",
    "reqst_resve_unit_value": 1,
    "mumm_use_posbl_time": 1,
    "mxmm_use_posbl_time": 2,
    "mode": "",
    "act": "",
    "type": 2,
    "cal_before": "N",
    "cal_next": "Y",
    "mgis_cdata": [127.08817787505, 37.495187838167],
    "mgis_buffer": "",
    "x": 127.08817787505,
    "y": 37.495187838167,
    "register_no": 1500788,
    "reqst_rcept_ntcn_yn": "",
    "reqst_clos_ntcn_yn": "",
    "notice_ntcn_yn": "",
    "type2": "",
    "MMBNO": 1633788,
    "logincheck": "Y",
    "score": "",
    "satisfyScore": 0,
    "reSvc": "Y",
    "form_txt": ""
}

response = session.post(url="https://yeyak.seoul.go.kr/web/reservation/insertFormReserve.do", data=payload_insertform, verify=False)
search_word = id  
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    search_word_in_html(response.content, search_word)


headers_1 = {
    # 'Accept': 'application/json, text/javascript, */*; q=0.01',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    # 'Accept-Language': 'en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7,vi;q=0.6',
    # 'Ajax': 'true',
    # 'Connection': 'keep-alive',
    # 'Content-Length': '69',  # Note: This should be calculated dynamically based on the payload
    # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': '; '.join([f'{cookie.name}={cookie.value}' for cookie in cookies]),
    'Host': 'yeyak.seoul.go.kr',
    'Origin': 'https://yeyak.seoul.go.kr',
    'Referer': 'https://yeyak.seoul.go.kr/web/reservation/insertFormReserve.do',
    # 'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    # 'Sec-Ch-Ua-Mobile': '?0',
    # 'Sec-Ch-Ua-Platform': '"Windows"',
    # 'Sec-Fetch-Dest': 'empty',
    # 'Sec-Fetch-Mode': 'cors',
    # 'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

payload_1 = {
    'rsv_svc_id': 'S210216135442800789',
    'resve_unit_seq': '67083281',
    'useDe': '20240710'
}


headers_rev = {
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    # "Accept-Encoding": "gzip, deflate, br, zstd",
    # "Accept-Language": "en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7,vi;q=0.6",
    # "Cache-Control": "max-age=0",
    # "Connection": "keep-alive",
    # "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryA7vNAhflgQOX9AvF", 
    # "Cookie": "WL_PCID=17053013308371732494854; WMONID=gCtpGOX8-X1; _ga=GA1.3.1400749289.1705301331; _ga_13TFLYF8E5=GS1.1.1719578229.2.1.1719578242.47.0.2123175698; GONGYEYAK=664C4A5A528F4B896436930466BA5416; MEM001_NM2=; TV_PAUSE_YN=N; ADD_PRVC_CLCT_AGRE_YN=Y; MEM_NM2=%EB%85%B8%EC%A2%85%ED%98%84; MEM_DIV=; USER_NM=; USER_NAME=; PW_CHECK_YN=; WL_PCID_DATA=%7B%22pcid%22%3A%2217053013308371732494854%22%2C%22recom_list%22%3A%5B%7B%22SERVICE_NAME%22%3A%22%EC%A7%80%EB%B0%A9%EC%84%B8%EB%82%A9%EB%B6%80%22%2C%22SERVICE_URL%22%3A%22https%3A%2F%2Fetax.seoul.go.kr%22%2C%22REG_DATE%22%3A1594859192000%2C%22RECOM_IDX%22%3A241%2C%22RANK%22%3A1%2C%22FLAG%22%3A1%7D%2C%7B%22SERVICE_NAME%22%3A%22%EB%B2%95%EB%AC%B4%ED%96%89%EC%A0%95(%EC%9E%90%EC%B9%98%EB%B2%95%EA%B7%9C)%22%2C%22SERVICE_URL%22%3A%22https%3A%2F%2Flegal.seoul.go.kr%2F%22%2C%22REG_DATE%22%3A1671613507000%2C%22RECOM_IDX%22%3A383%2C%22RANK%22%3A2%2C%22FLAG%22%3A1%7D%2C%7B%22SERVICE_NAME%22%3A%22%EC%84%9C%EC%9A%B8%EC%95%88%EC%A0%84%EB%88%84%EB%A6%AC%22%2C%22SERVICE_URL%22%3A%22https%3A%2F%2Fsafecity.seoul.go.kr%2F%22%2C%22REG_DATE%22%3A1710913538000%2C%22RECOM_IDX%22%3A402%2C%22RANK%22%3A3%2C%22FLAG%22%3A1%7D%2C%7B%22SERVICE_NAME%22%3A%22%EA%B3%B5%EA%B3%B5%EC%84%9C%EB%B9%84%EC%8A%A4%EC%98%88%EC%95%BD%22%2C%22SERVICE_URL%22%3A%22https%3A%2F%2Fyeyak.seoul.go.kr%22%2C%22REG_DATE%22%3A1725548400000%2C%22RECOM_IDX%22%3A0%2C%22RANK%22%3A1%2C%22PCID%22%3A%2217053013308371732494854%22%2C%22FLAG%22%3A3%7D%2C%7B%22SERVICE_NAME%22%3A%22%ED%8F%89%EC%83%9D%ED%95%99%EC%8A%B5%ED%8F%AC%ED%84%B8%22%2C%22SERVICE_URL%22%3A%22https%3A%2F%2Fsll.seoul.go.kr%22%2C%22REG_DATE%22%3A1725548400000%2C%22RECOM_IDX%22%3A0%2C%22RANK%22%3A2%2C%22PCID%22%3A%2217053013308371732494854%22%2C%22FLAG%22%3A3%7D%2C%7B%22SERVICE_NAME%22%3A%22%EC%9D%B8%EC%9E%AC%EA%B0%9C%EB%B0%9C%EC%9B%90%22%2C%22SERVICE_URL%22%3A%22https%3A%2F%2Fhrd.seoul.go.kr%22%2C%22REG_DATE%22%3A1725548400000%2C%22RECOM_IDX%22%3A0%2C%22RANK%22%3A3%2C%22PCID%22%3A%2217053013308371732494854%22%2C%22FLAG%22%3A3%7D%2C%7B%22SERVICE_NAME%22%3A%22%EC%B2%AD%EB%85%84%EB%AA%BD%EB%95%85%EC%A0%95%EB%B3%B4%ED%86%B5%22%2C%22SERVICE_URL%22%3A%22https%3A%2F%2Fyouth.seoul.go.kr%22%2C%22REG_DATE%22%3A1725548400000%2C%22RECOM_IDX%22%3A0%2C%22RANK%22%3A5%2C%22PCID%22%3A%2217053013308371732494854%22%2C%22FLAG%22%3A3%7D%2C%7B%22SERVICE_NAME%22%3A%22%EB%82%B4%EC%86%90%EC%95%88%EC%97%90%EC%84%9C%EC%9A%B8%22%2C%22SERVICE_URL%22%3A%22https%3A%2F%2Fmediahub.seoul.go.kr%22%2C%22REG_DATE%22%3A1725548400000%2C%22RECOM_IDX%22%3A0%2C%22RANK%22%3A6%2C%22PCID%22%3A%2217053013308371732494854%22%2C%22FLAG%22%3A3%7D%2C%7B%22SERVICE_NAME%22%3A%22%EC%84%9C%EC%9A%B8%EC%9D%BC%EC%9E%90%EB%A6%AC%ED%8F%AC%ED%84%B8%22%2C%22SERVICE_URL%22%3A%22https%3A%2F%2Fjob.seoul.go.kr%22%2C%22REG_DATE%22%3A1725548400000%2C%22RECOM_IDX%22%3A0%2C%22RANK%22%3A7%2C%22PCID%22%3A%2217053013308371732494854%22%2C%22FLAG%22%3A3%7D%2C%7B%22SERVICE_NAME%22%3A%22%EC%84%9C%EC%9A%B8%EB%B6%80%EB%8F%99%EC%82%B0%EC%A0%95%EB%B3%B4%EA%B4%91%EC%9E%A5%22%2C%22SERVICE_URL%22%3A%22http%3A%2F%2Fland.seoul.go.kr%22%2C%22REG_DATE%22%3A1725548400000%2C%22RECOM_IDX%22%3A0%2C%22RANK%22%3A10%2C%22PCID%22%3A%2217053013308371732494854%22%2C%22FLAG%22%3A3%7D%5D%7D; JSESSIONID=ih0bNnoj1fdtv6rx3DBuoFIXAIhSaiBnM4Og1rWxta4fEZ1lzOErXxSkQa1yIgRY.amV1c19kb21haW4vbWVtYmVyMTA2; temp_addr=20240906061530_136430466; MEM001_PK=2024051701203; MEM001_ID=133a4d320e3651912dee824b028fdd71c6a2165f26ae36; MEM001_NM=b3eacd72fe669121ed8e420b82df7dc1ab135e2bac31; REALNAME_YN=Y; PWD_CHANGE_YN=Y; PAUSE_YN=N; memUserId=bona405; MEM_NM=%EB%85%B8%EC%A2%85%ED%98%84; MEM_ID=bona405; SEOUL_EMAIL_DELYN=Y; MAYOR_ID=%23A05960055; _SSO_Global_Logout_url=get%5Ehttps%3A%2F%2Fwww.seoul.go.kr%2Fmember%2Fuserlogin%2FlogOut.do%24; sipreset_S210216140014448077=N",
    "Host": "yeyak.seoul.go.kr",
    "Origin": "https://yeyak.seoul.go.kr",
    "Referer": "https://yeyak.seoul.go.kr/web/reservation/insertFormReserve.do"
    # "Sec-CH-UA": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    # "Sec-CH-UA-Mobile": "?0",
    # "Sec-CH-UA-Platform": '"Windows"',
    # "Sec-Fetch-Dest": "document",
    # "Sec-Fetch-Mode": "navigate",
    # "Sec-Fetch-Site": "same-origin",
    # "Sec-Fetch-User": "?1",
    # "Upgrade-Insecure-Requests": "1",
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}


payload_rev = {
    'req_time': '1',
    'use_time_unit_code': 'B402',
    'tme_ty_code': 'TM02',
    'wait_posbl_co': '0',
    'use_stdr_rcept_daycnt': '14',
    'use_stdr_rcept_time': '14',
    'rsvde_stdr_rcept_daycnt': '1',
    'rsvde_stdr_rcept_time': '23',
    'rsv_svc_id': 'S210216135442800789',
    'mt_fdrm_resve_yn': '',
    'chrge_setle_place_code': 'B201',
    'rcept_mth_code': '1',
    'rcept_mth': 'WEB',
    'sysToday': '20240628',
    'sltYear': '2024',
    'sltMonth': '06',
    'sltDay': '29',
    'yyyymm': '202407',
    'yyyy': '2024',
    'mm': '7',
    'dd': '29',
    'calCheck': 'Y',
    'unitCheck': 'Y',
    'count': '',
    'rsv_counts': '',
    'rsv_counte': '',
    'reqst_resve_unit_value': '1',
    'mumm_use_posbl_time': '1',
    'mxmm_use_posbl_time': '2',
    'mode': '',
    'act': '',
    'type': '',
    'cal_before': 'Y',
    'cal_next': 'Y',
    'gcaptcha_v3_sitekey': '6Ldm1-MUAAAAAEHda-gP_HEp_Mpe6tEEAH9pommT',
    'email1': 'bona405',
    'email2': 'gmail.com',
    'bot_cha_ver': 'V2',
    'chrge_seq': '',
    'pchrg_yn': '0',
    'store_id': '',
    'pg_code': '',
    'zone_use_yn': 'N',
    'zone_seq': '',
    'zoneCheck': 'N',
    'untact_area': '/',
    'untact_area_yn': '0',
    'dynm_resve_button_yn': '1',
    'author_group_seq': '12842',
    'cl_code': 'T106',
    'tlphonno1': '',
    'moblphone1': '01033874405',
    'reSvc': '',
    'mberphone': '01033874405',
    'mbertlphone': '',
    'mberemail1': 'bona405',
    'mberemail2': 'gmail.com',
    'chatbot_resve_yn': '',
    'tm_count': '',
    'totDcCnt': '0',
    'unit_group_code': 'RC02',
    'unit_code': 'RD02',
    'use_unit_code': 'RB01',
    'use_nmpr_lmtt_yn': '1',
    'sms_yn': 'Y',
    'email_yn': 'Y',
    'start_date': '',
    'end_date': '',
    'moblphon_essntl_yn': '1',
    'email_essntl_yn': '0',
    'ades_essntl_yn': '0',
    'date_count': '0',
    'night': '',
    'sc_yn': 'N',
    'click_count': '0',
    'start_use_hm': '',
    'add_item_yn': 'Y',
    'user_add_item_yn': 'N',
    'resve_unit_seq': '67083281',
    'useDe': '20240710',
    'tgt_seq': '167355',
    'tgt_cnt': '1',
    'QChk': '',
    'user_req_cnt': '10',
    'addItemTxt': '.',
    'additem': '222492',
    'mber_nm': '노종현',
    'indvdl_grp_se_code': 'B503',
    'grp_nm': '.',
    'form_name2': '노종현',
    'tlphonno2': '',
    'moblphone2': '01033874405',
    'form_email1': 'bona405',
    'form_email2': 'gmail.com',
    'g-recaptcha-response': '',
    'chk_agree1': 'on',
    'person': '1',
    'tot_bass_use_am': '0',
    'dc_amount': '0',
    'tot_amount': '0',
    'vkey': 'vkey'
}



# print(certifi.where())
# response = requests.get(url='https://yeyak.seoul.go.kr', verify=certifi.where())
# print(response.status_code)

payload_2 = {
    'rsv_svc_id': 'S210216140014448077',
    'date': '20240916',
    'author_group_seq': '12842',
    'cl_code': 'T106',
    'usede_stdr_rcept_time': '14'
}

payload_3 = {
    'date': '20240916',
    'rsv_svc_id': 'S210216140014448077'
}

payload_4 = {
    'rsv_svc_id': 'S210216140014448077',
    'resve_unit_seq': '67088725',
    'useDe': '20240916'
}

payload_5 = {
    'req_time':'1',
    'use_time_unit_code':'B402',
    'tme_ty_code':'TM02',
    'wait_posbl_co':'0',
    'use_stdr_rcept_daycnt':'14',
    'use_stdr_rcept_time':'14',
    'rsvde_stdr_rcept_daycnt':'1',
    'rsvde_stdr_rcept_time':'23',
    'rsv_svc_id':'S210216140014448077',
    'mt_fdrm_resve_yn':'',
    'chrge_setle_place_code':'B201',
    'rcept_mth_code':'1',
    'rcept_mth':'WEB',
    'sysToday':'20240906',
    'sltYear':'2024',
    'sltMonth':'09',
    'sltDay':'07',
    'yyyymm':'202409',
    'yyyy':'2024',
    'mm':'9',
    'dd':'07',
    'calCheck':'Y',
    'unitCheck':'Y',
    'count':'',
    'rsv_counts':'',
    'rsv_counte':'',
    'reqst_resve_unit_value':'1',
    'mumm_use_posbl_time':'1',
    'mxmm_use_posbl_time':'2',
    'mode':'',
    'act':'',
    'type':'',
    'cal_before':'N',
    'cal_next':'Y',
    'gcaptcha_v3_sitekey':'6Ldm1-MUAAAAAEHda-gP_HEp_Mpe6tEEAH9pommT',
    'email1':'bona405',
    'email2':'gmail.com',
    'bot_cha_ver':'V2',
    'chrge_seq':'',
    'pchrg_yn':'0',
    'store_id':'',
    'pg_code':'',
    'zone_use_yn':'',
    'zone_seq':'',
    'zoneCheck':'N',
    'untact_area':'/',
    'untact_area_yn':'0',
    'dynm_resve_button_yn':'1',
    'author_group_seq':'12842',
    'cl_code':'T106',
    'tlphonno1':'',
    'moblphone1':'01033874405',
    'reSvc':'Y',
    'mberphone':'01033874405',
    'mbertlphone':'',
    'mberemail1':'bona405',
    'mberemail2':'gmail.com',
    'chatbot_resve_yn':'',
    'tm_count':'',
    'totDcCnt':'0',
    'unit_group_code':'RC02',
    'unit_code':'RD02',
    'use_unit_code':'RB01',
    'use_nmpr_lmtt_yn':'1',
    'sms_yn':'Y',
    'email_yn':'Y',
    'start_date':'',
    'end_date':'',
    'moblphon_essntl_yn':'1',
    'email_essntl_yn':'0',
    'ades_essntl_yn':'0',
    'date_count':'0',
    'night':'',
    'sc_yn':'N',
    'click_count':'0',
    'start_use_hm':'',
    'add_item_yn':'Y',
    'user_add_item_yn':'N',
    'resve_unit_seq':'67088725',
    'useDe':'20240916',
    'tgt_seq':'167384',
    'tgt_cnt':'1',
    'QChk':'',
    'user_req_cnt':'10',
    'addItemTxt':'agree',
    'additem':'222493',
    'mber_nm':'노종현',
    'indvdl_grp_se_code':'B502',
    'grp_nm':'',
    'form_name2':'노종현',
    'tlphonno2':'',
    'moblphone2':'01033874405',
    'form_email1':'bona405',
    'form_email2':'gmail.com',
    'g-recaptcha-response':'',
    'person':'1',
    'tot_bass_use_am':'0',
    'dc_amount':'0',
    'tot_amount':'0',
    'vkey':'vkey'
}


response = session.post(url="https://yeyak.seoul.go.kr/web/reservation/selectAllTimeCheckAjax.do", data=payload_2, headers=headers_1, verify=False)
# print(response.text)

response = session.post(url="https://yeyak.seoul.go.kr/web/reservation/selectListReservCalUnitAjax.do", data=payload_2, headers=headers_1, verify=False)
# print(response.text)

response = session.post(url="https://yeyak.seoul.go.kr/web/reservation/selectListCancelFeeInfoAjax.do", data=payload_3, headers=headers_1, verify=False)
# print(response.text)

response = session.post(url="https://yeyak.seoul.go.kr/web/reservation/selectReservRsvCountLimitYnAjax.do", data=payload_4, headers=headers_1, verify=False)
print(response.text)


response = session.post(url="https://yeyak.seoul.go.kr/web/reservation/selectUseChrgeInfoAjax.do", data=payload_5, headers=headers_1, verify=False)
print(response.text)
response = session.post(url="https://yeyak.seoul.go.kr/web/reservation/selectReservChairAjax.do", data=payload_4, headers=headers_1, verify=False)
print(response.text)
response = session.post(url="https://yeyak.seoul.go.kr/web/reservation/insertReservReceipt.do", data=payload_5, headers=headers_1, verify=False)
print(response.text)

