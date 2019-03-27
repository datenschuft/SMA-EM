"""
 *
 * by Wenger Florian 2015-11-12
 * wenger@unifox.at
 *
 * by david-m-m 2019-03-20
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

#import socket
import struct
import binascii
import sys
from speedwiredecoder import * 

# listen to the Multicast; SMA-Energymeter sends its measurements to 239.12.255.254:9522
#MCAST_GRP = '239.12.255.254'
#MCAST_PORT = 9522

# function to transform HEX to DEC
def hex2dec(s):
    """return the integer value of a hexadecimal string s"""
    return int(s, 16)

# clean exit
def abortprogram(signal,frame):
    # Housekeeping -> nothing to cleanup
    print('STRG + C = end program')
    sys.exit(0)

# prepare listen to socket-Multicast
#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
#sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#sock.bind(('', MCAST_PORT))
#mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
#sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

def readem(sock):
  smainfo=sock.recv(600)
  smainfoasci=binascii.b2a_hex(smainfo)

  # split the received message to seperate vars

  emparts=decode_speedwire(smainfo)

  return emparts

