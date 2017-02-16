#! /usr/bin/python

"""Copyright 2011 Phidgets Inc.
This work is licensed under the Creative Commons Attribution 2.5 Canada License.
To view a copy of this license, visit http://creativecommons.org/licenses/by/2.5/ca/
"""

__author__="Adam Stelmack"
__version__="2.1.8"
__date__ ="14-Jan-2011 2:29:14 PM"

#Basic imports
import sys
from time import sleep
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetException
from Phidgets.Devices.Bridge import Bridge, BridgeGain

#Create an accelerometer object
try:
    bridge = Bridge()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Information Display Function
def displayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (bridge.isAttached(), bridge.getDeviceName(), bridge.getSerialNum(), bridge.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of bridge inputs: %i" % (bridge.getInputCount()))
    print("Data Rate Max: %d" % (bridge.getDataRateMax()))
    print("Data Rate Min: %d" % (bridge.getDataRateMin()))
    print("Input Value Max: %d" % (bridge.getBridgeMax(0)))
    print("Input Value Min: %d" % (bridge.getBridgeMin(0)))

#Event Handler Callback Functions
def BridgeAttached(e):
    attached = e.device
    print("Bridge %i Attached!" % (attached.getSerialNum()))

def BridgeDetached(e):
    detached = e.device
    print("Bridge %i Detached!" % (detached.getSerialNum()))

def BridgeError(e):
    try:
        source = e.device
        print("Bridge %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def BridgeData(e):
    source = e.device
    ##############################################
    bi = source.getSerialNum();
    einp = e.index;
    ev = e.value;
    #print("%f" % (ev))
    print(e.index, e.value)
    with open(fname, "a") as myfile:
        myfile.write("%2.1f\t" % (einp))
        myfile.write("%f\n" % (ev))
    ##############################################
    #print("Bridge %i: Input %i: %f" % (source.getSerialNum(), e.index, e.value))


######################################     Main Program Code       ######################################
#########################################################################################################
try:
    print("Please input the file name for readings:")
    fname = raw_input()
    bridge.setOnAttachHandler(BridgeAttached)
    bridge.setOnDetachHandler(BridgeDetached)
    ##############################################
    fptr=open(fname,"w")
    #fptr.write("data begins below:\n")
    fptr.close
    ##############################################
    bridge.setOnErrorhandler(BridgeError)
    bridge.setOnBridgeDataHandler(BridgeData)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    bridge.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    bridge.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        bridge.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s\n" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    displayDeviceInfo()

try:
    print("Set data rate to 40ms ...")
    bridge.setDataRate(40)
    sleep(1)

    print("Set Gain to 8...")
    bridge.setGain(1, BridgeGain.PHIDGET_BRIDGE_GAIN_8)
    sleep(1)

    ##############    Select which bridge to enable   ###################
    print("Enable the Bridge input for reading data...")
    bridge.setEnabled(0, True)
    bridge.setEnabled(1, True)
    bridge.setEnabled(2, True)
    bridge.setEnabled(3, True)
    sleep(1)
    #####################################################################

except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        bridge.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)

print("Press Enter to quit....")

chr = sys.stdin.read(1)

print("Closing...")

try:
    ##################    Disable active bridges   ######################
    print("Disable the Bridge input for reading data...")
    bridge.setEnabled(0, False)
    bridge.setEnabled(1, False)
    bridge.setEnabled(2, False)
    bridge.setEnabled(3, False)
    #####################################################################
    sleep(1)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        bridge.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

    print("Exiting....")
    exit(1)

try:
    bridge.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)
