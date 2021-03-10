"""
 * sample feature module / just an example
 * for sma-em daemon
 *
"""
def run(emparts,config):
    """
    * sma-em daemon calls run for each measurement package
    * emparts: all measurements of one sma-em package
    * config: all config items from section FEATURE-[featurename] in /etc/smaemd/config
    *
    """
    #print("running sample feature")
    #print ('config')
    #print(config)
    pass


def stopping(emparts,config):
    """
    * executed on daemon stop
    * do some cleanup / close filehandles if needed and so on...
    """
    print("quitting")
    #close filehandles

def config(config):
    """
    * executed on daemon config init
    * do some configuration stuff...
    """
    global sw_debug
    sw_debug = int(config.get('debug', 0))
    print("sample: feature enabled")
