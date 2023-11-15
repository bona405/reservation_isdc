#-*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

import datetime
import time
import configparser
import requests
import json
from bs4 import BeautifulSoup

import datetime
import time
import configparser
import pytz
import logging
from PIL import Image
from io import BytesIO
import cv2
from google.cloud import vision
import urllib.parse
import random


##############################################################################################################
#################### SET UP #################################################################################
#############################################################################################################

######################## reserve info #########################
my_id = 'bona405'
my_pw = 'jong8576!@'
target_year = '2023'
target_month = '3'
target_day = '31'
court_id = 'court_1_normal'
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
time_css = [''] * 8
time_css[0] = "rbTime-0"
time_css[1] = "rbTime-1"
time_css[2] = "rbTime-2"
time_css[3] = "rbTime-3"
time_css[4] = "rbTime-4"
time_css[5] = "rbTime-5"
time_css[6] = "rbTime-6"
time_css[7] = "rbTime-7"
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
def validate_six_digit_number(number):
    if number.isdigit() and len(number) == 6:
        return True
    else:
        return False

###############################################################
#####################  chrome driver set up  ##################
###############################################################
chrome_options = Options()

chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('--disable-webgl')
# chrome_options.add_argument('--disable-extensions')
# chrome_options.add_argument('--blink-settings=imagesEnabled=false')
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=chrome_options)

# Navigate to the web page
url_0 = 'https://res.isdc.co.kr/facilityList.do?facType=29'
url_1 = 'https://res.isdc.co.kr/login.do'

###############################################################
#####################  Log in  ################################
###############################################################
# go to login page
driver.get(url_1)
# enter your username and password
driver.find_element(By.ID, "web_id").send_keys(my_id)
driver.find_element(By.ID, "web_pw").send_keys(my_pw)
time.sleep(1)

# submit the login form
driver.find_element(By.ID, "btn_login").click()
time.sleep(1)

###############################################################
#####################  reservation page  #######################
###############################################################
# go to tennis court page
driver.get(url_0)
# driver.maximize_window()


# court, time select
driver.find_element(By.ID, op_mode).click()
time.sleep(1)

driver.find_element(By.ID, court_id).click()
time.sleep(1)

MonthDiff = int(target_month) - int(month)
RunTime0 = 0
element_move_reservation = None
element_nextMon = None
RunTime1 = 0
# IsClicked1 = False
element_time_css = None
court_time_int = int(court_time)
mlength = round(random.uniform(2000, 2500), 12)

###############################################################
####################  Loop Start #############################
###############################################################
while element_move_reservation == None:
    try:
        if MonthDiff != 0:
            driver.find_element(By.NAME, "nextMon").click()
        # time.sleep(0.5) #no needed 230824
        driver.find_element(By.ID, target_date).click()
        element_move_reservation = driver.find_element(By.ID, "move_reservation")
        element_move_reservation.click()
        now = datetime.datetime.now() #temp
        print(now.strftime("%Y-%m-%d %H:%M:%S.%f")) #temp
    except:
        element_move_reservation = None
        driver.refresh()
        print("D-refrsh " + str(RunTime0))
        RunTime0 = RunTime0 + 1
        if(RunTime0 > 1000):
            time.sleep(1)
            RunTime0 = 0
            now = datetime.datetime.now()
            print(now.strftime("%Y-%m-%d %H:%M:%S.%f"))
print("date selected!")


if MonthDiff != 0:
    driver.find_element(By.NAME, "nextMon").click()


alert_message = ''
Validation_Check = False
while Validation_Check == False:
    try:
        time.sleep(0.5)
        ocr_nok_flg = True
        while(ocr_nok_flg == True):
            img_element = driver.execute_script('return document.querySelector("#selection > div > div:nth-child(15) > div:nth-child(2) > img:nth-child(1)");')
            img_element.screenshot('image.png')
            ocr_result = detect_text('image.png')
            if(validate_six_digit_number(ocr_result)):
                ocr_nok_flg = False
            else:
                driver.execute_script("document.querySelector(\"#reload\").click();")
        print("OCR clear!")
        driver.execute_script("document.getElementById('answer').value = '" + ocr_result + "';")
        driver.execute_script("document.querySelector(\"#check\").click();")
        alert = Alert(driver)
        alert.accept()
        time.sleep(1.3)
        driver.find_element(By.NAME, "headcount").click()
        time.sleep(1.3)
        driver.find_element(By.ID, "user2").click()
        time.sleep(1.3)
        driver.find_element(By.ID, "user2_contact").click()
        time.sleep(0.1)
        driver.execute_script("document.getElementById('"+ time_css[court_time_int] +"').click();")
        time.sleep(0.1)
        driver.find_element(By.CSS_SELECTOR, "label[for='userType-P']").click()
        time.sleep(0.1)
        driver.execute_script("document.getElementsByName('headcount')[0].value='2';")
        driver.execute_script("document.getElementsByName('user2')[0].value='" + user2_name + "';")
        driver.execute_script("document.getElementsByName('user2_contact')[0].value='" + user2_phone + "';")
        driver.execute_script(f"$('#mlength').val('{mlength}');")
        driver.execute_script("document.getElementById('btnReservation').click();")
        print("Alert Message:", alert_message)
        alert = driver.switch_to.alert
        alert_message = alert.text
        print(alert_message)
        if(alert_message == "예약되었습니다."):
            Validation_Check = True
    except:
        driver.refresh()
        print("R-refrsh " + str(RunTime1))
        RunTime1 = RunTime1 + 1
        if(RunTime1 > 1000):
            time.sleep(1)
            RunTime1 = 0
            now = datetime.datetime.now()
            print(now.strftime("%Y-%m-%d %H:%M:%S.%f"))

now = datetime.datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S.%f"))


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
soup = BeautifulSoup(user_info_response.text, 'html.parser')
name_element = soup.find('input', {'id': 'mem_nm'})
phone_number_element = soup.find('input', {'id': 'h_tel_no'})
name = name_element['value']
phone_number = phone_number_element['value']
print("User Name:", name)
print("User Phone Number:", phone_number)

reservation_data = {
    'resdate': target_date,
    'facId': court_id,
}
text_court_name = ''
fac_info_response = session.post(url="https://res.isdc.co.kr/facilityInfo.do", data=reservation_data)
if fac_info_response.status_code == 200:
    soup = BeautifulSoup(fac_info_response.text, 'html.parser')
    title_element = soup.find('p', class_='tit')
    text_court_name = title_element.get_text(strip=True)
    print(text_court_name)
    
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
            "content": f"my ID : {my_id}\n"
                       f"name: {name}\n"
                       f"target_date: {target_date}\n"
                       f"text_court_name: {text_court_name}\n"
                       f"rbTime: {court_time}\n"
                       f"alert_message: {alert_message}\n"
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
