#!/usr/bin/env python3
# coding=utf-8
"""
 *
 * by Wenger Florian 2019-12-31
 * wenger@unifox.at
 *
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
 * 2018-12-22 Tommi2Day small enhancements
 * 2019-08-13 datenschuft run without config
 *
 */
"""

import signal
import sys
import smaem
import socket
import struct
import binascii
from configparser import ConfigParser

# clean exit
def abortprogram(signal,frame):
    # Housekeeping -> nothing to cleanup
    print('STRG + C = end program')
    sys.exit(0)

# abort-signal
signal.signal(signal.SIGINT, abortprogram)


#read configuration
parser = ConfigParser()
#default values
smaserials = ""
ipbind = '0.0.0.0'
MCAST_GRP = '239.12.255.254'
MCAST_PORT = 9522
parser.read(['/etc/smaemd/config','config'])
try:
    smaemserials=parser.get('SMA-EM', 'serials')
    ipbind=parser.get('DAEMON', 'ipbind')
    MCAST_GRP = parser.get('DAEMON', 'mcastgrp')
    MCAST_PORT = int(parser.get('DAEMON', 'mcastport'))
except:
    print('Cannot find config /etc/smaemd/config... using defaults')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))
try:
    mreq = struct.pack("4s4s", socket.inet_aton(MCAST_GRP), socket.inet_aton(ipbind))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
except BaseException:
    print('could not connect to mulicast group or bind to given interface')
    sys.exit(1)

# processing received messages
smainfo=sock.recv(1024)
smainfoasci=binascii.b2a_hex(smainfo)

print ('----raw-1024---')
print (smainfo)
print ('----asci---')
print (smainfoasci)
