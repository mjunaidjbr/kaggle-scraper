# Importing the libraries 
import os
import time
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import warnings
#ignore warnings of depricated warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from defaults import *
import logging
#save the logs in a file
LOG_FILE_NAME = "links_scrapping_logs.log"

#constants for the script
#class name for the a tags in the page
# A_TAGS_CLASS_NAME = "sc-GJyyB hmKQqM"
# AUTHOR_CLASS_NAME = "sc-hhGHuG sc-gXSCqU iIhleq fyPHTK"
# TITLE_CLASS_NAME = "sc-iAEyYk sc-fsQiph sc-pTqjN bhyXVy feJEwm lcZWRG"
# SUB_TITLE_CLASS_NAME = "sc-fLQRDB sc-bALXmG sc-hMRyxU kPbSkA JDLpp dZNkES"
# DATASET_DESCRIPTION_CLASS_NAME = "sc-dmLtQE jWwnsR"
# LICENSE_CLASS_NAME = "sc-dKfzgJ sc-hIqOWS sc-eiwPGB jQQULV dclpAt eTlxRD"
# TAGS_CLASS_NAME = "sc-hJGKTP dzaWn"

#logging configuration
logging.basicConfig(filename=LOG_FILE_NAME, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s',force=True)

logging.info("Starting the script to scrape the links")

#text file
TEXT_FILE_NAME = "links.txt"

#create a text file to store the links
open(TEXT_FILE_NAME, "w").close()

#importing the local database functions file
from database_functions import add_record,check_url_present,local_session

#some Constants 
#path to the folder where you want to save the files
#script location real 
CWD = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FOLDER_NAME = "datasets"
OUTPUT_FOLDER = os.path.join(CWD, OUTPUT_FOLDER_NAME)
TMP_FOLDER = os.path.join(OUTPUT_FOLDER, "tmp")



#check if the OUTPUT_FOLDER exists or not if not create it
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

#check if the TMP_FOLDER exists or not if not create it
if not os.path.exists(TMP_FOLDER):
    os.makedirs(TMP_FOLDER)


#initializing the chrome driver 

#driver in headless mode
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)



#set driver download path 
# setting the download path 
driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': TMP_FOLDER}}
command_result = driver.execute("send_command", params)


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
    logging.error("Please enter your email and password in the script.py file")
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
time.sleep(5)


# Scrape the page
mainUrl = "https://www.kaggle.com/datasets?page="

#list of links for all pages
listOfDataSetsLinks = []
numberOfPages = input("Enter the number of pages you want to scrape: ")
startPage = input("Enter the start page: ")
for page_num in range(int(startPage), (int(numberOfPages) + int(startPage))):
    # print(f"Scraping page {page_num}")
    logging.info(f"Scraping page {page_num}")
    if page_num % 2 == 0:
        driver.quit()
        
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)



        #set driver download path 
        # setting the download path 
        driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': TMP_FOLDER}}
        command_result = driver.execute("send_command", params)


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
            logging.error("Please enter your email and password in the {os.path.basename(__file__)} file")
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
        time.sleep(5)

    
    #list of links for each page
    linksDatasetPage = []
    
    # Create the full url
    fullUrl = mainUrl + str(page_num)
    try:
        # Go to the page you want to scrape
        driver.get(fullUrl)
        # Wait for the page to load
        time.sleep(5)
        # Get the page source
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # scrape page logic here
        #get the table 

        # ul and class = km-list km-list--three-line
        data_ul = soup.find('ul', class_ = "km-list km-list--three-line")

        #get all a tags class = sc-csvncw fmIQhT
   
        data_a = data_ul.find_all('a', class_ = A_TAGS_CLASS_NAME , href=True)
    
        a_tags = [a.get('href') for a in data_a]
        linksDatasetPage = ["https://www.kaggle.com" + a  for a in a_tags]
        # print("list of links:", linksDatasetPage)

        #write the links to a file
        with open(TEXT_FILE_NAME, "a") as f:
            for link in linksDatasetPage:
                f.write(link + "\n" )

        #add the links to the listOfDataSetsLinks list
        listOfDataSetsLinks.extend(linksDatasetPage)

    except Exception as e:
        # print(f"Error occured while scraping the page {fullUrl}")
        logging.error(f"Error occured while scraping the page {fullUrl}")
        logging.error(f"Error: {e}")
        raise e

        # continue 

logging.info(f"Scraping of {numberOfPages} pages from {startPage} to {int(numberOfPages) + int(startPage)} page number completed successfully")
