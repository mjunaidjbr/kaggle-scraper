# Importing the libraries 
import os
import time
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

#constants for the script
#class name for the a tags in the page
A_TAGS_CLASS_NAME = "sc-crPCXo kMbriS"
AUTHOR_CLASS_NAME = "sc-hhGHuG sc-gXSCqU iIhleq fyPHTK"
TITLE_CLASS_NAME = "sc-iAEyYk sc-fsQiph sc-flFvMs bhyXVy feJEwm fnpKTf"
SUB_TITLE_CLASS_NAME = "sc-fLQRDB sc-bALXmG sc-ivSfqT kPbSkA JDLpp jpsCju"
DATASET_DESCRIPTION_CLASS_NAME = "sc-hjzGtE irsToa"
LICENSE_CLASS_NAME = "sc-dKfzgJ sc-hIqOWS sc-hSMeCy jQQULV dclpAt dJIfeo"

TAGS_CLASS_NAME = "sc-exfGlw iHaITa"

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
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)



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
time.sleep(5)


# Scrape the page
mainUrl = "https://www.kaggle.com/datasets?page="

#list of links for all pages
listOfDataSetsLinks = []

for page_num in range(1, 501):

    if page_num % 2 == 0:
        driver.quit()
        print(f"Scraping page {page_num}")
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)



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

        #add the links to the listOfDataSetsLinks list
        listOfDataSetsLinks.extend(linksDatasetPage)

    except Exception as e:
        print(f"Error occured while scraping the page {fullUrl}")
        raise e
        # continue 

        

    # Download the files       
    for i in linksDatasetPage:
        try:
            if i == "https://www.kaggle.com/datasets/dschettler8845/diffusiondb-2m-part-0001-to-0100-of-2000":
                print("skipping")
                continue
            #check if the url is already present in the database or not 
            #if present then skip it
            if check_url_present(local_session=local_session, url=i):
                print(f"URL {i} is already present in the database")
                continue 

            dataset_download_link = i + "/download"
            driver.get(i)
            time.sleep(5)
            page_soup = BeautifulSoup(driver.page_source, 'html.parser')

            #get the author name of the dataset
            author_name = page_soup.find('span', class_ = AUTHOR_CLASS_NAME)
            if " and " in author_name.text:
                author_name = author_name.text.split(" and ")[0]
            else:
                author_name = author_name.text

            #get the dataset title
            
            title = page_soup.find('h1', class_ = TITLE_CLASS_NAME)
            title = title.text
            #get the dataset sub title
            
            sub_title = page_soup.find('span', class_ = SUB_TITLE_CLASS_NAME)
            sub_title = sub_title.text

            #get the dataset description
            
            dataset_description = page_soup.find('div', class_ = DATASET_DESCRIPTION_CLASS_NAME)
            dataset_description = dataset_description.text

            #get the dataset license
            
            # license_ =  page_soup.find('p', class_ = LICENSE_CLASS_NAME)
            # license_ = license_.text
            license_ = "None"

            #get dataset tags
            
            tags_ = page_soup.find_all('button', class_ = TAGS_CLASS_NAME)
            tags_ = [tag.text for tag in tags_]
            #, separated string
            tags_ = ",".join(tags_)

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
            driver.get(dataset_download_link)
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

            #insert the data into the database
            try:
                add_record(local_session=local_session, url=str(i), download_link=str(dataset_download_link), base_folder_path=str(OUTPUT_FOLDER), path=str(path_of_zip_file), author_name=str(author_name), title=str(title), sub_title=str(sub_title), about_dataset=str(dataset_description), license=str(license_), tags=str(tags_) )
            except Exception as e:
                print("failed to insert record into the database: ", e)
                raise e
                # continue

        except Exception as e:
            print(f"failed to download the dataset: {i}" , e)
            raise e
            continue
    






        









