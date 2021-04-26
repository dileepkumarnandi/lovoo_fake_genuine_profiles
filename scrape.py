


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import requests
import time
import json
import pickle
import pandas as pd
import urllib.request

city_dict = pickle.load(open('city_dict.pkl','rb'))

list1=[]
image_url_list=[]
username_list=[]

def get_username(json):
    try:
        return json['name']
    except KeyError:
        return None

def get_gender(json):
    try:
        return json['gender']
    except KeyError:
        return None
    
def get_age(json):
    try:
        return json['age']
    except KeyError:
        return None
def get_freetext(json):
    try:
        return json['freetext']
    except KeyError:
        return None

def get_subscriptions(json):
    try:
        return json['subscriptions']
    except KeyError:
        return None

def get_isVip(json):
    try:
        return json['isVip']
    except KeyError:
        return None

def get_flirtInterests(json):
    try:
        return json['flirtInterests']
    except KeyError:
        return None
    
def get_counts(json):
    try:
        return json['counts']
    except KeyError:
        return None
def get_locations(json):
    try:
        return json['locations']
    except KeyError:
        return None
def get_isNew(json):
    try:
        return json['isNew']
    except KeyError:
        return None
def get_isOnline(json):
    try:
        return json['isOnline']
    except KeyError:
        return None
def get_isMobile(json):
    try:
        return json['isMobile']
    except KeyError:
        return None
def get_isHighlighted(json):
    try:
        return json['isHighlighted']
    except KeyError:
        return None
def get_picture(json):
    try:
        return json['picture']
    except KeyError:
        return None
def get_images(json):
    try:
        return json['images']
    except KeyError:
        return None
def get_isVerified(json):
    try:
        return json['isVerified']
    except KeyError:
        return None
def get_verifications(json):
    try:
        return json['verifications']
    except KeyError:
        return None

def login(user, pw):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome('C:/Users/Ganesh/Downloads/chromedriver.exe',options=chrome_options)
    driver.get("https://www.lovoo.com")
    user_agent = driver.execute_script("return navigator.userAgent;")
    time.sleep(4)
    iframe = driver.find_element(By.ID,"gdpr-consent-notice")
    driver.switch_to.frame(iframe)
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[id='save']"))).click()
    driver.switch_to.default_content()
    login = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-automation-id='login-button']"))).click()
    s=requests.Session()
    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='authEmail']")))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='authPassword']")))
    username.clear()
    username.send_keys(user)
    password.clear()
    password.send_keys(pw)
    login = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-automation-id='login-submit-button']"))).click()
    time.sleep(10)
    '''
    all_spans = driver.find_elements_by_xpath("//div[@class='full-width user-image user-userpic']")
    print(all_spans)
    for span in all_spans:
        if span.is_displayed():
        #time.sleep(2)
            span.click()
    '''
    
    driver.get('https://www.lovoo.com/api_web.php/users')
    time.sleep(10)
    members = driver.page_source
    members = members[84:-20]
    users = json.loads(members)
    
    
    for user in users['response']['result']:
        userinfo = {'username': get_username(user), 'gender': get_gender(user),'age':get_age(user), 'freetext': get_freetext(user), 'subscriptions':get_subscriptions(user),
        'isVip': get_isVip(user),'flirtInterests':get_flirtInterests(user), 'counts' : get_counts(user),'locations':get_locations(user),'isNew':get_isNew(user),
        'isOnline':get_isOnline(user),'isMobile':get_isMobile(user),'isHighlighted':get_isHighlighted(user),
        'picture':get_picture(user),'images' : get_images(user),
        'isVerified':get_isVerified(user),'verifications':get_verifications(user)
        }


        for fi in userinfo['flirtInterests']:
            if 'chat' in fi:
                userinfo['flirtInterests_chat'] =1
            else:
                userinfo['flirtInterests_chat'] =0
            if 'date' in fi:
                userinfo['flirtInterests_date'] =1
            else:
                userinfo['flirtInterests_date'] =0
            if 'friends' in fi:
                userinfo['flirtInterests_friends'] =1
            else:
                userinfo['flirtInterests_friends'] =0

        userinfo['city'] = userinfo['locations']['current']['city']
        userinfo['distance'] = userinfo['locations']['current']['distance'] 

        dataframe={}
        dataframe['age'] = userinfo['age']
        dataframe['flirtInterests_chat'] = userinfo['flirtInterests_chat']
        dataframe['flirtInterests_friends'] = userinfo['flirtInterests_friends']
        dataframe['flirtInterests_date'] = userinfo['flirtInterests_date']
        dataframe['isVip'] = userinfo['isVip']
        dataframe['isVerified'] = userinfo['isVerified']

        dataframe['city'] = userinfo['city']


        if dataframe['city'] in city_dict:
            dataframe['city'] = city_dict[dataframe['city']]
        else:
            city_dict[dataframe['city']]=len(city_dict)+1
            dataframe['city'] = city_dict[dataframe['city']]
            pickle.dump(city_dict, open('city_dict.pkl','wb'),protocol=2)
        
        dataframe['highlighted'] = userinfo['isHighlighted']
        dataframe['distance'] = userinfo['distance']
        dataframe['mobile'] = userinfo['isMobile']
        dataframe['online'] = userinfo['isOnline']

        image_url_list.append(userinfo['images'][0]['url'])
        username_list.append(userinfo['username'])

        list1.append(dataframe)
        #df=pd.dataframe(dataframe,index=[0])

        #print(dataframe) 
        #print()
        #print()
    df=pd.DataFrame(list1)
    #print(df.info())


    
    return df
'''   
def main():
    user_agent, cookies = login(credentials[0], credentials[1])

if __name__=="__main__":
    main()
'''

