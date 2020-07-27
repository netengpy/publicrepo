#!/bin/sh

# Put IOL images and key gen script in bucket folder named "images"
# Otherwise amend the lines 23-29 accordingly 
# Script assumes <bucket-name>/images/ path for files needed for IOL 
# ./eveng-init-setup <bucket-name>

echo
echo "-[INFO]- Configuring SSH root login ..."
echo "---------------------------------------"
printf "PermitRootLogin = yes\nPasswordAuthentication = yes\n"
sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
sed -i 's/#PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config
echo
echo "-[INFO]- Restarting SSHD..."
service sshd restart
sleep 5

echo
echo "-[INFO]- Copying images from bucket to /tmp/images ..."
echo "------------------------------------------------------"

gsutil cp -r gs://$1/* /tmp/
   
cd /opt/unetlab/addons/iol/bin/
mv /tmp/images/* .
rm -rf /tmp/images
   
key=$(python CiscoKeyGen.py 2>&1)
   
echo $key
echo 
echo "-[INFO]- Added license to iourc ..."
echo
echo '[license]' > /opt/unetlab/addons/iol/bin/iourc
echo $key';' >> /opt/unetlab/addons/iol/bin/iourc
cat /opt/unetlab/addons/iol/bin/iourc
cd

sleep 5
/opt/unetlab/wrappers/unl_wrapper -a fixpermissions

echo "-[INFO]- Configure IP address pnet1"
echo "-----------------------------------"
ip address add 192.168.255.254/24 dev pnet1
echo
echo "-[INFO]- Configure NAT pnet0"
echo "----------------------------"
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -t nat -A POSTROUTING -o pnet0 -s 192.168.255.0/24 -j MASQUERADE
echo
echo "-[INFO]- Install DHCP Server"
echo "----------------------------"
apt-get update -y
apt-get install isc-dhcp-server -y

echo
echo "-[INFO]- Configure DHCP Server"
echo "------------------------------"
echo
echo 'sed -i "s/INTERFACES=/INTERFACES="pnet1"/" /etc/default/isc-dhcp-server'
sed -i 's/INTERFACES=/INTERFACES="pnet1"/' /etc/default/isc-dhcp-server
echo
echo 'sed -i "s/#authoritative;/authoritative;/" /etc/dhcp/dhcpd.conf'
sed -i 's/#authoritative;/authoritative;/' /etc/dhcp/dhcpd.conf 
echo

match='authoritative;'
insert='# EVE-NG NAT Interface\
subnet 192.168.255.0 netmask 255.255.255.0 {\
        range 192.168.255.1 192.168.255.100;\
        interface pnet1;\
        default-lease-time 600;\
        max-lease-time 7200;\
        option domain-name-servers 8.8.8.8;\
        option broadcast-address 192.168.255.255;\
        option subnet-mask 255.255.255.0;\
        option routers 192.168.255.1;\
}'

sed -i "/$match/ a $insert" /etc/dhcp/dhcpd.conf 

echo "-[INFO]- Restart DHCP Server"
echo "----------------------------"

systemctl start isc-dhcp-server
systemctl enable isc-dhcp-server
echo
echo "-[INFO]- DHCP server lease file"
echo "-------------------------------"
echo "/var/lib/dhcp/dhcpd.leases" 
#cat /var/lib/dhcp/dhcpd.leases
echo
echo "Use below egrep command to check DHCP lease"
echo "-------------------------------------------"
echo "egrep -a 'lease|hostname' /var/lib/dhcp/dhcpd.leases | sort | uniq"
echo

sleep 5
echo "-[INFO]- Installing Python venv package ..."
echo "-------------------------------------------"
sleep 3
apt-get install python3-venv -y

echo "-[INFO]- Creating Python3 venv named 'workspace'"
echo "------------------------------------------------"
python3 -m venv workspace
source workspace/bin/activate
pip install --upgrade pip
pip install netmiko==2.4.2
pip install paramiko
pip install ncclient
pip install xmltodict
deactivate
/opt/unetlab/wrappers/unl_wrapper -a fixpermissions
echo
echo "Check out the workspace venv for Python scripts"
echo "All Done! :)"

