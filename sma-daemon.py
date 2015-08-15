#!/usr/bin/python3
# coding=utf-8
"""
 * 
 * by Wenger Florian 2015-08-15
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
import smaem
  
class MyDaemon(daemon3x):
	def run(self):
		while True:
			time.sleep(1)
			#print ("1")
			#readem()
			smaem.readem()
  
if __name__ == "__main__":
	daemon = MyDaemon('/tmp/daemon-example.pid')
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
		sys.exit(2)
