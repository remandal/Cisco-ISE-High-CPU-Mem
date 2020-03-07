import os
import datetime
import netmiko
from netmiko import ConnectHandler
from netmiko import Netmiko

"""
iou1 = {
    'device_type': 'cisco_ios',
    'ip': '172.16.221.106',
    'username': 'admin',
    'password': 'cisco',
}

device = ConnectHandler(**iou1)
"""




device = ConnectHandler(device_type="cisco_ios", ip="DEVICE IP",
                        username="USERNAME", password="PASSWORD")

output1 = device.send_command("show running-config")
save_file = open("Switch_running.txt", "w")
save_file.write(output1)
save_file.close()
device.disconnect()
