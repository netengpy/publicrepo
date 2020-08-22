#!/usr/bin/env python

'''
Author - omz
29-07-2020
'''

import argparse
import os
import requests
import sys
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def main():
    # Replace url for vManage
    baseurl = 'https://192.168.1.1'
    url = baseurl + '/j_security_check'

    # Replace User and Password
    data = {"j_username" : "admin", "j_password" : "admin"}
    sess = requests.session()
    response = sess.post(url=url, data=data, verify=False)

    if response.status_code !=  200:
        print('Login Failed ')
        sys.exit(0)

##################################################################     
### Create a specific feature template in the templates folder ###
##################################################################

#    with open('templates/' + jsonfile) as f:
#        data = f.read()
#        data = json.loads(data)
#
#    # vManage API URL for feature templates 
#    url = baseurl + '/dataservice/template/feature'
#    response = sess.post(url=url, json=data, verify=False)
#    if response.status_code !=  200:
#        print('Create FeatureTemplates Failed. Status code = ' + str(response.status_code) )
#        print(response.text)
#        sys.exit(0)
#    else:
#        print('Template '+args.filejson+' succesfully deployed to vManage')
#        print()

########################################################        
### Create all feature templates in the given folder ###
########################################################

    templates = os.listdir('Custom_FeatureTemplates/vEdge/')
    #templates = os.listdir('Generic_vEdge_FeatureTemplates/')

    # vManage API URL for feature templates 
    url = baseurl +'/dataservice/template/feature'
    for template in templates:
        print(template)
        f = open('Custom_FeatureTemplates/vEdge/' + template)
        #f = open('Generic_vEdge_FeatureTemplates/' + template)
        data = f.read()
        data = json.loads(data)
        response = sess.post(url=url, json=data, verify=False)
        if response.status_code != 200:
            print('Create FeatureTemplates Failed. Status code = ' + str(response.status_code))
        else:
            print('Successfully loaded {}\n'.format(template))

if __name__ == '__main__':
    parser = argparse.ArgumentParser('template parser')
    #parser.add_argument('-h', action="store", dest="hostname", help="Enter vManage IP Address.")
    parser.add_argument('-f', action="store", dest="filejson", help="Enter json file for template.")
    args = parser.parse_args()
    #host = args.hostname
    jsonfile = args.filejson
    main()




