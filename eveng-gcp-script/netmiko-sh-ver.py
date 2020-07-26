#!/usr/bin/env python
from netmiko import ConnectHandler
import re
r1 = {
'device_type': 'cisco_ios',
'host': '192.168.255.14',
'username': 'cisco',
'password': 'cisco',
'port': '22'
}

net_connect = ConnectHandler(**r1)
output = net_connect.send_command('',expect_string=r'#',strip_command=False, strip_prompt=False)
output += net_connect.send_command('show version',expect_string=r'#',strip_command=False, strip_prompt=False)
net_connect.disconnect()

IOS_RE = r'(Cisco IOS\s+(\S+\s+.*))'        
matched = re.findall(IOS_RE,output)
print(matched[0][0])

#print(output)