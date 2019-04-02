"""
 *
 * by Wenger Florian 2015-11-12
 * wenger@unifox.at
 *
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
 */
"""
#import socket
import struct
import binascii
import sys



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
  # summary
  # consume/Bezug=getting energy from main grid
  # supply/supply=putting energy to the main grid


  smaserial=hex2dec(smainfoasci[40:48])
  pconsume=hex2dec(smainfoasci[64:72])/10
  pconsumecounter=hex2dec(smainfoasci[80:96])/3600000
  psupply=hex2dec(smainfoasci[104:112])/10
  psupplycounter=hex2dec(smainfoasci[120:136])/3600000
  qconsume=hex2dec(smainfoasci[144:152])/10
  qconsumecounter=hex2dec(smainfoasci[160:176])/3600000
  qsupply=hex2dec(smainfoasci[184:192])/10
  qsupplycounter=hex2dec(smainfoasci[200:216])/3600000
  sconsume=hex2dec(smainfoasci[224:232])/10
  sconsumecounter=hex2dec(smainfoasci[240:256])/3600000
  ssupply=hex2dec(smainfoasci[264:272])/10
  ssupplycounter=hex2dec(smainfoasci[280:296])/3600000
  cosphi=hex2dec(smainfoasci[304:312])/1000
  #L1
  p1consume=hex2dec(smainfoasci[320:328])/10
  p1consumecounter=hex2dec(smainfoasci[336:352])/3600000
  p1supply=hex2dec(smainfoasci[360:368])/10
  p1supplycounter=hex2dec(smainfoasci[376:392])/3600000
  q1consume=hex2dec(smainfoasci[400:408])/10
  q1consumecounter=hex2dec(smainfoasci[416:432])/3600000
  q1supply=hex2dec(smainfoasci[440:448])/10
  q1supplycounter=hex2dec(smainfoasci[456:472])/3600000
  s1consume=hex2dec(smainfoasci[480:488])/10
  s1consumecounter=hex2dec(smainfoasci[496:512])/3600000
  s1supply=hex2dec(smainfoasci[520:528])/10
  s1supplycounter=hex2dec(smainfoasci[536:552])/3600000
  thd1=hex2dec(smainfoasci[560:568])/1000
  v1=hex2dec(smainfoasci[576:584])/1000
  cosphi1=hex2dec(smainfoasci[592:600])/1000
  #L2
  p2consume=hex2dec(smainfoasci[608:616])/10
  p2consumecounter=hex2dec(smainfoasci[624:640])/3600000
  p2supply=hex2dec(smainfoasci[648:656])/10
  p2supplycounter=hex2dec(smainfoasci[664:680])/3600000
  q2consume=hex2dec(smainfoasci[688:696])/10
  q2consumecounter=hex2dec(smainfoasci[704:720])/3600000
  q2supply=hex2dec(smainfoasci[728:736])/10
  q2supplycounter=hex2dec(smainfoasci[744:760])/3600000
  s2consume=hex2dec(smainfoasci[768:776])/10
  s2consumecounter=hex2dec(smainfoasci[784:800])/3600000
  s2supply=hex2dec(smainfoasci[808:816])/10
  s2supplycounter=hex2dec(smainfoasci[824:840])/3600000
  thd2=hex2dec(smainfoasci[848:856])/1000
  v2=hex2dec(smainfoasci[864:872])/1000
  cosphi2=hex2dec(smainfoasci[880:888])/1000
  #L3
  p3consume=hex2dec(smainfoasci[896:904])/10

  p3consumecounter=hex2dec(smainfoasci[912:928])/3600000
  p3supply=hex2dec(smainfoasci[936:944])/10
  p3supplycounter=hex2dec(smainfoasci[952:968])/3600000
  q3consume=hex2dec(smainfoasci[976:984])/10
  q3consumecounter=hex2dec(smainfoasci[992:1008])/3600000
  q3supply=hex2dec(smainfoasci[1016:1024])/10
  q3supplycounter=hex2dec(smainfoasci[1032:1048])/3600000
  s3consume=hex2dec(smainfoasci[1056:1064])/10
  s3consumecounter=hex2dec(smainfoasci[1072:1088])/3600000
  s3supply=hex2dec(smainfoasci[1096:1104])/10
  s3supplycounter=hex2dec(smainfoasci[1112:1128])/3600000
  thd3=hex2dec(smainfoasci[1136:1144])/1000
  v3=hex2dec(smainfoasci[1152:1160])/1000
  cosphi3=hex2dec(smainfoasci[1168:1176])/1000

  #Returning values
  emparts = {'serial':smaserial,'pconsume':pconsume,'pconsumecounter':pconsumecounter,'psupply':psupply,'psupplycounter':psupplycounter,
  'sconsume':sconsume,'sconsumecounter':sconsumecounter,'ssupply':ssupply,'ssupplycounter':ssupplycounter,
  'qconsume':qconsume,'qconsumecounter':qconsumecounter,'qsupply':qsupply,'qsupplycounter':qsupplycounter,
  'cosphi':cosphi,
  'p1consume':p1consume,'p1consumecounter':p1consumecounter,'p1supply':p1supply,'p1supplycounter':p1supplycounter,
  's1consume':s1consume,'s1consumecounter':s1consumecounter,'s1supply':s1supply,'s1supplycounter':s1supplycounter,
  'q1consume':q1consume,'q1consumecounter':q1consumecounter,'q1supply':q1supply,'q1supplycounter':q1supplycounter,
  'v1':v1,'thd1':thd1,'cosphi1':cosphi1,
  'p2consume':p2consume,'p2consumecounter':p2consumecounter,'p2supply':p2supply,'p2supplycounter':p2supplycounter,
  's2consume':s2consume,'s2consumecounter':s2consumecounter,'s2supply':s2supply,'s2supplycounter':s2supplycounter,
  'q2consume':q2consume,'q2consumecounter':q2consumecounter,'q2supply':q2supply,'q2supplycounter':q2supplycounter,
  'v2':v2,'thd2':thd2,'cosphi2':cosphi2,
  'p3consume':p3consume,'p3consumecounter':p3consumecounter,'p3supply':p3supply,'p3supplycounter':p3supplycounter,
  's3consume':s3consume,'s3consumecounter':s3consumecounter,'s3supply':s3supply,'s3supplycounter':s3supplycounter,
  'q3consume':q3consume,'q3consumecounter':q3consumecounter,'q3supply':q3supply,'q3supplycounter':q3supplycounter,
  'v3':v3,'thd3':thd3,'cosphi3':cosphi3 }
  return emparts
