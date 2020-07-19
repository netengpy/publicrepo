#!/usr/bin/env python3.8

from netmiko import ConnectHandler
import requests
import sys

# r1 = {'name': 'R1', 'connect': {'ip': '192.168.131.131', 'username': 'cisco', 'password': 'cisco', 'device_type': 'cisco_ios','global_delay_factor': 2,}}
# r2 = {'name': 'R2', 'connect': {'ip': '192.168.131.132', 'username': 'cisco', 'password': 'cisco', 'device_type': 'cisco_ios','global_delay_factor': 2,}}
# r3 = {'name': 'R3', 'connect': {'ip': '192.168.24.131', 'username': 'cisco', 'password': 'cisco', 'device_type': 'cisco_ios','global_delay_factor': 2,}}
# r4 = {'name': 'R4', 'connect': {'ip': '192.168.24.132', 'username': 'cisco', 'password': 'cisco', 'device_type': 'cisco_ios','global_delay_factor': 2,}}
# r5 = {'name': 'R5', 'connect': {'ip': '192.168.24.133', 'username': 'cisco', 'password': 'cisco', 'device_type': 'cisco_ios','global_delay_factor': 2,}}
# r6 = {'name': 'R6', 'connect': {'ip': '192.168.24.134', 'username': 'cisco', 'password': 'cisco', 'device_type': 'cisco_ios','global_delay_factor': 2,}}
# r7 = {'name': 'R7', 'connect': {'ip': '192.168.24.135', 'username': 'cisco', 'password': 'cisco', 'device_type': 'cisco_ios','global_delay_factor': 2,}}
# r8 = {'name': 'R8', 'connect': {'ip': '192.168.24.136', 'username': 'cisco', 'password': 'cisco', 'device_type': 'cisco_ios','global_delay_factor': 2,}}
# r9 = {'name': 'R9', 'connect': {'ip': '192.168.24.137', 'username': 'cisco', 'password': 'cisco', 'device_type': 'cisco_ios','global_delay_factor': 2,}}
# r10 = {'name': 'R10', 'connect': {'ip': '192.168.24.138', 'username': 'cisco', 'password': 'cisco', 'device_type': 'cisco_ios','global_delay_factor': 2,}}

# devices = [r1,r2,r3,r4,r5,r6,r7,r8,r9,r10]

username = 'cisco'
password = 'cisco'
device_type ='cisco_ios'

with open("ip.txt","r") as f:
    devices = f.readlines()

#printed on webpage
print("DEBUG_INFO",str(sys.argv))
#baseurl = input("URL to configs: ")
baseurl = "http://172.23.188.45/{}/".format(sys.argv[1])
print(baseurl)
for device in devices:
    device = device.strip('\n').split(' ')
    exist_check = requests.get(baseurl + device[0] + '.txt')
    if exist_check.status_code == 200:
        print()
        print('Connecting to {} {}'.format(device[0], device[1]))
        
        # net_connect = ConnectHandler(**device['connect'])
        net_connect = ConnectHandler(ip=device[1], 
                                     device_type=device_type,
                                     username=username,
                                     password=password,
                                     global_delay_factor=2)
        net_connect.config_mode()
        print('Connected to {}'.format(device[0]))
        
        #R1(config)#file prompt ?
        #  alert  Prompt only for destructive file operations
        #  noisy  Confirm all file operation parameters
        #  quiet  Seldom prompt for file operations
        #  <cr>

        net_connect.send_command('file prompt quiet')
        net_connect.exit_config_mode()
        output = net_connect.send_command('\n', expect_string=r'#')
        print('Copying {}.txt from http server to {}'.format(device[0],device[1]))
        output += net_connect.send_command('copy ' + baseurl + device[0] + '.txt running' , expect_string=r'#')
        print(output)
        net_connect.disconnect()
    else:
        print('Device config not available, {}'.format(device[0]))
