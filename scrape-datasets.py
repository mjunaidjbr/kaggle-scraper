# Importing the libraries 
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
import logging
import warnings
#ignore deprecation warnings 
warnings.filterwarnings("ignore", category=DeprecationWarning)



#code for blacklisting the urls
#blacklist urls
#check blacklist file exists or not
BLACKLIST_FILE_NAME = "blacklist.txt"
if os.path.exists(BLACKLIST_FILE_NAME):
    with open(BLACKLIST_FILE_NAME, 'r') as f:
        blacklist = f.read().splitlines()
    logging.info(f"blacklist urls are {blacklist}")
else:
    blacklist = []











#save the logs in a file
LOG_FILE_NAME = "data_scrapping_logs.log"
# Set the logging configuration
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#to save the logs in a file
logging.basicConfig(filename=LOG_FILE_NAME, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',force=True)


logging.info("program started to scrape the data from the links")
# #constants for the script
# #class name for the a tags in the page
# A_TAGS_CLASS_NAME = "sc-GJyyB hmKQqM"
# AUTHOR_CLASS_NAME = "sc-hhGHuG sc-gXSCqU iIhleq fyPHTK"
# TITLE_CLASS_NAME = "sc-iAEyYk sc-fsQiph sc-pTqjN bhyXVy feJEwm lcZWRG"
# SUB_TITLE_CLASS_NAME = "sc-fLQRDB sc-bALXmG sc-hMRyxU kPbSkA JDLpp dZNkES"
# DATASET_DESCRIPTION_CLASS_NAME = "sc-dmLtQE jWwnsR"
# LICENSE_CLASS_NAME = "sc-dKfzgJ sc-hIqOWS sc-eiwPGB jQQULV dclpAt eTlxRD"
# TAGS_CLASS_NAME = "sc-hJGKTP dzaWn"
#importing the local database functions file
from database_functions import add_record,check_url_present,local_session

#some Constants 
#path to the folder where you want to save the files
#script location real 
CWD = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FOLDER_NAME = "datasets"
OUTPUT_FOLDER = os.path.join(CWD, OUTPUT_FOLDER_NAME)
TMP_FOLDER = os.path.join(OUTPUT_FOLDER, "tmp")
INPUT_FILE_NAME = "links.txt"
SUCCESS_FILE_NAME = "success.txt"
ERROR_FILE_NAME = "error.txt"

#check input file exists or not
if not os.path.exists(INPUT_FILE_NAME):
    # print(f"Input file {INPUT_FILE_NAME} does not exists")
    logging.error(f"Input file {INPUT_FILE_NAME} does not exists")
    exit()

#create the success and error file
open(SUCCESS_FILE_NAME, "w").close()
open(ERROR_FILE_NAME, "w").close()



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

# emailXPath = "/html/body/main/div[1]/div/div[4]/div[2]/form/div[2]/div[1]/div/label/input" 
email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, emailXPath)))
email_input.send_keys(email)
# passwordXPath = "/html/body/main/div[1]/div/div[4]/div[2]/form/div[2]/div[2]/div/label/input"
password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, passwordXPath)))
password_input.send_keys(password)
# signInXPath = "/html/body/main/div[1]/div/div[4]/div[2]/form/div[2]/div[3]/button/span"
signInButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, signInXPath)))
signInButton.click()
time.sleep(15)


# Scrape the page
mainUrl = "https://www.kaggle.com/datasets?page="

#list of links for all pages
listOfDataSetsLinks = []

linksDatasetPage = []

#get the data from the links.txt file
with open(INPUT_FILE_NAME, 'r') as f:
    linksDatasetPage = f.readlines()
    linksDatasetPage = [x.strip() for x in linksDatasetPage]
    #remove the elements that are in blacklist from linksDatasetPage
    linksDatasetPage = [x for x in linksDatasetPage if x not in blacklist]


        

# Download the files       
for val,i in enumerate(linksDatasetPage, start=1):
    # print("###################################")
    # print("processing link:", i)
    logging.info("processing link: %s", i)
    # print("###################################")
    try:
        if val % 5 == 0:
            driver.quit()
            # print(f"Scraping page {page_num}")
            options = Options()
            options.headless = True
            # PROXY="167.71.241.136:33299"
            # options.add_argument('--proxy-server=%s' % PROXY)
            driver = webdriver.Chrome( options=options)



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
            # emailXPath = "/html/body/main/div[1]/div/div[4]/div[2]/form/div[2]/div[1]/div/label/input" 
            email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, emailXPath)))
            email_input.send_keys(email)
            # passwordXPath = "/html/body/main/div[1]/div/div[4]/div[2]/form/div[2]/div[2]/div/label/input"
            password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, passwordXPath)))
            password_input.send_keys(password)
            # signInXPath = "/html/body/main/div[1]/div/div[4]/div[2]/form/div[2]/div[3]/button/span"
            signInButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, signInXPath)))
            signInButton.click()
            time.sleep(5)
        # if i == "https://www.kaggle.com/datasets/dschettler8845/diffusiondb-2m-part-0001-to-0100-of-2000":
        #     print("skipping")
        #     continue
        #check if the url is already present in the database or not 
        #if present then skip it
        if check_url_present(local_session=local_session, url=i):
            # print(f"URL {i} is already present in the database")
            logging.info("URL %s is already present in the database", i)
            continue 

        dataset_download_link = i + "/download"
        driver.get(i)
        time.sleep(5)
        #check the download button is present or not
        try:
            # download_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/main/div[1]/div/div[6]/div[2]/div/div[2]/div[1]/div/a/button")))
            #clickable
            download_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[1]/div/div[6]/div[2]/div/div[2]/div[1]/div/a/button")))
        except Exception as e:
            # print("download button not present")
            logging.error("download button not present in the link: %s", i)
            #also except the error in the error file
            logging.error("exception: %s", e)
            #paste the link to error file
            #append the link to blacklist file
            with open(BLACKLIST_FILE_NAME, "a") as f:
                f.write(i + "\n")
            continue

        time.sleep(5)
        page_soup = BeautifulSoup(driver.page_source, 'html.parser')

        #get the author name of the dataset

        try:
            author_name = page_soup.find('span', class_ = AUTHOR_CLASS_NAME)
            if " and " in author_name.text:
                author_name = author_name.text.split(" and ")[0]
            else:
                author_name = author_name.text
        except:
            author_name = ""

        #get the dataset title
        try:
            title = page_soup.find('h1', class_ = TITLE_CLASS_NAME)
            title = title.text
        except:
            title = ""

        #get the dataset sub title
        try:
            sub_title = page_soup.find('span', class_ = SUB_TITLE_CLASS_NAME)
            sub_title = sub_title.text
        except:
            sub_title = ""


        #get the dataset description
        try:
            dataset_description = page_soup.find('div',text='About Dataset')
            dataset_description = dataset_description.find_next_sibling('div')
            dataset_description = dataset_description.text
        except:
            dataset_description = ""

        #get the dataset license        
        try:
            license_ = page_soup.find('h2', text="License")
            license_ = license_.find_next_sibling('p')
            license_ = license_.text
        except:
            license_ = ""

        #get dataset tags
        try:
            tags_ = page_soup.find('h2', text="Tags")
            tags_ = tags_.find_next_sibling('div')
            tags_ = tags_.find_all('span')
            tags_ = [tag.text for tag in tags_]
            tags_ = ",".join(tags_)
        except:
            tags_ = ""

        # https://www.kaggle.com/datasets/rayhan32/nba-player-status-2003-2023-23k-data
        link_= i.replace("https://www.kaggle.com/datasets/", "")
        link_ = link_.split("/")
        author_folder_name = link_[0]
        dataset_file_name = link_[1]
        full_author_folder_path = os.path.join(OUTPUT_FOLDER, author_folder_name)
        #check if author folder exists if not create it
        if not os.path.exists(full_author_folder_path):
            os.mkdir(full_author_folder_path)
        
        #download the dataset
        # driver.get(dataset_download_link)
        download_button.click()
        #while archive.zip is not downloaded wait
        while not os.path.exists(os.path.join(TMP_FOLDER, "archive.zip")):
            time.sleep(3)

        #move the archive.zip to author folder
        shutil.move(os.path.join(TMP_FOLDER, "archive.zip"), full_author_folder_path)

        #change name of archive.zip to dataset_file_name
        os.rename(os.path.join(full_author_folder_path, "archive.zip"), os.path.join(full_author_folder_path, dataset_file_name + ".zip"))
    

        path_of_zip_file = os.path.join(full_author_folder_path, dataset_file_name + ".zip")
        path_of_zip_file_updated = path_of_zip_file.replace(OUTPUT_FOLDER, "")
        # print("author_name: ", author_name)
        # print("title: ", title)
        # print("sub_title: ", sub_title)
        # print("dataset_description: ", dataset_description)
        # print("license: ", license_)
        # print("tags: ", tags_)
        # print("dataset_download_link: ", dataset_download_link)
        # print("output_folder: ", OUTPUT_FOLDER)
        # print("path_of_zip_file: ", path_of_zip_file)
        # print("path_of_zip_file_updated: ", path_of_zip_file_updated)

        #check tags_ empty or not if empty then set it to None
        if tags_ == "":
            tags_ = "None"
        #check sub_title empty or not if empty then set it to None
        if sub_title == "":
            sub_title = "None"
        #check author_name empty or not if empty then set it to None
        if author_name == "":
            author_name = "None"
        #check license_ empty or not if empty then set it to None
        if license_ == "":
            license_ = "None"
        #check dataset_description empty or not if empty then set it to None
        if dataset_description == "":
            dataset_description = "None"
        #check title empty or not if empty then set it to None
        if title == "":
            title = "None"
        


        #insert the data into the database
        try:
            add_record(local_session=local_session, url=str(i), download_link=str(dataset_download_link), base_folder_path=str(OUTPUT_FOLDER), path=str(path_of_zip_file), author_name=str(author_name), title=str(title), sub_title=str(sub_title), about_dataset=str(dataset_description), license=str(license_), tags=str(tags_) )
        except Exception as e:
            # print("failed to insert record into the database: ", e)
            logging.error("failed to insert record into the database: %s", e)
            #also except the error in the error file
            logging.error("exception: %s", e)

            #roll back the session
            local_session.rollback()

            try:
                #commit the session
                local_session.commit()
            except Exception as e:
                print("failed to commit the session: ", e)
            #paste the link to error file
            with open(ERROR_FILE_NAME, "a") as f:
                f.write(i + "\n")
            # raise e
            continue
        #paste the link to success file
        with open(SUCCESS_FILE_NAME, "a") as f:
            f.write(i + "\n")

    except Exception as e:
        # print(f"failed to download the dataset: {i}" , e)
        logging.error("failed to download the dataset: %s", i)
        #also except the error in the error file
        logging.error("exception: %s", e)
        #paste the link to error file
        with open(ERROR_FILE_NAME, "a") as f:
            f.write(i + "\n")
        # raise e
        continue


    
if driver:
    driver.quit()

logging.info("finished downloading all the datasets")






        









