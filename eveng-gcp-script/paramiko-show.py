#!/usr/bin/env python

import paramiko
import time
import getpass
import os
import sys
 
#IP = '1.1.1.2'
#USER = raw_input("Username : ")
#PASS = getpass.getpass("Password : ")
#ENABLE = getpass.getpass("Enable : ")

# ONLY FOR TESTING. UNCOMMENT ABOVE AND COMMENT BELOW AFTER TESTING
IP = '192.168.255.14'
USER = 'cisco'
PASS = 'cisco'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(IP, port=22, username=USER, password=PASS, look_for_keys=False,allow_agent=False)
remote = ssh.invoke_shell()

# Un-comment below to send enable command if default priv not 15
#remote.send('enable\n')
#remote.send('%s\n' % ENABLE)

remote.send('\n')
remote.send("terminal length 0\n")
remote.send('sh ver\n')
time.sleep(3)
#remote.send('exit')
output = remote.recv(5000)
print(output.decode(encoding='utf-8'))