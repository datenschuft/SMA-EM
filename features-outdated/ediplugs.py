"""
    Get power consumption values of Edimax smartplugs

    2020-08-19 thsell

    [FEATURE-ediplugs]
    plugs = [
    [ip, user, password]
    ] 
"""

import time
from libs.smartplug import SmartPlug

edi_last_update = 0
edi_debug = 0
edi_data=[]

def run(emparts,config):

    global edi_debug
    global edi_last_update
    global edi_data


    # Only update every X seconds
    if time.time() < edi_last_update + int(config.get('min_update', 20)):
        if (edi_debug > 1):
            print("edi: data skipping")
        return


    edi_last_update = time.time()

    edi_data = []
    for inv in eval(config.get('plugs')):
        host, user, password = inv
        plug = SmartPlug(host, (user, password))

        try:
            mdata = {'state': plug.state, 'pconsume': float(plug.power), 'aconsume': float(plug.current)}
            edi_data.append({**plug.info, **mdata})
        except:
            print('Error connecting to Smartplug')

    # query
    if edi_data is None:
        if edi_debug > 0:
            print("Edi: no data" )

    if edi_debug > 0:
        for i in edi_data:
            i['timestamp'] = time.time()
            print("Edi:" + format(i))


def stopping(emparts,config):
    pass

def on_publish(client,userdata,result):
    pass

def config(config):
    global edi_debug
    edi_debug=int(config.get('debug', 0))
    print('ediplugs: feature enabled')
