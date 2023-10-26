#-*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json

import datetime
import time
import configparser
import pytz
import logging

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

###############################################################
#####################  posting  ##################
###############################################################
original_url = "https://res.isdc.co.kr"
login_url = "https://res.isdc.co.kr/loginCheck.do"
user_info_url = "https://res.isdc.co.kr/memberModify.do"
fac_url = "https://res.isdc.co.kr/facilityInfo.do"
res_info_url = "https://res.isdc.co.kr/reservationInfo.do"
res_table_url = "https://res.isdc.co.kr/getTimeTableByDate.do"
cost_info_url = "https://res.isdc.co.kr/getCostInfo.do"
ajax_url = "https://res.isdc.co.kr/insertReservation.do"

session = requests.Session()

##############  Login  ###################
login_data = {
    "web_id": my_id,
    "web_pw": my_pw,
}
login_response = session.post(login_url, data=login_data)
if "loginCheck.do" not in login_response.url:
    print("Login successful")
else:
    print("Login failed")

##############  Get user name, Phone number  ###################
user_info_response = session.get(user_info_url)
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
    server_time = get_server_time(original_url)
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
    fac_info_response = session.post(fac_url, data=reservation_data)
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
    res_table_response = session.post(res_table_url, data=reservation_data)
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
     
    ##############  cost info  ###################
    costId = '0'
    cost = '0'
    cost_data = {
        'resdate': target_date,
        'facId': court_id,
        'ttId': ttid_val,
    }
    cos_info_response = session.post(cost_info_url, data=cost_data)
    if cos_info_response.status_code == 200:
        response_data = json.loads(cos_info_response.text)
        costVO = response_data.get('costVO', {})
        costId = costVO.get('costId')
        cost = costVO.get('cost')
        print("costId:", costId)
    else:
        print("Failed to retrieve the cost_info_url page. Status code:", cos_info_response.status_code)

    ##############  res_info_url info  ###################
    discount = '0'
    # text_court_name = ''
    res_info_response = session.post(res_info_url, data=reservation_data)
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
        # target_span = soup.find('span', class_='txt1')
        # if target_span:
        #     text_court_name = target_span.get_text()
        #     print(text_court_name)
        # else:
        #     print("Element with class text_court_name not found.")
    else:
        print("Failed to retrieve the res_info_response page. Status code:", res_info_response.status_code)

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
        'g-recaptcha-response': '0',
        'etc' : name+ ' / ' +phone_number+ ',' +user2_name+ ' / ' +user2_phone,
    }
    ajax_response = session.post(ajax_url, data=params)
    if ajax_response.status_code == 200:
        print("AJAX requested")
        print(ajax_response.text)
    else:
        print("AJAX request fail: ", ajax_response.status_code)

    if 'RES' in ajax_response.text:
        print("===== reservaton success!! =====")
        break 

    iteration_no = iteration_no + 1
    if iteration_no > 10:
        break
    time.sleep(3)
    print("repeated : ", iteration_no)


logging.basicConfig(filename='res_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logging.info(f'ajax_response text: {ajax_response.text}')
logging.info(f'ajax_response text: {ajax_response.status_code}')
for key, value in params.items():
    logging.info(f'{key}: {value}')
logging.shutdown()


while True :
    exit_ = input("\n press enter to quit\n")
    break


