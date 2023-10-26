#-*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import keyboard
import datetime
import time
import timeit
import configparser

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

#####################  court info  ############################
if court_id ==   'court_1_normal'       : court_element_id = 'FAC26'
elif court_id == 'court_2_weekend'      : court_element_id = 'FAC44'
elif court_id == 'court_2_normal'       : court_element_id = 'FAC17'
elif court_id == 'court_3_weekend'      : court_element_id = 'FAC42'
elif court_id == 'court_3_normal'       : court_element_id = 'FAC18'
elif court_id == 'court_4_weekend'      : court_element_id = 'FAC43'
elif court_id == 'court_4_normal'       : court_element_id = 'FAC35'
elif court_id == 'court_1_today_weekend': court_element_id = 'FAC46'
elif court_id == 'court_1_today_normal' : court_element_id = 'FAC12'
elif court_id == 'court_2_today_weekend': court_element_id = 'FAC47'
elif court_id == 'court_2_today_normal' : court_element_id = 'FAC20'
elif court_id == 'court_t'              : court_element_id = 'FAC38'
else                                    : None

time_css = [''] * 5
time_css[0] = "label[for=\"rbTime-0\"]"
time_css[1] = "label[for=\"rbTime-1\"]"
time_css[2] = "label[for=\"rbTime-2\"]"
time_css[3] = "label[for=\"rbTime-3\"]"
time_css[4] = "label[for=\"rbTime-4\"]"
##############################################################################################################
#################### SET UP #################################################################################
#############################################################################################################

target_date = target_year+'-'+target_month+'-'+target_day
target_date_int = datetime.datetime(int(target_year), int(target_month), int(target_day))
execution_date = year+'-'+month+'-'+day

if target_date_int == datetime.datetime(int(year), int(month), int(day)) :
    if court_id.split('_')[2] != 'today':
        print("\n target day and execution day are same. did you choose the right court?\n")
        ans0 = input("Y/N?\n")
        if ans0 != "Y":
            quit()
if target_date_int.weekday() >= 5 :
    if court_id.split('_')[-1] != 'weekend':
        print("\n target day is weekend. did you choose the right court?\n")
        ans0 = input("Y/N?\n")
        if ans0 != "Y":
            quit()
else:
    if court_id.split('_')[-1] != 'normal':
        print("\n target day is weekday. did you choose the right court?\n")
        ans0 = input("Y/N?\n")
        if ans0 != "Y":
            quit()

while True:
    now = datetime.datetime.now()
    print(execution_datetime-now)
    if now >= execution_datetime:
        break
    time.sleep(5) # Wait for 1 second before checking again

###############################################################
#####################  chrome driver set up  ##################
###############################################################
chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-webgl')
chrome_options.add_argument('--disable-extensions')
# chrome_options.add_argument('--blink-settings=imagesEnabled=false')

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}

# driver = webdriver.Chrome(options=chrome_options, desired_capabilities=caps)
driver = webdriver.Chrome(options=chrome_options)

# Enable network interception
driver.execute_cdp_cmd('Network.enable', {})

# Add request blocking patterns to block the 'assets' folder
folder_pattern = '*/img/*'
driver.execute_cdp_cmd('Network.setBlockedURLs', {"urls": [folder_pattern]})

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

# Get the handle of the main window
main_window_handle = driver.current_window_handle

# Close the pop-up window
for i in range(NumberOfPopups):
    for handle in driver.window_handles:
        if handle != main_window_handle:
            popup_window_handle = handle
    driver.switch_to.window(popup_window_handle)
    driver.close()

# Switch back to the main window
driver.switch_to.window(main_window_handle)


# court, time select
driver.find_element(By.ID, '1').click()
time.sleep(1)

driver.find_element(By.ID, court_element_id).click()
time.sleep(1)

MonthDiff = int(target_month) - int(month)
RunTime0 = 0
element_move_reservation = None
element_nextMon = None
RunTime1 = 0
# IsClicked1 = False
element_time_css = None
court_time_int = int(court_time)
Validation_Check = False
RGB_R = 'rgb(173, 118, 139)'
RGB_G = 'rgb(212, 245, 193)'
RGB_B = 'rgb(209, 209, 209)'
now = datetime.datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S.%f"))
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
    # time.sleep(0.08)
    # now = datetime.datetime.now()
    # print(now.strftime("%Y-%m-%d %H:%M:%S.%f"))
time.sleep(100)

if MonthDiff != 0:
    driver.find_element(By.NAME, "nextMon").click()
    # driver.find_element(By.ID, target_date).click()
if op_mode != '0' :
    driver.execute_script("document.getElementById('"+target_date+"').click();")


while Validation_Check == False:
    try:
        driver.execute_script("document.querySelector('"+ time_css[court_time_int] +"').click();")
        driver.execute_script("document.querySelector('label[for=\"userType-P\"]').click();")
        driver.execute_script("document.getElementsByName('headcount')[0].value='2';")
        driver.execute_script("document.getElementsByName('user2')[0].value='" + user2_name + "';")
        driver.execute_script("document.getElementsByName('user2_contact')[0].value='" + user2_phone + "';")

        # #########  recaptcha  ##########
        # for i in range(1):
        #     keyboard.press_and_release('tab')
        #     time.sleep(0.001)
        # keyboard.press_and_release('enter')
        # time.sleep(10)

        driver.execute_script("document.getElementById('btnReservation').click();")
        print("reservation button pushed")
        now = datetime.datetime.now() #temp
        print(now.strftime("%Y-%m-%d %H:%M:%S.%f")) #temp
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

alert = driver.switch_to.alert
alert_message = alert.text
print("Alert Message:", alert_message)

now = datetime.datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S.%f"))

# driver.switch_to.default_content()
###############################################################     

while True :
    exit_ = input("\n press enter to quit\n")
    driver.quit()
    break