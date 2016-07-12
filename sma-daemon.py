#!/usr/bin/python3
# coding=utf-8
"""
 *
 * by Wenger Florian 2016-07-12
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
import smaem

#read configuration
parser = SafeConfigParser()
parser.read('/etc/smaemd/config')

smaemserials=parser.get('SMA-EM', 'serials')
serials=smaemserials.split(' ')
smavalues=parser.get('SMA-EM', 'values')
values=smavalues.split(' ')
pidfile=parser.get('DAEMON', 'pidfile')

class MyDaemon(daemon3x):
	def run(self):
		emparts = {}
		while True:
			emparts=smaem.readem()
			for serial in serials:
				#print(serial)
				#print(emparts['serial'])
				if serial==format(emparts['serial']):
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
		else:
			print ("Unknown command")
			sys.exit(2)
		sys.exit(0)
	else:
		print ("usage: %s start|stop|restart" % sys.argv[0])
		print (pidfile)
		sys.exit(2)
