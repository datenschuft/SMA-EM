"""
    Allow remote debug with PyCharm

    2018-12-23 Tommi2Day

    [FEATURE-debug]
    # Debug settings
    debughost=mypc
    debugport=9100

"""
import pydevd

def run(emparts,config):
    pass
def stopping(emparts,config):
    pass
def config(config):
    # prepare mqtt settings
    print('debug feature enabled')
    debughost = config.get('debughost', None)
    debugport = config.get('debugport', None)
    if None not in (debughost,debugport):
        try:
            print('activate debug for '+debughost+' Port '+str(debugport))
            pydevd.settrace(debughost, port=int(debugport), stdoutToServer=True, stderrToServer=True)
        except Exception as e:
            print( '...failed')
            print(e)
            pass
