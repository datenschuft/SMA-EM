"""
    Send SMA values to mqtt broker.

    2018-12-23 Tommi2Day
    2019-03-02 david-m-m

    Configuration:

    [FEATURE-mqtt]
    # MQTT broker details

    mqtthost=mqtt
    mqttport=1883
    #mqttuser=
    #mqttpass=

    #mqttf topic and provided data ields
    mqttfields=pconsume,psupply,p1consume,p2consume,p3consume,p1supply,p2supply,p3supply
    #topic will be exted3ed with serial
    mqtttopic=SMA-EM/status

    # publish all values additionally as single topics (0 or 1)
    publish_single=1

    # How frequently to send updates over (defaults to 20 sec)
    min_update=5

    #debug output
    debug=0

"""

import paho.mqtt.client as mqtt
import platform
import json
import time


mqtt_last_update = 0
mqtt_debug = 0

def run(emparts,config):
    global mqtt_last_update
    global mqtt_debug


    # Only update every X seconds
    if time.time() < mqtt_last_update + int(config.get('min_update', 20)):
        if (mqtt_debug > 1):
            print("mqtt: data skipping")
        return

    # prepare mqtt settings
    mqtthost = config.get('mqtthost', 'mqtt')
    mqttport = config.get('mqttport', 1883)
    mqttuser = config.get('mqttuser', None)
    mqttpass = config.get('mqttpass', None)
    mqtttopic = config.get('mqtttopic',"SMA-EM/status")
    mqttfields = config.get('mqttfields', 'pconsume,psupply')
    publish_single = int(config.get('publish_single',0))

    # mqtt client settings
    myhostname = platform.node()
    mqtt_clientID = 'SMA-EM@' + myhostname
    client = mqtt.Client(mqtt_clientID)
    if None not in [mqttuser,mqttpass]:
        client.username_pw_set(username=mqttuser, password=mqttpass)

    #last aupdate
    mqtt_last_update = time.time()


    serial = emparts['serial']
    data = {}
    for f in mqttfields.split(','):
        data[f] = emparts[f]

    #add pv data
    try:
        #add summ value to
        from features.pvdata import pv_data
        pvpower=pv_data.get("AC Power",0)
        if pvpower is None: pvpower = 0
        pconsume=emparts.get('pconsume',0)
        psupply=emparts.get('psupply',0)
        pusage=pvpower+pconsume-psupply
        data['pvsum']=pvpower
        data['pusage']=pusage
    except:
        pv_data = None
        pass


    data['timestamp']=mqtt_last_update
    payload=json.dumps(data)
    topic=mqtttopic+'/'+str(serial)
    try:
            # mqtt connect
            client.connect(str(mqtthost), int(mqttport))
            client.on_publish = on_publish
            client.publish(topic, payload)
            # publish each value as separate topic
            if publish_single == 1:
                for item in data.keys():
                    itemtopic=topic+'/'+item
                    if mqtt_debug > 0:
                        print("mqtt: publishing %s:%s" % (itemtopic,data[item]) )
                    client.publish(itemtopic,str(data[item]))
            if mqtt_debug > 0:
                print("mqtt: sma-em data published %s:%s" % (
                    format(time.strftime("%H:%M:%S", time.localtime(mqtt_last_update))),payload))

            #pvoption
            mqttpvtopic = config.get('pvtopic', None)
            if None not in [pv_data,mqttpvtopic]  :
                if pv_data is not None:
                    pvserial = pv_data.get("serial")
                    pvtopic=mqttpvtopic+'/'+str(pvserial)
                    payload=json.dumps(pv_data)
                    client.publish(pvtopic, payload)
                    if mqtt_debug > 0:
                        print("mqtt: sma-pv data published %s:%s" % (
                            format(time.strftime("%H:%M:%S", time.localtime(mqtt_last_update))),payload))

    except Exception as e:
            print("mqtt: Error publishing")
            print(e)
            pass



def stopping(emparts,config):
    pass

def on_publish(client,userdata,result):
    time.sleep(0.01) # experimental value, seems to work...
    pass

def config(config):
    global mqtt_debug
    mqtt_debug=int(config.get('debug', 0))
    print('mqtt: feature enabled')
