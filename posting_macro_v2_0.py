#-*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json

import datetime
import time
import configparser
import pytz
import logging
from PIL import Image
from io import BytesIO
from google.cloud import vision
import random
import sys
import re

##############################################################################################################
#################### SET UP #################################################################################
#############################################################################################################
logging.basicConfig(filename='console_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
######################## reserve info #########################
my_id = 'bona405'
my_pw = 'jong8576!@'
target_year = '2023'
target_month = '3'
target_day = '31'
court_id = 'FAC26'
court_time = '1'
user2_name = "김훈"
user2_phone = "01071627106"
######################## execution day #########################
year='2023'
month='3'
day='28'
hour='6'
minute='58'
second='0'

# Create ConfigParser object
config = configparser.ConfigParser()

# Read from file
config.read('config.ini')

# Get values from each section
my_id = config['LOGIN']['ID']
my_pw = config['LOGIN']['password']
target_year = config['RESERVATION']['target_year']
target_month = config['RESERVATION']['target_month']
target_day = config['RESERVATION']['target_day']
court_id = config['RESERVATION']['target_court']
court_time = config['RESERVATION']['target_schedule']
user2_name = config['PARTNER']['name']
user2_phone = config['PARTNER']['phone_no']
year = config['EXECUTION']['year']
month = config['EXECUTION']['month']
day = config['EXECUTION']['day']
hour  = config['EXECUTION']['hour']
minute  = config['EXECUTION']['minute']
second  = config['EXECUTION']['second']
IsAutoDate = config['MODE']['AutoDate']
time_delay = float(config['MODE']['time_delay'])

if IsAutoDate == '1':
    current_datetime = datetime.datetime.now()
    cutoff_time = datetime.time(7, 0, 0)  # 7:00 AM
    if current_datetime.time() < cutoff_time:
        next1_datetime = current_datetime.replace(hour=7, minute=0, second=0, microsecond=0)
    else:
        next1_date = (current_datetime + datetime.timedelta(days=1)).date()
        next1_datetime = datetime.datetime.combine(next1_date, cutoff_time)
    
    next3_date = (next1_datetime + datetime.timedelta(days=3)).date()
    year = str(next1_datetime.year)
    month = str(next1_datetime.month)
    day = str(next1_datetime.day)
    target_year = str(next3_date.year)
    target_month = str(next3_date.month)
    target_day = str(next3_date.day)


print("#################info####################")
print("my ID      : "+my_id)
print("target_date: "+target_year + target_month + target_day)
print("court_info : "+court_id + "    " +court_time)
print("partner    : "+user2_name + "            " +user2_phone)
print("##########################################")
execution_datetime = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
print('execute on: ' + str(execution_datetime) + '\n')

#####################  schedule info  ############################
rbTime_mapping = {
    '0': 'rbTime-0',
    '1': 'rbTime-1',
    '2': 'rbTime-2',
    '3': 'rbTime-3',
    '4': 'rbTime-4',
    '5': 'rbTime-5',
    '6': 'rbTime-6',
    '7': 'rbTime-7',
}
rbTime = rbTime_mapping.get(court_time, None)

def get_server_time(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            server_time_str = response.headers.get('Date')
            server_time = datetime.datetime.strptime(server_time_str, '%a, %d %b %Y %H:%M:%S %Z')
            return server_time
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
def server_time_to_gmt9(server_time):
    gmt9 = pytz.timezone('Asia/Tokyo')  # Time zone for GMT+9
    server_time_gmt9 = server_time.replace(tzinfo=pytz.utc).astimezone(gmt9)
    return server_time_gmt9
def detect_text(path):
    client = vision.ImageAnnotatorClient()
    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    image_context = vision.ImageContext(language_hints=["ar"],)
    response = client.text_detection(image=image, image_context=image_context)
    texts = response.text_annotations
    return texts[0].description
def validate_six_digit_number(number):
    if number.isdigit() and len(number) == 6:
        return True
    else:
        return False
def check_iteration(iteration_no, max_no, sleep_time):
    if iteration_no > max_no:
        print("\niteration timeout")
        sys.exit()
    time.sleep(sleep_time)
    print("repeated:", iteration_no)

def safe_post(session, url, data, headers=None, max_retries=5, sleep_time=0.1, timeout=30):
    iteration_no = 0
    while iteration_no < max_retries:
        try:
            response = session.post(url=url, data=data, headers=headers, timeout=timeout)
            response.raise_for_status()  
            print('URL successful : ' + url)
            return response
        except requests.exceptions.HTTPError as http_err:
            log_and_print(f"HTTP error occurred: {http_err}") 
        except requests.exceptions.ConnectionError as conn_err:
            log_and_print(f"Connection error occurred: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            log_and_print(f"Timeout error occurred: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            log_and_print(f"Request error occurred: {req_err}")
        iteration_no += 1
        print("Retrying...")
        time.sleep(sleep_time)
    print('URL failed : ' + url)
    sys.exit()

def safe_get(session, url, headers=None, max_retries=5, sleep_time=0.1):
    iteration_no = 0
    while iteration_no < max_retries:
        try:
            response = session.get(url=url, headers=headers)
            response.raise_for_status()  
            print('URL successful : ' + url)
            return response
        except requests.exceptions.HTTPError as http_err:
            log_and_print(f"HTTP error occurred: {http_err}") 
        except requests.exceptions.ConnectionError as conn_err:
            log_and_print(f"Connection error occurred: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            log_and_print(f"Timeout error occurred: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            log_and_print(f"Request error occurred: {req_err}")
        iteration_no += 1
        print("Retrying...")
        time.sleep(sleep_time)
    print('URL failed : ' + url)
    sys.exit()

def log_and_print(message, *args):
    if args: formatted_message = message + ' ' + ' '.join(map(str, args))
    else: formatted_message = message
    logging.info(formatted_message)
    print(formatted_message)
    
patterns = {
    'discount_option': re.compile(
        r'<option[^>]*value=["\']?(\d+)["\']?[^>]*selected',
        re.DOTALL
    )
}
##############################################################################################################
#################### SET UP #################################################################################
#############################################################################################################
target_date = target_year+'-'+target_month+'-'+target_day
target_date_int = datetime.datetime(int(target_year), int(target_month), int(target_day))
execution_date = year+'-'+month+'-'+day
mlength = round(random.uniform(2000, 2500), 12)


chars = ['**StandBy**', '                  ',]
i = 0
while True:
    now = datetime.datetime.now()
    time_until_execution = execution_datetime - now
    if i >= 1: i = 0
    else: i += 1
    print("\033[F" * 1, end="")
    print(f"{time_until_execution}  {chars[i]}")

    if time_until_execution <= datetime.timedelta(seconds=20):
        print("20 seconds or less remaining. Exiting the loop.")
        break
    time.sleep(1)
###############################################################
#####################  posting  ##################
###############################################################
session = requests.Session()
start_time = None
server_sleep_time = 13
##############  Login  ##  Get user name, Phone number  ###################
login_data = {
    "web_id": my_id,
    "web_pw": my_pw,
}
url_log_in_0 = "https://res.isdc.co.kr/loginCheck.do"
url_log_in_1 = "https://res.isdc.co.kr/rest_loginCheck.do"
url_log_in = url_log_in_1
iteration_no = 0
while True:
    login_response = safe_post(session, url_log_in, login_data, max_retries=5, sleep_time=1)
    user_info_response = safe_get(session, url="https://res.isdc.co.kr/memberModify.do", max_retries=5, sleep_time=0.5)
    soup = BeautifulSoup(user_info_response.text, 'html.parser')
    name_element = soup.find('input', {'id': 'mem_nm'})
    phone_number_element = soup.find('input', {'id': 'h_tel_no'})
    name = name_element['value']
    phone_number = phone_number_element['value']
    if name and phone_number:
        log_and_print("User Name:", name)
        log_and_print("User Phone Number:", phone_number)
        break 
    else:
        log_and_print("Error: no name nor phone.no")
        iteration_no += 1
        check_iteration(iteration_no, 10, 0.5) 

execution_timezone = pytz.timezone('Asia/Tokyo')  # Assuming execution time is in GMT+9 timezone
execution_datetime = execution_timezone.localize(execution_datetime)
iteration_no = 0
while True:
    server_time = get_server_time(url="https://res.isdc.co.kr")
    if server_time is not None:
        server_time_gmt9 = server_time_to_gmt9(server_time)
        if server_time_gmt9 >= execution_datetime:
            log_and_print("Server time has passed the execution datetime. Exiting the loop.")
            break
        else:
            log_and_print(f"Server Time: {server_time_gmt9}")
    else:
        log_and_print("Failed to retrieve server time. Retrying...")
        iteration_no += 1
        check_iteration(iteration_no, 10, 0.5)


reservation_data = {
    'resdate': target_date,
    'facId': court_id,
}
text_court_name = ''
fac_info_response = safe_post(session, url="https://res.isdc.co.kr/facilityInfo.do", data=reservation_data, max_retries=5, sleep_time=0.5)
soup = BeautifulSoup(fac_info_response.text, 'html.parser')
title_element = soup.find('p', class_='tit')
text_court_name = title_element.get_text(strip=True)
log_and_print(text_court_name)
inResUserType = soup.find('input', {'id': 'inResUserType'})['value']
inResDay = soup.find('input', {'id': 'inResDay'})['value']
inResEndTime = soup.find('input', {'id': 'inResEndTime'})['value']
inResStartTime = soup.find('input', {'id': 'inResStartTime'})['value']
outResUserType = soup.find('input', {'id': 'outResUserType'})['value']
outResDay = soup.find('input', {'id': 'outResDay'})['value']
outResStartTime = soup.find('input', {'id': 'outResStartTime'})['value']
outResEndTime = soup.find('input', {'id': 'outResEndTime'})['value']
durationType = soup.find('input', {'id': 'durationType'})['value']
internetBooking = soup.find('input', {'id': 'internetBooking'})['value']

##############  Reservation info ttid  ###################
ttid_val = '0'
iteration_no = 0
while True:
    res_table_response = safe_post(session, url="https://res.isdc.co.kr/getTimeTableByDate.do", data=reservation_data, max_retries=5, sleep_time=0.5)
    # start_time = time.time()
    soup = BeautifulSoup(res_table_response.text, 'html.parser')
    input_element = soup.find('input', id=rbTime)
    if input_element:
        ttid_val = input_element.get('value')
        log_and_print("ttid:", ttid_val)
        break 
    else:
        log_and_print("Error: no ttid found")
        iteration_no += 1
        check_iteration(iteration_no, 20, 0.01) 

##############  discount info  ###################
iteration_no = 0
discount = '0'
while True:
    # start_time = time.time()
    # log_and_print("----------local time(start): ", time.strftime("%H:%M:%S"))
    headers = {
        "Referer": "https://res.isdc.co.kr/facilityInfo.do"
    }
    res_info_response = safe_post(session, url="https://res.isdc.co.kr/reservationInfo.do", data=reservation_data, headers=headers, max_retries=20, sleep_time=0.01, timeout=5)
    start_time = time.time()
    log_and_print("----------local time(start): ", time.strftime("%H:%M:%S"))

    if 'discount' in res_info_response.text:
        match = patterns['discount_option'].search(res_info_response.text)
        if match:
            discount = match.group(1)
            log_and_print("discount:", discount)
            break
        else:
            log_and_print("Error: discount select found but no selected option")
            iteration_no += 1
            check_iteration(iteration_no, 10, 0.5)
    else:
        log_and_print("No discount select element found")
        iteration_no += 1
        check_iteration(iteration_no, 100, 0.01)


iteration_no = 0
iteration_no_t = 0
# time_delay = 1.5
while True:     
    headers = {
        "Referer": "https://res.isdc.co.kr/reservationInfo.do"
    }
    userType_data = {
        'userType': 'P',
        'facId': court_id
    }
    user_data = {
        'facId': court_id
    }
    time.sleep(time_delay)
    userType_response = safe_post(session, url="https://res.isdc.co.kr/checkUserType.do", data=userType_data, headers=headers, max_retries=5, sleep_time=0.5)
    time.sleep(time_delay)
    headcount_response = safe_post(session, url="https://res.isdc.co.kr/checkHeadcount.do", data=user_data, headers=headers, max_retries=5, sleep_time=0.5)
    time.sleep(time_delay)
    user2_response = safe_post(session, url="https://res.isdc.co.kr/checkUser2.do", data=user_data, headers=headers, max_retries=5, sleep_time=0.5)
    time.sleep(time_delay)
    checkAnswer_response = safe_post(session, url="https://res.isdc.co.kr/checkAnswer.do", data=user_data, headers=headers, max_retries=5, sleep_time=0.5)
    time.sleep(time_delay)
    ##############  captchaimg  ###################
    captchaimg_loop_flg = True
    while(captchaimg_loop_flg):
        captchaImg_response = safe_get(session, url="https://res.isdc.co.kr/captchaImg.do", headers=headers, max_retries=5, sleep_time=0.5)
        if captchaImg_response.status_code == 200:
            image_data = captchaImg_response.content
            image = Image.open(BytesIO(image_data))
            image.save('image.png')
            log_and_print("image_downloaded")
        else:
            log_and_print("Failed to fetch the image")

        ocr_result = ''
        ocr_result = detect_text('image.png')
        log_and_print(ocr_result)
        
        ##############  chkAnswer  ###################
        answer = {
            'answer': ocr_result
        }
        if(validate_six_digit_number(ocr_result)):
            time.sleep(time_delay)
            chkAnswer_response = safe_post(session, url="https://res.isdc.co.kr/chkAnswer.do", data=answer, headers=headers, max_retries=5, sleep_time=0.5)
            if chkAnswer_response.text == '200':
                log_and_print("chkAnswer success!")
                captchaimg_loop_flg = False
            else:
                log_and_print("chkAnswer failed")
                captchaimg_loop_flg = True
                iteration_no += 1
                check_iteration(iteration_no, 10, 0)
                
    time.sleep(time_delay)
    ##############  cost info  ###################
    costId = '0'
    cost = '0'
    cost_data = {
        'resdate': target_date,
        'facId': court_id,
        'ttId': ttid_val,
    }
    cos_info_response = safe_post(session, url="https://res.isdc.co.kr/getCostInfo.do", data=cost_data, max_retries=5, sleep_time=0.5)
    if cos_info_response.status_code == 200:
        response_data = json.loads(cos_info_response.text)
        costVO = response_data.get('costVO', {})
        costId = costVO.get('costId')
        cost = costVO.get('cost')
        log_and_print("costId:", costId)
    else:
        log_and_print("https://res.isdc.co.kr/getCostInfo.do not found. code:", cos_info_response.status_code)

    ############## Final post ###################
    params = {
        'ttId': ttid_val,
        'startTime': '',
        'costId': costId, #
        'discountId': discount,
        'subFacCnt': '',
        'eventId': '32',
        'userId': my_id,
        'originCost': cost,
        'teamId': '0',
        'ju_dc': '1',
        'resType': '8',
        'penaltyFlag': 'true',
        'facType': '29',
        'residenceType': '',
        'fresStartDate': '',
        'fresEndDate': '',
        'fuseStartDate': '',
        'fuseEndDate': '',
        'fresStartTime': '',
        'fresEndTime': '',
        'miniHeadcount': '2',
        'mlength': mlength,
        'facId': court_id,
        'durationType': durationType,
        'inResUserType': inResUserType,
        'inResDay': inResDay,
        'inResStartTime': inResStartTime,
        'inResEndTime': inResEndTime,
        'outResUserType': outResUserType,
        'outResDay': outResDay,
        'outResStartTime': outResStartTime,
        'outResEndTime': outResEndTime,
        'internetBooking': internetBooking,
        'loginname': text_court_name,
        'resdate': target_date,
        'rbTime': ttid_val,
        'userType': 'P',
        'teamName': '',
        'loginname': name,
        'loginname': phone_number,
        'headcount': '2',
        'user1': name,
        'user1_contact': phone_number,
        'user2': user2_name,
        'user2_contact': user2_phone,
        'user3': '',
        'user3_contact': '',
        'user4': '',
        'user4_contact': '',
        'user5': '',
        'user5_contact': '',
        'user6': '',
        'user6_contact': '',
        'user7': '',
        'user7_contact': '',
        'user8': '',
        'user8_contact': '',
        'discount': discount,
        'subfacname': '이용 부속시설 없음',
        'cost': cost,
        'subcost': '0',
        'totalCost': cost,
        'etc' : name+ ' / ' +phone_number+ ',' +user2_name+ ' / ' +user2_phone,
    }
    time.sleep(time_delay)
    # CheckPenalty_response = session.post(url="https://res.isdc.co.kr/checkPenaltyResCnt.do", data=params, headers=headers)
    # log_and_print("CheckPenalty_response: " + CheckPenalty_response.text)
    end_time = time.time()
    elapsed_time = end_time - start_time
    log_and_print("elapsed time : %.6f s" % elapsed_time)
    if elapsed_time < server_sleep_time:
        additional_sleep = server_sleep_time - elapsed_time
        log_and_print("Sleep additional time : %.6f s" % additional_sleep)
        time.sleep(additional_sleep)
    log_and_print("----------local time(reserving...): ", time.strftime("%H:%M:%S"))
    Reservation_response = safe_post(session, url="https://res.isdc.co.kr/insertReservation.do", data=params, headers=headers, max_retries=2, sleep_time=0.1)
    log_and_print("----------local time(reserved...): ", time.strftime("%H:%M:%S"))
    if Reservation_response.status_code == 200:
        log_and_print("insertReservation: " + Reservation_response.text)
    else:
        log_and_print("insertReservation: ", Reservation_response.status_code)

    if 'RES' in Reservation_response.text:
        log_and_print("===== reservaton success!! =====")
        break 
    # time_delay = time_delay + 0.1
    # log_and_print("time_delay : ", time_delay)
    iteration_no_t += 1
    check_iteration(iteration_no_t, 1, 0.5)

# Gists
token = "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"
gists_url = "https://api.github.com/gists"

headers = {
    "Authorization": f"token {token}",
}
data = {
    "public": False,
    "files": {
        "variables.txt": {
            "content": f"name: {name}\n"
                       f"text_court_name: {text_court_name}\n"
                       f"target_date: {target_date}\n"
                       f"rbTime: {rbTime}\n"
                       f"Reservation_response.status_code: {Reservation_response.status_code}\n"
                       f"Reservation_response.text: {Reservation_response.text}\n"
        }
    }
}
response = requests.post(gists_url, headers=headers, data=json.dumps(data))

if response.status_code == 201:
    log_and_print("Gist created successfully.")
    log_and_print("Gist URL:", response.json()["html_url"])
else:
    log_and_print("Failed to create Gist. Status code:", response.status_code)

sys.exit()


