#!/usr/bin/env python3
# coding=utf-8
"""
 * SMA-EM Daemon
 * Daemon processing measurement datageams from SMA Energymeter or Energymeter 2
 *
 * by Wenger Florian 2018-05-27
 * wenger@unifox.at
 *
 *  this software is released under GNU General Public License, version 2.
 *  This program is free software;
 *  you can redistribute it and/or modify it under the terms of the GNU General Public License
 *  as published by the Free Software Foundation; version 2 of the License.
 *  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
 *  without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 *  See the GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License along with this program;
 *  if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
 *
 */
"""
import sys, time
#from daemon3x import daemon3x
from configparser import SafeConfigParser
import smaem
import socket
import struct
import importlib
import signal
import time
import sys, getopt
import os
import glob, os

# ---------------------------------------------------------
class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self,signum, frame):
    self.kill_now = True

# ---------------------------------------------------------
#class MyDaemon(daemon3x):
#    def enablefeatures(self,featurelist):
#        self.__featurelist=featurelist
#    def stop(self):
#        for feature in self.__featurelist:
#            print ('stopping feature'+feature )
#            self.__featurelist[feature].cleanup()
#        super().stop()
#    def run(self):
#        #featureobj=smasample()
#        # prepare listen to socket-Multicast
#        socketconnected = False
#        while not socketconnected:
#            #try:
#            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
#            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#            sock.bind(('', MCAST_PORT))
#            try:
#                mreq = struct.pack("4s4s", socket.inet_aton(MCAST_GRP), socket.inet_aton(ipbind))
#                sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
#                file = open("/run/shm/em-status", "w")
#                file.write('multicastgroup connected')
#                file.close()
#                socketconnected = True
#            except BaseException:
#                print('could not connect to mulicast group... rest a bit and retry')
#                file = open("/run/shm/em-status", "w")
#                file.write('could not connect to mulicast group... rest a bit and retry')
#                file.close()
#                time.sleep(5)
#        emparts = {}
#        while True:
#            #getting sma values
#            emparts=smaem.readem(sock)
#            for serial in serials:
#                # process only known sma serials
#                if serial==format(emparts['serial']):
#                    for feature in self.__featurelist:
#                        print ('processing feature'+feature )
#                        self.__featurelist[feature].run(emparts)
#
# ---------------------------------------------------------

def startupfeatures():
    #initialisation of features
    print ("start features")
    featurelist = {}
    for feature in features:
        #print("from "+ feature+ " import " + feature)
        mod = __import__('features.' + feature, fromlist=['feature'])
        featureclass = getattr(mod, 'feature')
        featurelist[feature]=featureclass()
        #loading config of feature to feature object
        config=dict(parser.items('FEATURE-'+feature))
        featurelist[feature].loadconfig(config)
    return featurelist


# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------



#checkparameters
configfile = '/etc/smaemd/config'
try:
  opts, args = getopt.getopt(sys.argv[1:],"hc:v",["configfile=","ofile="])
except getopt.GetoptError:
  print ('unknown options\nuse sma-daemon.py -c <configfile>\nor try -h for more options')
  sys.exit(2)
for opt, arg in opts:
  if opt == '-h':
     print ('sma-daemon.py\n -c <configfile>\n -h show this help screen\n -v show version\n - ...')
     sys.exit()
  elif opt in ("-c", "--configfile"):
     configfile = arg
  elif opt =='-v':
     print ('sma-daemon.py \nVersion: 1.9. BETA\n (c) wenger florian\nlicense GNU GPL v2')
     sys.exit()
#print ('Configfile is "', configfile)


#check Configfile
if not os.access(configfile, os.R_OK):
    print ('configfile ',configfile, 'is not accessable')
    sys.exit(127)

if __name__ == '__main__':
  killer = GracefulKiller()
  #checkparameters
  configfile = '/etc/smaemd/config'
  try:
    opts, args = getopt.getopt(sys.argv[1:],"hc:v",["configfile=","ofile="])
  except getopt.GetoptError:
    print ('unknown options\nuse sma-daemon.py -c <configfile>\nor try -h for more options')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
       print ('sma-daemon.py\n -c <configfile>\n -h show this help screen\n -v show version\n - ...')
       sys.exit()
    elif opt in ("-c", "--configfile"):
       configfile = arg
    elif opt =='-v':
       print ('sma-daemon.py \nVersion: 1.9. BETA\n (c) wenger florian\nlicense GNU GPL v2')
       sys.exit()
  #check Configfile
  if not os.access(configfile, os.R_OK):
      print ('configfile ',configfile, 'is not accessable')
      sys.exit(127)
  #reading configs
  parser = SafeConfigParser()
  parser.read(configfile)
  smaemserials=parser.get('SMA-EM', 'serials')
  serials=smaemserials.split(' ')
  pidfile=parser.get('DAEMON', 'pidfile')
  ipbind=parser.get('DAEMON', 'ipbind')
  MCAST_GRP = parser.get('DAEMON', 'mcastgrp')
  MCAST_PORT = int(parser.get('DAEMON', 'mcastport'))
  features=parser.get('SMA-EM', 'features')
  features=features.split(' ')
  #set defaults
  if MCAST_GRP == "":
      MCAST_GRP = '239.12.255.254'
  if MCAST_PORT == 0:
      MCAST_PORT = 9522
  featurelist=startupfeatures()
  emparts = {}
  while True:
    #time.sleep(1)
    print("doing something in a loop ...")
    socketconnected = False
    while not socketconnected:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', MCAST_PORT))
        try:
            mreq = struct.pack("4s4s", socket.inet_aton(MCAST_GRP), socket.inet_aton(ipbind))
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            file = open("/run/shm/em-status", "w")
            file.write('multicastgroup connected')
            file.close()
            socketconnected = True
        except BaseException:
            print('could not connect to mulicast group... rest a bit and retry')
            file = open("/run/shm/em-status", "w")
            file.write('could not connect to mulicast group... rest a bit and retry')
            file.close()
            time.sleep(5)
    emparts=smaem.readem(sock)
    for serial in serials:
        # process only known sma serials
        if serial==format(emparts['serial']):
            for feature in featurelist:
                #print ('processing feature'+feature )
                featurelist[feature].run(emparts)
    if killer.kill_now:
      print('someone want me to stop working')
      for feature in featurelist:
        print ('stopping feature'+feature )
        featurelist[feature].cleanup()
      break

  print ("End of the program. I was killed gracefully ")
  sys.exit(0)


#def shutdownfeatures(featurelist):
#    #shutdown features (housekeeping)
#    print("shutdown features")
#    featurecounter=0
#    for feature in featurelist:
#        print(feature)
#        featurelist[feature].cleanup()



#Daemon - Coding
#if __name__ == "__main__":
#    daemon = MyDaemon(pidfile)
#    if len(sys.argv) == 2:
#        if 'start' == sys.argv[1]:
#            readconfig()
#            featurelist=startupfeatures()
#            daemon.enablefeatures(featurelist)
#            daemon.start()
#        elif 'stop' == sys.argv[1]:
#            #shutdownfeatures(featurelist)
#            daemon.stop()
#        elif 'restart' == sys.argv[1]:
#            #shutdownfeatures(featurelist)
#            readconfig()
#            featurelist=startupfeatures()
#            daemon.enablefeatures(featurelist)
#            daemon.restart()
#        elif 'run' == sys.argv[1]:
#            readconfig()
#            featurelist=startupfeatures()
#            print("running-the-system")
#            daemon.enablefeatures(featurelist)
#            #daemon.run()
#            time.sleep(1)
#            #shutdownfeatures(featurelist)
#            daemon.stop()
#        else:
#            print ("SMA-EM Daemon\nUnknown command")
#            sys.exit(2)
#        sys.exit(0)
#    else:
#        print ("SMA-EM Daemon\nusage: %s start|stop|restart|run" % sys.argv[0])
#        print (pidfile)
#        sys.exit(2)
