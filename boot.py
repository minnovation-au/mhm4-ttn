####################################################
########### 							############
###########  MHM4LD boot.py 			############
###########	 Firmware v0.1L 			############
###########  Written by Simon Maselli	############
###########	 (c) M innovation 2018		############
###########								############
####################################################

import gc, ubinascii, machine, pycom, struct, sys

mac=ubinascii.hexlify(machine.unique_id(),':').decode().replace(":","")
pycom.heartbeat(False)
print(mac)
gc.enable()
sys.path.append('/flash/ch')
sys.path.append('/flash/www')

############## INITIALISE WiFi ###################
from network import WLAN
wlan = WLAN(mode=WLAN.AP, ssid='AlphaX-MHM4-'+mac[-4:], auth=(WLAN.WPA2, mac), channel=11, antenna=WLAN.EXT_ANT)

######### START WEBBROWSER IF NOT CONFIGURED #########
if 'config.py' not in os.listdir('/flash'):
    print('Start WebServer')
    import webserver
    while True:
        pass

######## INITIALISE EXTERNAL STORAGE IF FITTED #######
import os
from machine import SD
try:
    sd = SD()
    os.mount(sd, '/sd')
except:
    pass

######################################
########## LoRaWAN Setup #############
######################################
import config
from network import LoRa

dev_addr = struct.unpack(">l", ubinascii.unhexlify(config.devadd))[0] # these settings can be found from TTN
nwk_swkey = ubinascii.unhexlify(config.nwskey) # these settings can be found from TTN
app_swkey = ubinascii.unhexlify(config.appkey) # these settings can be found from TTN

print("Connecting to TTN")
lora = LoRa(mode=LoRa.LORAWAN)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

print("Removing all channels ", end='')
for i in range(0, 72):
    print("{}, ".format(i), end='')
    lora.remove_channel(i)
print(" OK")

# Then we create only the channels we want.
# It shouldn't be necessary to set up more than one channel. See:
# https://forum.pycom.io/topic/1284/problem-pairing-otaa-node-to-nano-gateway-in-us-ttn/7
lora.add_channel(0, frequency=916800000, dr_min=0, dr_max=5)
lora.add_channel(1, frequency=923000000, dr_min=0, dr_max=5)