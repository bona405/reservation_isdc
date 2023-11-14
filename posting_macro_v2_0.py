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
import pytesseract
import cv2
from google.cloud import vision

##############################################################################################################
#################### SET UP #################################################################################
#############################################################################################################

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
op_mode='0'

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
NumberOfPopups = int(config['MODE']['NumberOfPopups'])
op_mode = config['MODE']['op_mode']
IsAutoDate = config['MODE']['AutoDate']

if(IsAutoDate == '1'):
    current_date = datetime.date.today()
    next1_date = current_date + datetime.timedelta(days=1)
    year = str(next1_date.year)
    month = str(next1_date.month)
    day = str(next1_date.day)
    next3_date = current_date + datetime.timedelta(days=4)
    target_year = str(next3_date.year)
    target_month = str(next3_date.month)
    target_day = str(next3_date.day)


print("#################info####################")
print("my ID      : "+my_id)
print("target_date: "+target_year + target_month + target_day)
print("court_info : "+court_id + "    " +court_time)
print("partner    : "+user2_name + "            " +user2_phone)
print("op_mode    : "+op_mode)
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

##############################################################################################################
#################### SET UP #################################################################################
#############################################################################################################

target_date = target_year+'-'+target_month+'-'+target_day
target_date_int = datetime.datetime(int(target_year), int(target_month), int(target_day))
execution_date = year+'-'+month+'-'+day


while True:
    now = datetime.datetime.now()
    time_until_execution = execution_datetime - now
    print(time_until_execution)
    if time_until_execution <= datetime.timedelta(seconds=20):
        print("20sec or less remaining. Exiting the loop.")
        break
    time.sleep(5) # Wait for 1 second before checking again

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
###############################################################
#####################  posting  ##################
###############################################################
session = requests.Session()
##############  Login  ###################
login_data = {
    "web_id": my_id,
    "web_pw": my_pw,
}
login_response = session.post(url="https://res.isdc.co.kr/loginCheck.do", data=login_data)
if "loginCheck.do" not in login_response.url:
    print("Login successful")
else:
    print("Login failed")

##############  Get user name, Phone number  ###################
user_info_response = session.get(url="https://res.isdc.co.kr/memberModify.do")
if user_info_response.status_code == 200:
    soup = BeautifulSoup(user_info_response.text, 'html.parser')
    name_element = soup.find('input', {'id': 'mem_nm'})
    phone_number_element = soup.find('input', {'id': 'h_tel_no'})
    name = name_element['value']
    phone_number = phone_number_element['value']
    print("User Name:", name)
    print("User Phone Number:", phone_number)
else:
    print("Failed to fetch the webpage. Status code:", user_info_response.status_code)

execution_timezone = pytz.timezone('Asia/Tokyo')  # Assuming execution time is in GMT+9 timezone
execution_datetime = execution_timezone.localize(execution_datetime)
while True:
    server_time = get_server_time(url="https://res.isdc.co.kr")
    if server_time is not None:
        server_time_gmt9 = server_time_to_gmt9(server_time)
        if server_time_gmt9 >= execution_datetime:
            print("Server time has passed the execution datetime. Exiting the loop.")
            break
        else:
            print(f"Server Time: {server_time_gmt9}")
    else:
        print("Failed to retrieve server time. Retrying...")


reservation_data = {
    'resdate': target_date,
    'facId': court_id,
}
iteration_no = 0
while True:
    ##############  Reservation info resuser  ###################
    text_court_name = ''
    fac_info_response = session.post(url="https://res.isdc.co.kr/facilityInfo.do", data=reservation_data)
    if fac_info_response.status_code == 200:
        soup = BeautifulSoup(fac_info_response.text, 'html.parser')
        title_element = soup.find('p', class_='tit')
        text_court_name = title_element.get_text(strip=True)
        print(text_court_name)

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
    else:
        print("Failed to retrieve the fac_url page. Status code:", fac_info_response.status_code)

    ##############  Reservation info ttid  ###################
    ttid_val = '0'
    res_table_response = session.post(url="https://res.isdc.co.kr/getTimeTableByDate.do", data=reservation_data)
    if res_table_response.status_code == 200:
        soup = BeautifulSoup(res_table_response.text, 'html.parser')
        input_element = soup.find('input', id=rbTime)
        if input_element:
            ttid_val = input_element.get('value')
            print("ttid:", ttid_val)
        else:
            print("ttid element not found.")
    else:
        print("Failed to retrieve the res_table_url page. Status code:", res_table_response.status_code)
     
    ##############  discount info  ###################
    headers = {
        "Referer": "https://res.isdc.co.kr/facilityInfo.do"
    }
    discount = '0'
    res_info_response = session.post(url="https://res.isdc.co.kr/reservationInfo.do", data=reservation_data, headers = headers)
    if res_info_response.status_code == 200:
        soup = BeautifulSoup(res_info_response.text, 'html.parser')
        select_element = soup.find('select', id='discount')
        if select_element:
            selected_option = select_element.find('option', selected=True)
            if selected_option:
                discount = selected_option['value']
                print("discount:", discount)
            else:
                print("Selected option not found.")
        else:
            print("Select element not found.")
    else:
        print("Failed to retrieve the res_info_response page. Status code:", res_info_response.status_code)


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
    userType_response = session.post(url="https://res.isdc.co.kr/checkUserType.do", data=userType_data, headers = headers)
    time.sleep(0.5)
    headcount_response = session.post(url="https://res.isdc.co.kr/checkHeadcount.do", data=user_data, headers = headers)
    time.sleep(0.5)
    user2_response = session.post(url="https://res.isdc.co.kr/checkUser2.do", data=user_data, headers = headers)
    time.sleep(0.5)
    ##############  captchaimg  ###################
    captchaimg_loop_flg = True
    while(captchaimg_loop_flg):
        captchaImg_response = session.get(url="https://res.isdc.co.kr/captchaImg.do", headers=headers)
        if captchaImg_response.status_code == 200:
            image_data = captchaImg_response.content
            image = Image.open(BytesIO(image_data))
            image.save('image.png')
            print("image_downloaded")
        else:
            print("Failed to fetch the image")

        ocr_result = ''
        ocr_result = detect_text('image.png')
        print(ocr_result)

        ##############  chkAnswer  ###################
        answer = {
            'answer': ocr_result
        }
        # Send a GET request with the Referer header
        chkAnswer_response = session.post(url="https://res.isdc.co.kr/chkAnswer.do", data=answer, headers=headers)
        if chkAnswer_response.text == '200':
            print("chkAnswer success!")
            captchaimg_loop_flg = False
        else:
            print("chkAnswer failed")
            captchaimg_loop_flg = True

    ##############  cost info  ###################
    costId = '0'
    cost = '0'
    cost_data = {
        'resdate': target_date,
        'facId': court_id,
        'ttId': ttid_val,
    }
    cos_info_response = session.post(url="https://res.isdc.co.kr/getCostInfo.do", data=cost_data)
    if cos_info_response.status_code == 200:
        response_data = json.loads(cos_info_response.text)
        costVO = response_data.get('costVO', {})
        costId = costVO.get('costId')
        cost = costVO.get('cost')
        print("costId:", costId)
    else:
        print("Failed to retrieve the cost_info_url page. Status code:", cos_info_response.status_code)

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
        'penaltyFlag': '',
        'facType': '29',
        'residenceType': '',
        'fresStartDate': '',
        'fresEndDate': '',
        'fuseStartDate': '',
        'fuseEndDate': '',
        'fresStartTime': '',
        'fresEndTime': '',
        'miniHeadcount': '2',
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
    time.sleep(0.5)
    Reservation_response = session.post(url="https://res.isdc.co.kr/insertReservation.do", data=params, headers=headers)
    if Reservation_response.status_code == 200:
        print("insertReservation: " + Reservation_response.text)
    else:
        print("insertReservation: ", Reservation_response.status_code)

    if 'RES' in Reservation_response.text:
        print("===== reservaton success!! =====")
        break 

    iteration_no = iteration_no + 1
    if iteration_no > 10:
        break
    time.sleep(0.5)
    print("repeated : ", iteration_no)


logging.basicConfig(filename='res_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logging.info(f'Reservation_response text: {Reservation_response.text}')
logging.info(f'Reservation_response status: {Reservation_response.status_code}')
for key, value in params.items():
    logging.info(f'{key}: {value}')
logging.shutdown()


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
    print("Gist created successfully.")
    print("Gist URL:", response.json()["html_url"])
else:
    print("Failed to create Gist. Status code:", response.status_code)

while True :
    exit_ = input("\n press enter to quit\n")
    break
