#!/usr/bin/python3
import selenium

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

import time

url = 'http://www.ip8.com/'
# url = 'https://ipecho.net/plain'
# url='http://free-proxy.cz/en/ipinfo'
#to check ip address
# url = 'https://www.whatismyip.com/'

from seleniumwire import webdriver
#175.107.255.39
# 159.203.61.169:8080
# options = {
#     'proxy': {
#         'http': 'http://myusername:password@myproxyserver.com:123456', 
#         'https': 'http://myusername:password@myproxyserver.com:123456',
#         'no_proxy': 'localhost,127.0.0.1' # excludes
#     }  
# }
#socks5
# proxy="5.161.125.70:8080"
# proxy=input("Enter proxy(ip:port):")
proxy="120.46.197.14:8083"
options1 = {
    'proxy': {
        'http': f"http://{proxy}",
        'https': f"http://{proxy}",
        'no_proxy': 'localhost,127.0.0.1' # excludes
    }
}
#socks5
# 199.229.254.129:4145
# options1 = {
#     'proxy': {
#         'http': f"socks5://{proxy}",
#         'https': f"socks5://{proxy}",
#         'no_proxy': 'localhost,127.0.0.1' # excludes
#     }
# }
options= webdriver.ChromeOptions()
# options.headless = True
driver = webdriver.Chrome(ChromeDriverManager().install(),options=options, seleniumwire_options=options1)

driver.get(url=url)

time.sleep(10)

print(driver.page_source)
time.sleep(10)