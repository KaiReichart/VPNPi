from flask import render_template, redirect
from app import app
import json, random, glob, re, shutil, os




@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/vpn')
def vpn():
    with open('vpnServers.json') as json_data:
        vpnFile = json.load(json_data)
        currentvpn = vpnFile['vpnlist'][vpnFile['currentvpnID']]
        vpnlist = vpnFile['vpnlist']
    return render_template('vpn.html', vpnlist=vpnlist, currentvpn=currentvpn)

## TODO: do server stuff
@app.route('/vpn/changeVPN/<vpnID>')
def changeVPN(vpnID):
    with open('vpnServers.json') as json_data:
        vpnFile = json.load(json_data)
        currentvpn = vpnFile['vpnlist'][vpnFile['currentvpnID']]
        vpnlist = vpnFile['vpnlist']

    if vpnID == 'random':
        vpnID = random.choice(list(vpnlist.keys()))
        while (vpnlist[vpnID]['netflix'] == 0):
            vpnID = random.choice(vpnlist.keys())
    vpnFile['currentvpnID'] = vpnID
    with open('vpnServers.json', 'w') as outfile:
        json.dump(vpnFile, outfile)

    filename = vpnFile['vpnlist'][vpnID]['filename']
    os.system('sudo cp ovpn/'+filename+' /etc/openvpn/vpn.conf')
    os.system('sudo service openvpn restart')
    return redirect("/vpn")

    return vpnID;


@app.route('/vpn/vpnNetflix/<state>')
def vpnNetflix(state):
    with open('vpnServers.json') as json_data:
        vpnFile = json.load(json_data)
        currentvpnID = vpnFile['currentvpnID']
        vpnlist = vpnFile['vpnlist']
    if state == '1':
        vpnlist[currentvpnID]['netflix'] = '1';
    elif state == '0':
        vpnlist[currentvpnID]['netflix'] = '0';
    else:
        return redirect("/vpn")
    vpnFile['vpnlist'] = vpnlist
    with open('vpnServers.json', 'w') as outfile:
        json.dump(vpnFile, outfile)
    return redirect("/vpn")


@app.route('/vpn/resetList')
def resetList():
    filenameList = glob.glob("ovpn/*.ovpn")

    with open('vpnServers.json') as json_data:
        vpnFile = json.load(json_data)
        currentvpnID = vpnFile['currentvpnID']

    vpnlist = {}
    for filename in filenameList:
        filename = filename.rsplit('/', 1)[-1]
        id = filename.rsplit('.')[0]
        vpnlist[id] = {}
        vpnlist[id]['filename'] = filename
        vpnlist[id]['id'] = id
        vpnlist[id]['netflix'] = ''


    vpnFile['currentvpnID'] = id

    vpnFile['vpnlist'] = vpnlist

    with open('vpnServers.json', 'w') as outfile:
        json.dump(vpnFile, outfile)


    return redirect("/vpn")
    
@app.route('/vpn/resetConnection')
def resetConnection():
    os.system('sudo service openvpn restart')
    return redirect("/vpn")


@app.route('/log')
def log():
    with open('error.txt') as f:
        log = f.read()
    return log

@app.route('/reboot')
def reboot():
    os.system('sudo reboot')
