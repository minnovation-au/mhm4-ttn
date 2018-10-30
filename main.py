####################################################
########### 							############
###########  MHM4LD main.py 			############
###########	 Firmware v0.1L				############
###########  Written by Simon Maselli	############
###########	 (c) M innovation 2018		############
###########								############
####################################################

############ Import Required Modules ############
import machine
import utime, gc, pycom, os, ubinascii, ustruct, socket
from machine import WDT, deepsleep, Timer, Pin
from network import Sigfox

############ DEFINE GLOBAL VARIABLES ############
mac=ubinascii.hexlify(machine.unique_id(),':').decode().replace(":","")
chrono=Timer.Chrono()
chrono.start()
wdt=WDT(timeout=30000)

############ SET PINOUT FOR DEVICE MODEL ############ 
pins = ['P10,P19','P11,P20','P21,P3','P22,P9'] #Pinout for MHM4 Mainboard v2.4

############ INDICATE (external light) ############
def indicate():
    p_out = Pin('P12', mode=Pin.OUT)
    p_out.value(1)
    pycom.rgbled(0x00007f) #Turn on Red LED
    utime.sleep(1.2)
    p_out.value(0)
    pycom.rgbled(0) #Turn on Red LED
    utime.sleep(1.2)

############ POWERNAP FUNCTION ############
def powerNap(): ### Cleanup & Powernap Mode
    c=0
    chrono.reset()
    gc.collect()
    print("PowerNap")
    while chrono.read() < 586:   #THROTTLE FOR SEND TO 10mins
        wdt.feed()
        utime.sleep(1)
        c+=1
        if c == 16:
            print("Heartbeat")
            c=0

################# SETUP SOCKET #################
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW) # create a LoRa socket
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5) # set the LoRaWAN data rate
s.setblocking(False) # make the socket non-blocking

############ LOAD CHANNEL & SEND DATA ############
while True:
    for y in range(0,4):
        io = pins[y].split(',')
        if 'ch'+str(y+1)+'.py' in os.listdir('/flash/ch'):
            packet = __import__('ch'+str(y+1))
            try:
                data = bytes("{\"ch"+str(y+1)+"\":"+packet.data(io[0],io[1])+"}",'utf-8')
                s.send(data) #Send on LoRaWAN TTN Network
                indicate()
            except:
                pycom.rgbled(0x7f0000) #Turn on Red LED
                print("CH"+str(y+1)+" Fail")

    powerNap()