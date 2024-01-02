import csv
import serial
import serial.tools.list_ports
import time
import os
import subprocess

def load_csv(filename='pywebclicker.csv'):
    f = open(filename,'r')
    rdr = list(csv.reader(f))
    list_host_info = list()
    
    title_line = rdr[0]
    data_line = rdr[1:]
    for data in data_line:
        host_info = { name: value for name, value in zip(title_line, data) }
        list_host_info.append(host_info)
    
    f.close()
    return list_host_info

def send_serial(com='COM4', command='3', poweron=True):
    ports = serial.tools.list_ports.comports()
    check = False
    for port, desc, hwid in sorted(ports):
        print("{} : {} [{}]".format(port, desc, hwid))
        if ( com == port ):
            check = True
    if (check is False):
        print('{} is not found'.format(com))
        return False # not find COM port
    try:
        ser = serial.Serial(
            port = com, 
            baudrate=9600, 
            parity='N',
            stopbits=1,
            bytesize=8,
            timeout=8
            )
    except serial.serialutil.SerialException:
        print('{} is already connected by other SW'.format(com))
        return False # device is already connected

    if (ser.isOpen() is False):
        print('{} is not open'.format(com))
        return False 
    if poweron is True:
        power_on(ser,command)
        print('{} {} power-on'.format(com,command))
    else:
        power_off(ser,command)
        print('{} {} power-off'.format(com,command))
    ser.close()
    return True

def power_on(ser, command='3'):
    command_map = {'1':'q', '2':'w', '3':'e', '4':'r'}
    time.sleep(0.1)        
    ser.write(command.encode()) # power release
    time.sleep(0.1)
    ser.write(command_map[command].encode()) # power push
    time.sleep(0.1)
    ser.write(command.encode()) # power release
    time.sleep(0.1)
    time.sleep(10) # wait power on...
    
def power_off(ser, command='3'):
    command_map = {'1':'q', '2':'w', '3':'e', '4':'r'}
    time.sleep(0.1)        
    ser.write(command.encode()) # power release
    time.sleep(0.1)
    ser.write(command_map[command].encode()) # power push
    time.sleep(7) # wait 10s...
    ser.write(command.encode()) # power release
    time.sleep(0.1)
    time.sleep(3) # wait remain time    

def ping_check(host='WDKR-PSHOST-01'):
    hostname = host+'.sdcorp.global.sandisk.com'
    response = os.system("ping -n 1 " + hostname + ' | findstr /i "TTL" > NUL')
    if response == 0:
        Netstatus = "Active"
    else:
        Netstatus = "Error"
    return Netstatus
    
def check_clicker_command(command):
    clicker = command
    clicker = [item.strip() for item in clicker.split('/')]
    if (clicker[0].find('COM') < 0):
        print ('COM is not defined')
        return False, False
    if (clicker[1] in ['1','2','3','4']) is False:
        print ('Clicker maaping (1,2,3,4) is wrong. please check it')
        return False, False
        
    _com = clicker[0]
    _clicker_no = clicker[1]
    return _com, _clicker_no
if __name__ == "__main__":
    #send_serial()
    #s = ping_check(host="WDKR-CSH-HW2")
    c = 'WDKR-PSHOST-01-on'
    clicker = 'COM3 / 1 / q'
    check_clicker_command(clicker)
    print(clicker)