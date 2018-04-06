# VPNPi

## Installation

### Prerequesites

- python 3.x
  - ``sudo apt-get install python3``
- pip3
  - ``sudo apt-get install python3-pip``
- flask
  - ``pip3 install flask``

### Main Program

- Download newest release
- Copy files to preferred Destination (/etc/VPNPi/)

## Configure

### Host and Port

- change ``VPNPi.py``

```
  app.run(host="0.0.0.0", port=5000)
```

- Host:
  - 0.0.0.0 -> listen on all Interfaces, open to LAN
  - 127.0.0.1 / localhost / [blank] -> only listen on local machine
- Port:
  - You can choose what you want, but it may be that the port is already in use.

## Run

- cd into installation directory
- ``python3 VPNPi.py``

Access the Webpage from your Browser

-> [IP-Adress / localhost]:[Port]

## Setup on Raspberry Pi

### Allow Connections from LAN

**run this in Terminal**
``` bash
  $ iptables -I INPUT -p tcp --dport 5000 -j ACCEPT
```

**in VPNPi.py**
```python
  app.run(host="0.0.0.0", port=5000)
```
### make App run after reboot

** Terminal **
```bash
$ crontab -e
```

**add this to the File**
```
  @reboot cd /etc/VPNPi; python3 VPNPi.py > log.txt 2> error.txt; cd
  */15 * * * * sudo service openvpn restart
```
