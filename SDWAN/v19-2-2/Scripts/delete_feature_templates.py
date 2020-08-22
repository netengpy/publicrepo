#!/usr/bin/env python

'''
Author - omz
29-07-2020
'''

import requests
import sys

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Replace url for vManage
baseurl = 'https://192.168.1.1'
url = baseurl + '/j_security_check'

# Replace User and Password
data = {"j_username" : "admin", "j_password" : "admin"}
sess = requests.session()
response = sess.post(url=url, data=data, verify=False)

if response.status_code !=  200:
	print('Login Failed')
	sys.exit(0)

# vManage API URL for feature templates 
url = baseurl + '/dataservice/template/feature'

response = sess.get(url=url, verify=False)
list_ids = []
data = response.json()
for item in data['data']:
    if item['factoryDefault'] != True:

# Create list of non-default templates ids
        list_ids.append(item['templateId'])
if list_ids == []:
    print('There are no custom feature Templates to delete.')
    sys.exit('No Templates')

confirm = input('Do you want to delete ALL custom Feature Templates? Y or N ')
if confirm.lower() == 'y':
    print('The following templates will be deleted.\n')
    for item in data['data']:
        if item['factoryDefault'] != True:
            print(item['templateName'])
    confirm_again = input('\nConfirm again, delete all the custom Feature Templates? Y or N ')
    if confirm_again.lower() == 'y':
        for item in list_ids:
            response = sess.delete(url=url + '/' + item)
            print(response.status_code)


