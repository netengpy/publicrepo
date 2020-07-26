ENVIRONMENT_IN_USE = "sandbox"

# Set the 'Environment Variables' based on the lab environment in use
if ENVIRONMENT_IN_USE == "sandbox":
    # Values for the Always On IOS XE Sandbox
    IOS_XE_1 = {
        "host": "ios-xe-mgmt.cisco.com",
        "username": "root",
        "password": "D_Vay!_10&",
        "netconf_port": 10000,
        "restconf_port": 9443,
        "ssh_port": 8181
    }
