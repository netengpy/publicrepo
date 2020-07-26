# Eve-NG-in-Google-Cloud :cloud:
Install Eve-NG in Google Cloud

#### Create a Googe Cloud account which will give you $300US free credit
https://cloud.google.com/

* Log in to GCP
* Click `Go To Console`
* Click `Select a project`
* Click `New Project`
* Project name = `cloud-eveng`
* Click '`Create`

Click `Activate Cloud Shell` (top right toolbar) 

> Create the nested virtualization supported image based on `Ubuntu 16.04 LTS` 

Paste the below into the cloud shell terminal: 

```gcloud compute images create nested-virt-ubuntu --source-image-project=ubuntu-os-cloud --source-image-family=ubuntu-1604-lts --licenses="https://www.google.com/compute/v1/projects/vm-options/global/licenses/enable-vmx”```

Say `yes` if asked to enable API on project

* Click burger menu on the top left and select `Compute Engine` 
* Select the project if asked
* Click `Create`

Enter the below properties. 

Name = `eve-ng` 
Region = `Choose location closest or cheaper for you`
Zone = `Choose location closest or cheaper for you`

> Choosing a region closer to you is better from a latency perspective. 
> Look at the estimated price on the left, prices varies across different regions.

> To run IOS-XR, IOS-XRV or CSR1000v increase the CPU’s and memory. 

* Firewall = `Allow HTTP traffic` 

* Click Done
* Click Create

#### Create Firewall rules
- Step 1: Navigation menu/VPC Network/Firewall rules
- Step 2: Create new firewall rule
- Step 3: Create an ingress FW rule; allow TCP ports 0-65335
- Step 4: Create an egress FW rule; allow TCP ports 0-65535

#### Create GCP bucket
* Create a GCP bucket and upload the IOL images and script to generate the license key
* Important note - name the bucket whatever you want BUT the folder containing the images must be named 'images'. Else the eveng-init-setup.sh script will fail. Modify the paths in script if needed.

* Navigate back to `Compute Engine > VM Instances`
* Click on `SSH` 

```
sudo -i
* git clone or copy the shell script to eve-ng 
Go the folder with shell script and execute: 
bash eveng-init-setup.sh <bucket-name> 
```
You could also make the script executeable - `chmod +x eveng-init-setup.sh` and run as `./eveng-init-setup.sh <bucket-name>`
* Fix the permissions using the below command: 
`/opt/unetlab/wrappers/unl_wrapper -a fixpermissions`

* Browse to the web GUI with your instance's public IP address

