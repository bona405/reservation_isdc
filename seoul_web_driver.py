from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import time
from selenium.common.exceptions import NoSuchElementException


# URL for the login page
main_url = "https://yeyak.seoul.go.kr/web/main.do"
login_url = "https://yeyak.seoul.go.kr/web/loginForm.do"
reserve_url = "https://yeyak.seoul.go.kr/web/reservation/selectReservView.do?rsv_svc_id=S210216135442800789&code=T100&dCode=&sch_order=1&sch_choose_list=&sch_type=&sch_text=%EB%A7%88%EB%A3%A8%EA%B3%B5%EC%9B%90&sch_recpt_begin_dt=&sch_recpt_end_dt=&sch_use_begin_dt=&sch_use_end_dt=&svc_prior=N&sch_reqst_value="
reserve_url0 = "https://yeyak.seoul.go.kr/web/reservation/selectReservView.do?rsv_svc_id=S210216140014448077"

# User credentials
id = 'bona405'
pw = 'jong8576!@'

driver = webdriver.Chrome()
def run_js(script):
    print(driver.execute_script(script))
    time.sleep(1)
driver.maximize_window()

# Open the login page
###################################################
driver.get(main_url)
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "#header > div.container > div > div.state > a").click()
time.sleep(1)

# Enter the username and password
username_field = driver.find_element(By.ID, 'userid')
username_field.send_keys(id)
time.sleep(1)
password_field = driver.find_element(By.ID, 'userpwd')
password_field.send_keys(pw)
time.sleep(1)

jscode_ = """
document.querySelector("#addUserForm > div.login_inp_box > button").click()
"""
run_js(jscode_)
###################################################


###################################################
driver.get(reserve_url0)
time.sleep(1)

date = '20240926'
# jscode_ = f"""
# document.querySelector("#div_cal_{date}").click()
# """
# run_js(jscode_)  # 날짜 선택


jscode_ = """
document.querySelector("#aform > div.dt_top_box > div.con_box > div > div > a.common_btn.blue").click()
"""
run_js(jscode_) #예약
###################################################

###################################################
schedule = '1'
valid = False
while not valid:
    try:
        date_element = driver.find_element(By.ID, 'div_cal_' + date)
        date_element.click()
        jscode_ = f"""
        document.querySelector("#unit{schedule} > a").click()
        """
        run_js(jscode_)
        valid = True 
    except Exception as e:
        print('no element found')
        driver.refresh()
        time.sleep(1) 


jscode_ = """
$("#person").val(1)
"""
run_js(jscode_)

jscode_ = """
addItem1.value = '동의'
"""
run_js(jscode_)

# recaptcha_data = 
# jscode_ = f'$("#g-recaptcha-response").val("{recaptcha_data}")'
recapchar_param = '&response=03AFcWeA6cHiOePLPNJKa3b2U_i_n98fXGb-n0P2EqyCRbe_8KfXl_Atd-JXQvA7obRCsfpj91KLKjgcq4WH_rZTj3mrrpHrpKBsZvdgGLtSzLtIH9HJ62uDQm-xovz5iZ426QxeI3M47FP3fxuOyE19SoQ-Py2hhS_LV1jHpKHlByCPjgCABwKlryVOybP4w6BzgSNrs-HE1cEvLV6IG98r6VrdMhdjzsjyGfJnG93m691l8KYClPZCWZKfAbNMHGIPNdzjMQ3rdKlYHjA1i76DuwZa28UJ5zOLYZO8kLp5xLlEsNlBvWWge85wEA4UQH_ScRp1_8CCVmZgM00jdizRtPfkwIKdhKrHq4YS-b8p_fW7Y7xAhpcCc_mOiLAj20uBk6Xwe0tI1cBqBhhgZEe17PB_EqG3bknz8zhW0ACmETjkXIrGVVPDsnijSeO16ubI5O0iTin9vqV563z6lz24_yd0PGJU-3m8ryLfQ3D8dksIbQaoyL1Usix9U6VNYuRUbluG3890Yom5aXaIwq_wbGvFzoz-l7JUFTt6sQI0e4dOT9Xc7pc7oJ9MvHQHlGNbH_3Y8pTLo8FMtqplvth1MpNTm36UsbNQMVtGUIyR42vdhhFnOkSHIdwhlHJX5ByUiTwnr9i2JpmYn26BKxTk3gw84grpOAxZkA2zvnq-4rM81daPKxTece1rJQKvop9wbt46YGQ0Cnp8pXLdRikIxupECoS7Csz2Uuv3fXk8tO1ykWsVqWUmKQkY8RIoLCFFNDP2Mw5bjOX2qXUVi0dQOahjRmatU4Wt5mqaqnyeNkk2nnYYIcW0R-E-auspvDVYbublsjIrBPB_CjqLl-35TfEgXpYf71aP7h0h1LzTBO-L730XD8cQ6eGEHCD6U7aAPNrxnS0jXv'
jscode_ = f"""
paramCaptcha = '{recapchar_param}';
"""
run_js(jscode_)


jscode_ = """
$("[name=chk_agree1]").prop("checked",true)
"""
run_js(jscode_)

time.sleep(10000)
jscode_ = """
$("#aform").attr({action:"/web/reservation/insertReservReceipt.do", method:'post'}).submit();
"""
run_js(jscode_)
###################################################

