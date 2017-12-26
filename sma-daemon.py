#!/usr/bin/env python3
# coding=utf-8
"""
 *
 * by Wenger Florian 2017-12-28
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
from daemon3x import daemon3x
from configparser import SafeConfigParser
import urllib.request
from urllib.error import URLError
import json
import smaem
import socket
import struct


#read configuration
parser = SafeConfigParser()
parser.read('/etc/smaemd/config')

smaemserials=parser.get('SMA-EM', 'serials')
serials=smaemserials.split(' ')
smavalues=parser.get('SMA-EM', 'values')
values=filter(len, smavalues.split(' '))
pidfile=parser.get('DAEMON', 'pidfile')
ipbind=parser.get('DAEMON', 'ipbind')
MCAST_GRP = parser.get('DAEMON', 'mcastgrp')
MCAST_PORT = int(parser.get('DAEMON', 'mcastport'))

#set defaults
if MCAST_GRP == "":
    MCAST_GRP = '239.12.255.254'
if MCAST_PORT == 0:
    MCAST_PORT = 9522

domoticz = {}
for key in parser.sections():
	if key.startswith('DOMOTICZ-'):
		domoticz[key[9:]] = parser[key]

class MyDaemon(daemon3x):
	def run(self):
		# prepare listen to socket-Multicast
		socketconnected = False
		while not socketconnected:
			#try:
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
		emparts = {}
		while True:
			emparts=smaem.readem(sock)
			for serial in serials:
				#print(serial)
				#print(emparts['serial'])
				if serial==format(emparts['serial']):
					if serial in domoticz:
						dom = domoticz[serial]

                        # Only update every X seconds
						if time.time() < domoticz.get('last_update', 0) + int(domoticz.get('min_update', 20)):
							#print("skipping")
							continue
						domoticz['last_update'] = time.time()

						for key in dom:
							if key in ['api', 'min_update', 'last_update']:
								continue

							url = "%s?type=command&param=udevice&idx=%s&nvalue=0&svalue=" % (dom['api'], dom[key])
							if key in ['pregard', 'p1regard', 'p2regard', 'p3regard']:
								url += "%0.2f;%0.2f" % (emparts[key], emparts[key + "counter"] * 1000)
							else:
								url += "%0.2f" % emparts[key]

							#print(url)
							try:
								urllib.request.urlopen( url )
							except URLError as e:	   # ignore if domoticz was down
								print("Error from domoticz request")
								print(e)
								pass

					#print("match")
					for value in values:
						file = open("/run/shm/em-"+format(serial)+"-"+format(value), "w")
						file.write('%.4f' % emparts[value])
						file.close()

if __name__ == "__main__":
	daemon = MyDaemon(pidfile)
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		elif 'run' == sys.argv[1]:
			daemon.run()
		else:
			print ("Unknown command")
			sys.exit(2)
		sys.exit(0)
	else:
		print ("usage: %s start|stop|restart" % sys.argv[0])
		print (pidfile)
		sys.exit(2)
