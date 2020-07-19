import telnetlib
import time
import sys
import requests
from datetime import datetime
import re


def eveng_api():
    data = '{"username":"admin","password":"eve","html5": "-1"}'
    login = requests.post('http://192.168.136.131/api/auth/login', data=data)
    cookies = login.cookies
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'DNT': '1',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'Referer': 'http://192.168.136.131/legacy/',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    # current date and time
    now = datetime.now()
    time_stamp = datetime.timestamp(now) * 1000
    url = 'http://192.168.136.131/api/labs/{}.unl/nodes?_={}'.format(sys.argv[1],int(time_stamp))
    nodes = requests.get(url=url, headers=headers, cookies=cookies)

    data = nodes.json()
    nodes_dict = data["data"]
    #print(nodes_dict)

    device_dict = {}
    for key, value in nodes_dict.items():
        #print(value)
        hostname = value["name"]
        url = value["url"].split(":")
        ip = url[1].replace("//","")
        port = (url[2])
        
        device_dict[key] = hostname, ip, port

    return device_dict


def telnet_conf(hostname, ip, port):
    try:        
        TELNET_TIMEOUT = 5
        READ_TIMEOUT = 5
        
        #Logging into device
        #print(hostname, ip, port)
        conn = telnetlib.Telnet(ip, port, TELNET_TIMEOUT)
       
        #Entering global config mode
        conn.write(b"en\n")
        conn.write(b"terminal length 0\n")
        conn.write(b"configure terminal\n")
        conn.write(b"hostname %b\n" % hostname.encode())
        time.sleep(1)
        
        #Open user selected file for reading
        with open('Int_and_SSH_Config.txt', 'r') as cmd_file:
            #Starting from the beginning of the file
            cmd_file.seek(0)

            #Writing each line in the file to the device
            for cmd in cmd_file.readlines():
                cmd = cmd.strip('\r\n')
                conn.write(cmd.encode() + b'\r')
                time.sleep(.1)
        
        #Closing the conn
        conn.close()
        
    except IOError as error:
        print(error)


def telnet_show_int_ip(ip, port):
    try:        
        TELNET_TIMEOUT = 5
        READ_TIMEOUT = 5
        
        #Logging into device
        #print(ip, port)
        conn = telnetlib.Telnet(ip, port, TELNET_TIMEOUT)
        
        #Entering global config mode
        conn.write(b"\n")
        conn.write(b"sh ip int bri | i Ethernet0/0\n")
        time.sleep(.2)
        
        output = conn.read_very_eager()
        #print(output)
        
        #Closing the conn
        conn.close()
        
    except IOError as error:
        print(error)
    return output


def telnet_conf_ip(int_ip, ip, port):
    try:        
        TELNET_TIMEOUT = 5
        READ_TIMEOUT = 5
        
        #Logging into device
        #print("DEBUG - {} {} {}".format(int_ip, ip, port))
        conn = telnetlib.Telnet(ip, port, TELNET_TIMEOUT)
       
        #Entering global config mode
        conn.write(b"en\n")
        conn.write(b"configure terminal\n")
        conn.write(b"int e0/0\n")
        conn.write(b"ip address %b 255.255.255.0\n" % int_ip.encode())
        conn.write(b"end\n")
        conn.write(b"wr\n")
        time.sleep(1)
        
        #Closing the conn
        conn.close()
        
    except IOError as error:
        print(error)


def main():
    print()
    print("Getting device info from the Eve-NG lab - '{}'".format(sys.argv[1]))
    device_dict = eveng_api()
    print(device_dict)

    for value in device_dict.items():
        hostname = value[1][0]
        ip = value[1][1]
        port = value[1][2]
        print()
        print("Configuring {} ...".format(hostname))
        print("Configuring SSH and interface e0/0 DHCP ...")
        telnet_conf(hostname, ip, port)

    print("\nSleep 45s for the device to get DHCP IP address and generate crypto keys.")
    print("Next step will configure the DHCP IP address as permanent IP in interface.\n")
    time.sleep(45)
    
    with open("ip.txt","w") as f:
    
        for value in device_dict.items():
            hostname = value[1][0]
            ip = value[1][1]
            port = value[1][2]
    
            int_output = telnet_show_int_ip(ip, port)
            #print(int_output)
    
            int_output = int_output.decode('utf8')
            int_ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', int_output)
    
            print("{} fixed IP address - {}".format(hostname, int_ip[0]))
            device = "{} {}\n".format(hostname, int_ip[0])
            
            f.write(device)
            time.sleep(1)
    
            print("Configuring IP address from DHCP as permanent ...")
            telnet_conf_ip(int_ip[0], ip, port)
            
    print()        
    print("INFO - ip.txt created to deploy the INE lab config for {} topology.".format(sys.argv[1]))
    print()
if __name__ == '__main__':
	main()


