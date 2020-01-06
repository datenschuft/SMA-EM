"""
    Send SMA values to symcon (www.symcon.de) via web hook
    need Symcon 4.0+

    2018-12-23 Tommi2Day

    Configuration:
    [FEATURE-symcon]
    # symcon
    host=ips
    port=3777
    emhook=/hook/smaem
    pvhook=/hook/smawr
    timeout=5
    user=
    password=
    fields=pconsume,psupply,p1consume,p2consume,p3consume,p1supply,p2supply,p3supply
    pvfields=AC Power,AC Voltage,grid frequency,DC Power,DC input voltage,daily yield,total yield,Power L1,Power L2,Power L3

    # How frequently to send updates over (defaults to 20 sec)
    min_update=30

    debug=0

"""

import urllib.request,urllib.error
import json
import time
import platform

symcon_last_update = 0
symcon_debug=0
def run(emparts,config):
    global symcon_last_update
    global symcon_debug

    # Only update every X seconds
    if time.time() < symcon_last_update + int(config.get('min_update', 20)):
        if (symcon_debug > 1):
            print("Symcon: data skipping")
        return

    # prepare hook settings
    host = config.get('host', 'ips')
    port = config.get('port', 3777)
    timeout = config.get('timeout', 5)
    emhook = config.get('emhook','/hook/smaem')
    user = config.get('user', None)
    password = config.get('password', None)
    fields = config.get('fields', 'pconsume,psupply')

    # mqtt client settings
    myhostname = platform.node()

    symcon_last_update = time.time()

    url='http://'+host+':'+str(port)+emhook

    #last aupdate
    symcon_last_update = time.time()


    serial = emparts['serial']
    data = {}
    for f in fields.split(','):
        data[f] = emparts[f]

    data['timestamp']=symcon_last_update
    data['sender']=myhostname
    data['serial']=str(serial)
    payload=json.dumps(data)

    #prepare request
    req = urllib.request.Request(url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    dataasbytes = payload.encode('utf-8')  # needs to be bytes
    req.add_header('Content-Length', len(dataasbytes))
    #print(dataasbytes)
    req.add_header("User-Agent", "SMEM")

    #prepare auth
    if None not in [user,password]:
        passman = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, url, user, password)
        authhandler = urllib.request.HTTPBasicAuthHandler(passman)
        opener = urllib.request.build_opener(authhandler)
        urllib.request.install_opener(opener)
        if symcon_debug > 2:
            print('Symcon EM: use Basic auth')

    #send it
    try:
            response = urllib.request.urlopen(req, data=dataasbytes,timeout=int(timeout))

    except urllib.error.HTTPError as e:
        if symcon_debug > 0:
            print('Symcon EM: HTTPError: {%s} to %s' % (format(e.code),url ))
        pass
    except urllib.error.URLError as e:
        if symcon_debug > 0:
            print('Symcon EM: URLError: {%s} to %s ' % (format(e.reason),url))
        pass
    except Exception as e:
        if symcon_debug > 0:
            print("Symcon EM: Error from symcon request")
            print(e)
        pass
    else:
        if symcon_debug > 0:
            print("Symcon EM: data published %s:%s to %s" % (format(time.strftime("%H:%M:%S", time.localtime(symcon_last_update))),payload,url))

    #send pv data
    pvhook = config.get('pvhook')
    pvfields = config.get('pvfields', 'AC Power,daily yield')
    if  None in [pvhook,pvfields]: return
    try:
        from features.pvdata import pv_data
    except:
        return

    serial = pv_data['serial']
    data = {}
    pvurl = 'http://' + host + ':' + str(port) + pvhook
    pvpower = pv_data.get("AC Power")
    if None in [serial,pvpower]: return
    for f in pvfields.split(','):
      data[f] = pv_data.get(f,0)

    data['timestamp'] = symcon_last_update
    data['sender'] = myhostname
    data['serial'] = str(serial)
    pvpayload = json.dumps(data)

    # prepare request
    pvreq = urllib.request.Request(pvurl)
    pvreq.add_header('Content-Type', 'application/json; charset=utf-8')
    pvdataasbytes = pvpayload.encode('utf-8')  # needs to be bytes
    pvreq.add_header('Content-Length', len(pvdataasbytes))
    # print(dataasbytes)
    pvreq.add_header("User-Agent", "SMWR")

    # prepare auth
    if None not in [user, password]:
        passman = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, pvurl, user, password)
        authhandler = urllib.request.HTTPBasicAuthHandler(passman)
        opener = urllib.request.build_opener(authhandler)
        urllib.request.install_opener(opener)
        if symcon_debug > 2:
            print('Symcon PV: use Basic auth')

    # send it

    try:
        response = urllib.request.urlopen(pvreq, data=pvdataasbytes, timeout=int(timeout))

    except urllib.error.HTTPError as e:
        if symcon_debug > 0:
            print('Symcon PV : HTTPError: {%s} to %s ' % (format(e.reason),pvurl))
        pass
    except urllib.error.URLError as e:
        if symcon_debug > 0:
            print('Symcon PV: URLError: {%s} to %s ' % (format(e.reason),pvurl))
        pass
    except Exception as e:
        if symcon_debug > 0:
            print("Symcon PV: Error from symcon request")
            print(e)
        pass
    else:
        if symcon_debug > 0:
            print("Symcon PV: data published %s:%s to %s" % (
            format(time.strftime("%H:%M:%S", time.localtime(symcon_last_update))), pvpayload,pvurl))


def stopping(emparts,config):
    pass

def config(config):
    global symcon_debug
    symcon_debug=int(config.get('debug', 0))
    print('symcon: feature enabled')
