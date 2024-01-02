from flask import Flask, render_template, request, redirect, send_file, jsonify, flash
from pyclicker import load_csv, ping_check, check_clicker_command, send_serial
import time
import random
app = Flask("JobScrapper")
app.secret_key = "Chung"
db = {} # 데이터베이스
list_host_info=load_csv()

@app.route('/data')
def get_data():
    data = dict()
    for host_info in list_host_info:
        # 'WDKR-PSHOST-01' : xxxx
        # 'WDKR-PSHOST-02' : xxxx
        #data[host_info['HOST'].replace('-','')] = '%03d'%(int(random.random()*1000))
        data[host_info['HOST'].replace('-','')] = ping_check(host_info['HOST'])
    return jsonify(data)

@app.route('/<cmd>')
def command(cmd=None):
    cmd = cmd.split('__') # cmd[0] : host name,  cmd[1] : on or off (via button, __on or __off is attached)
    response = 'Power on'
    comport = False
    no = False
    print(cmd)
    for host_info in list_host_info:
        print(host_info['HOST'])
        if(host_info['HOST'] == cmd[0]): # find matched clicker command
            comport, no = check_clicker_command(host_info['Clicker'])
            break
    if (comport is not False):
        ret = send_serial(com=comport, command=no, poweron=True if cmd[1] == 'on' else False)
        if ret is True:
            return 'Done : {} trigger power {}.'.format(host_info['HOST'], cmd[1]), 200, {'Content-Type': 'text/plain'}
        else:
            return 'COM port is not found or used in other SW', 200, {'Content-Type': 'text/plain'}
    else:
        return 'Clicker is not configured or COM port is not found', 200, {'Content-Type': 'text/plain'}
    
@app.route("/")
def home():
    global list_host_info
    list_host_info=load_csv()
    return render_template("home.html",list_host_info=list_host_info)

app.run("0.0.0.0")