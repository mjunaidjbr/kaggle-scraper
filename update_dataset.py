import os
from defaults import *
import time
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from database_functions import add_record,check_url_present,local_session,get_data_from_id

#get the input from user
number_of_datasets = int(input("Number of datasets to process: "))
start_number = int(input("start id number of dataset: "))

#login 
#driver in headless mode
options = Options()
options.headless = True
# options.add_argument('--disable-auto-close')
driver = webdriver.Chrome(options=options)


# Login to Kaggle 
# email 
email = "nogew43062@kaudat.com"
# password 
password = "kagglepassword"

#username
# username = "kaudatunique"

#check if the email and password are not empty 
if email == None or password == None:
    # print("Please enter your email and password in the script.py file")
    print("Please enter your email and password in the script.py file")
    exit()
    

signInUrl = "https://www.kaggle.com/account/login?phase=emailSignIn" 
driver.get(signInUrl)
emailXPath = "/html/body/main/div[1]/div/div[4]/div[2]/form/div[2]/div[1]/div/label/input" 
email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, emailXPath)))
email_input.send_keys(email)
passwordXPath = "/html/body/main/div[1]/div/div[4]/div[2]/form/div[2]/div[2]/div/label/input"
password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, passwordXPath)))
password_input.send_keys(password)
signInXPath = "/html/body/main/div[1]/div/div[4]/div[2]/form/div[2]/div[3]/button/span"
signInButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, signInXPath)))
signInButton.click()
time.sleep(15)



for i in range(start_number, (number_of_datasets+1)):

    # print(get_url_from_id(local_session,1))
    try:
        row = get_data_from_id(local_session,i)
    except:
        print(f"datasets successfully updated from id {str(start_number)} to {str(i)}")

    #initializing the chrome driver 
    if i%5 == 0:
        #driver in headless mode
        options = Options()
        options.headless = True
        # options.add_argument('--disable-auto-close')
        driver = webdriver.Chrome(options=options)


        # Login to Kaggle 
        # email 
        email = "nogew43062@kaudat.com"
        # password 
        password = "kagglepassword"

        #username
        # username = "kaudatunique"

        #check if the email and password are not empty 
        if email == None or password == None:
            # print("Please enter your email and password in the script.py file")
            print("Please enter your email and password in the script.py file")
            exit()
            

        signInUrl = "https://www.kaggle.com/account/login?phase=emailSignIn" 
        driver.get(signInUrl)
        emailXPath = "/html/body/main/div[1]/div/div[4]/div[2]/form/div[2]/div[1]/div/label/input" 
        email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, emailXPath)))
        email_input.send_keys(email)
        passwordXPath = "/html/body/main/div[1]/div/div[4]/div[2]/form/div[2]/div[2]/div/label/input"
        password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, passwordXPath)))
        password_input.send_keys(password)
        signInXPath = "/html/body/main/div[1]/div/div[4]/div[2]/form/div[2]/div[3]/button/span"
        signInButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, signInXPath)))
        signInButton.click()
        time.sleep(15)

    # url="https://www.kaggle.com/datasets/gayu14/tv-and-movie-metadata-with-genres-and-ratings-imbd"
    url = str(row.url)

    driver.get(url)
    time.sleep(10)

    page_soup = BeautifulSoup(driver.page_source, 'html.parser')




    #title
    #get the dataset title
    try:
        title = page_soup.find('h1', class_ = TITLE_CLASS_NAME)
        title = title.text
    except:
        title = ""

    #sub_title
    #get the dataset sub title
    try:
        sub_title = page_soup.find('span', class_ = SUB_TITLE_CLASS_NAME)
        sub_title = sub_title.text
    except:
        sub_title = ""
        
    #author_name
    #get the author name of the dataset
    try:
        author_name = page_soup.find('span', class_ = AUTHOR_CLASS_NAME)
        if " and " in author_name.text:
            author_name = author_name.text.split(" and ")[0]
        else:
            author_name = author_name.text
    except:
        author_name = ""

    #description

    try:
        description = page_soup.find('div',text='About Dataset')
        description = description.find_next_sibling('div')
        description = description.text
    except:
        description = ""

    #license
    license = page_soup.find('h2', text="License")
    try:
        license = license.find_next_sibling('p')
        license = license.text
    except:
        license = ""



    #tags
    tags = page_soup.find('h2', text="Tags")
    try:
        tags = tags.find_next_sibling('div')
        tags = tags.find_all('span')
        tags = [tag.text for tag in tags]
        tags = ",".join(tags)
    except:
        tags = ""

    # print("title:",title)
    # print("sub_title",sub_title)
    # print("Author:",author_name)
    # print("Description:", description)
    # print("License:", license)
    # print("Tags:", tags)

    row.title = title
    row.sub_title = sub_title
    row.author_name = author_name
    row.about_dataset = description
    row.license = license
    row.tags = tags

    local_session.commit()
    print(f"Row with id {str(i)} has been updated")