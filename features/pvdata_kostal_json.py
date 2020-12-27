"""
    Get inverter pv values http / Json on Kostal interters

    2020-05-24 Wenger Florian

    Configuration:
    pip3 install requests json

    [FEATURE-pvdata_kostal_json]

    # How frequently to send updates over (defaults to 20 sec)
    # my kostal inverter updates the values only every 3 seconds
    #
    # How frequently to send updates over (defaults to 20 sec)
    min_update=15
    #debug output
    debug=0

    #inverter connection
    inv_host = <inverter-ip>
    #['address', 'NONE', 'NONE' 'description', 'unit']
    # to get the same structure of sma pvdata feature
    registers = [
          ['33556736', 'NONE', 'NONE', 'DC Power', 'W'],
          ['33555202', 'NONE', 'NONE', 'DC string1 voltage', 'V'],
          ['33555201', 'NONE', 'NONE', 'DC string1 current', 'A'],
          ['33555203', 'NONE', 'NONE', 'DC string1 power', 'W'],
          ['67109120', 'NONE', 'NONE', 'AC Power', 'W'],
          ['67110400', 'NONE', 'NONE', 'AC frequency', 'Hz'],
          ['67110656', 'NONE', 'NONE', 'AC cosphi', '°'],
          ['67110144', 'NONE', 'NONE', 'AC ptot limitation', ''],
          ['67109378', 'NONE', 'NONE', 'AC phase1 voltage', 'V'],
          ['67109377', 'NONE', 'NONE', 'AC phase1 current', 'A'],
          ['67109379', 'NONE', 'NONE', 'AC phase1 power', 'W'],
          ['251658754', 'NONE', 'NONE', 'yield today', 'Wh'],
          ['251658753', 'NONE', 'NONE', 'yield total', 'kWh'],
          ['251658496', 'NONE', 'NONE', 'operationtime', ''],
          ]


r = requests.get(url='http://192.168.1.21/api/dxs.json?dxsEntries=67109120&sessionId=1234567890')
cont = json.loads(r.content)
#print(cont)
print(cont["dxsEntries"][0]["value"],"W Kostal")
sys.exit()

"""

import requests, json, time
pv_last_update = 0
pv_debug = 0
# pv_data
pv_data={}

def run(emparts,config):
    global pv_debug
    global pv_last_update
    #global pv_data_last
    global pv_data

    host = config.get('inv_host')
    registers = eval(config.get('registers'))

    # Only update every X seconds
    if time.time() < pv_last_update + int(config.get('min_update', 20)):
        if (pv_debug > 0):
            print("pv: data skipping")
            print("reuse last values")
            print("PV:" + format(pv_data))
        return
    pv_last_update = time.time()
    url = "http://"+host+"/api/dxs.json?sessionId=1234567890"
    for register in registers:
        if (pv_debug > 0):
            print (register[0])
        url=url+"&dxsEntries="+register[0]
    if (pv_debug > 1):
        print (url)
    r = requests.get(url)
    cont = json.loads(r.content)
    #print(cont)
    pv_data={}
    if cont['status']["code"] == 0:

        for pvjdata in cont["dxsEntries"]:
            #process the json values
            item=pvjdata["dxsId"]
            value=pvjdata["value"]
            for register in registers:
                if int(register[0])==int(item):
                    if pv_debug > 0:
                        print("---")
                        print(str(item) + " " + register[3] + " " + str(value) + " " + register[4])
                    pv_data[register[3]]=float(value)
        #pv_data_last=pv_data
    else:
        print ("PVdata-Result json, but not OK")

    if pv_data is None:
        if pv_debug > 0:
            print("PV: no data" )

    pv_data['timestamp'] = time.time()
    if pv_debug > 0:
            print("PV:" + format(pv_data))


def stopping(emparts,config):
    pass

def config(config):
    global pv_debug
    pv_debug=int(config.get('debug', 0))
    print('pvdata_kostal_json: feature enabled')
