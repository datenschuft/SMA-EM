"""
    Send SMA values to mqtt broker.

    2018-12-23 Tommi2Day
    2019-03-02 david-m-m
    2020-09-22 Tommi2Day ssl support
    2021-01-07 sellth added support for multiple inverters

    Configuration:

    [FEATURE-mqtt]
    # MQTT broker details
    mqtthost=mqtt
    mqttport=1883
    #mqttuser=
    #mqttpass=
    mqttfields=pconsume,psupply,p1consume,p2consume,p3consume,p1supply,p2supply,p3supply
    #topic will be exted3ed with serial
    mqtttopic=SMA-EM/status
    pvtopic=SMA-PV/status
    # publish all values as single topics (0 or 1)
    publish_single=1
    # How frequently to send updates over (defaults to 20 sec)
    min_update=30
    #debug output
    debug=0

    # ssl support
    # adopt mqttport above to your ssl enabled mqtt port, usually 8883
    # options:
    # activate without certs=use tls_insecure
    # activate with ca_file, but without client_certs
    ssl_activate=0
    # ca file to verify
    ssl_ca_file=ca.crt
    # client certs
    ssl_certfile=
    ssl_keyfile=
    #TLSv1.1 or TLSv1.2 (default 2)
    tls_protocol=2

"""

import paho.mqtt.client as mqtt
import platform
import json
import time
import ssl
import traceback

mqtt_last_update = 0
mqtt_debug = 0


def run(emparts, config):
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
    mqtttopic = config.get('mqtttopic', "SMA-EM/status")
    mqttfields = config.get('mqttfields', 'pconsume,psupply')
    publish_single = int(config.get('publish_single', 0))

    ssl_activate = config.get('ssl_activate', False)
    ssl_ca_file = config.get('ssl_ca_file', None)
    ssl_certfile = config.get('ssl_certfile', None)
    ssl_keyfile = config.get('ssl_keyfile', None)
    tls_protocol = config.get('tls_protocol', "2")
    if tls_protocol == "1":
        tls = ssl.PROTOCOL_TLSv1_1
    elif tls_protocol == "2":
        tls = ssl.PROTOCOL_TLSv1_2
    else:
        tls = ssl.PROTOCOL_TLSv1_2
        if mqtt_debug > 0:
            print("tls_protocol %s unsupported, use (TLSv1.)2" % tls_protocol)

    # mqtt client settings
    myhostname = platform.node()
    mqtt_clientID = 'SMA-EM@' + myhostname
    client = mqtt.Client(mqtt_clientID)
    if None not in [mqttuser, mqttpass]:
        client.username_pw_set(username=mqttuser, password=mqttpass)

    if ssl_activate == "1":
        # and ssl_ca_file:
        if ssl_certfile and ssl_keyfile and ssl_ca_file:
            # use client cert
            client.tls_set(ssl_ca_file, certfile=ssl_certfile, keyfile=ssl_keyfile, tls_version=tls)
            if mqtt_debug > 0:
                print("mqtt: ssl ca and client verify enabled")
        elif ssl_ca_file:
            # no client cert
            client.tls_set(ssl_ca_file, tls_version=tls)
            if mqtt_debug > 0:
                print("mqtt: ssl ca verify enabled")
        else:
            # disable certificat verify as there is no certificate
            client.tls_set(tls_version=tls)
            client.tls_insecure_set(True)
            if mqtt_debug > 0:
                print("mqtt: ssl verify disabled")
    else:
        if mqtt_debug > 0:
            print("mqtt: ssl disabled")

    # last aupdate
    # last aupdate
    mqtt_last_update = time.time()

    serial = emparts['serial']
    data = {}
    for f in mqttfields.split(','):
        data[f] = emparts.get(f, 0)

    # add pv data
    pvpower = 0
    daily = 0
    try:
        from features.pvdata import pv_data

        for inv in pv_data:
            # handle missing data during night hours
            if inv.get("AC Power") is None:
                pass
            elif inv.get("DeviceClass") == "Solar Inverter":
                pvpower += inv.get("AC Power", 0)
                # NOTE: daily yield is broken for some inverters
                daily += inv.get("daily yield", 0)

        pconsume = emparts.get('pconsume', 0)
        psupply = emparts.get('psupply', 0)
        pusage = pvpower + pconsume - psupply
        data['pvsum'] = pvpower
        data['pusage'] = pusage
        data['pvdaily'] = daily
    except:
        pv_data = None
        pass

    data['timestamp'] = mqtt_last_update
    payload = json.dumps(data)
    topic = mqtttopic + '/' + str(serial)
    try:
        # mqtt connect
        client.connect(str(mqtthost), int(mqttport))
        client.loop_start()
        client.publish(topic, payload)
        if mqtt_debug > 0:
            print("mqtt: sma-em topic %s data published %s:%s" % (topic,
                                                                  format(time.strftime("%H:%M:%S", time.localtime(
                                                                      mqtt_last_update))), payload))
        # publish each value as separate topic
        if publish_single == 1:
            for item in data.keys():
                itemtopic = topic + '/' + item
                if mqtt_debug > 0:
                    print("mqtt: publishing %s:%s" % (itemtopic, data[item]))
                client.publish(itemtopic, str(data[item]))

        # pvoption
        mqttpvtopic = config.get('pvtopic', None)
        if None not in [pv_data, mqttpvtopic]:
            if pv_data is not None:
                for inv in pv_data:
                    pvserial = inv.get("serial")
                    pvtopic = mqttpvtopic + '/' + str(pvserial)
                    payload = json.dumps(inv)
                    # sendf pv topic
                    client.publish(pvtopic, payload)
                    if mqtt_debug > 0:
                        print("mqtt: sma-pv topic %s data published %s:%s" % (
                            pvtopic,
                            format(time.strftime("%H:%M:%S",
                                                 time.localtime(
                                                     mqtt_last_update))),
                            payload))
        client.loop_stop()
        client.disconnect()

    except Exception as e:
        print("mqtt: Error publishing")
        print(traceback.format_exc())
        pass


def stopping(emparts, config):
    pass


def config(config):
    global mqtt_debug
    mqtt_debug = int(config.get('debug', 0))
    print('mqtt: feature enabled')
