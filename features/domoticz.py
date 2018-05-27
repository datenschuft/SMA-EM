"""
    Send SMA values over to domoticz. Configuration like:

    [FEATURE-domoticz]
    # Domoticz API endpoint
    api=http://127.0.1.1:8080/json.htm

    # How frequently to send updates over (defaults to 20 sec)
    min_update=30

    # List of items to send over. Each item should contain a string like <SMA serial>:<domoticz ID>,<SMA serial 2>:<domoticz ID 2>, ...
    pregard=1234567869:73
    v1=1234567869:72

    original feature written by https://github.com/mzealey
    rewritten by wenger florian 2018-05-17 (untested - please check the feature)
"""




from features.smafeature import smafeature
class feature(smafeature):
    def __init__(self):
        super().__init__()
        self.__last_update = 0
        #declare your own thins
        print("initialisation of feature domoticz")
    def run (self,emparts):
        import json
        import time
        import urllib.request
        # Only update every X seconds
        config=self.getconfig()
        if time.time() < self.__last_update + int(config.get('min_update', 20)):
            #print("skipping")
            return
        self.__last_update = time.time()
        serial = format(emparts['serial'])
        for key in config:
            if key in ['api', 'min_update']:
                continue
            # Dictionary of serial: domoticz device id
            dom_ids = dict(item.split(':') for item in config[key].split(','))
            if serial not in dom_ids:
                continue
            url = "%s?type=command&param=udevice&idx=%s&nvalue=0&svalue=" % (config['api'], dom_ids[serial])
            if key in ['pregard', 'p1regard', 'p2regard', 'p3regard']:
                url += "%0.2f;%0.2f" % (emparts[key], emparts[key + "counter"] * 1000)
            else:
                url += "%0.2f" % emparts[key]
            try:
                urllib.request.urlopen( url )
            except Exception as e:      # ignore if domoticz was down (URLError doesnt catch all io errors that may occur)
                print("Error from domoticz request")
                print(e)
                pass
    def cleanup(self):
        print("done")
