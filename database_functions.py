from database_initialize import engine, Record, session

local_session = session(bind=engine)
#add a record to the database
def add_record(local_session,url, download_link, base_folder_path, path, author_name, title, sub_title, about_dataset, license, tags):
    new_record = Record(url=url, download_link=download_link, base_folder_path=base_folder_path, path=path, author_name=author_name, title=title, sub_title=sub_title, about_dataset=about_dataset, license=license, tags=tags)
    local_session.add(new_record)
    local_session.commit()

#call the function to add a record to the database of kaggle datasets
# add_record(url="https://www.kaggle.com/datasets/ulrikthygepedersen/co2-emissions-by-country",
# download_link="https://www.kaggle.com/ulrikthygepedersen/co2-emissions-by-country/download",
# base_folder_path="/home/ulrik/Downloads",
# path="/home/ulrik/Downloads/co2-emissions-by-country.zip",
# author_name="Ulrik Thyge Pedersen",
# title="CO2 emissions by country",
# sub_title="CO2 emissions by country",
# about_dataset="CO2 emissions by country",
# license="CC0: Public Domain",
# tags="co2, emissions, country")

#function check url present in database
def check_url_present(local_session,url):
    if local_session.query(Record).filter(Record.url == url).count() > 0:
        return True
    else:
        return False
    
