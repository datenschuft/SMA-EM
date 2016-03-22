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
import socket
import struct
import binascii


# listen to the Multicast; SMA-Energymeter sends its measurements to 239.12.255.254:9522
MCAST_GRP = '239.12.255.254'
MCAST_PORT = 9522


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
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


def readem():  
  smainfo=sock.recv(600)
  smainfoasci=binascii.b2a_hex(smainfo)
  
  # split the received message to seperate vars
  # summary 
  # regard/Bezug=getting energy from main grid
  # surplus/surplus=putting energy to the main grid
  
  
  smaserial=hex2dec(smainfoasci[40:48])
  pregard=hex2dec(smainfoasci[64:72])/10
  pregardcounter=hex2dec(smainfoasci[80:96])/3600000
  psurplus=hex2dec(smainfoasci[104:112])/10
  psurpluscounter=hex2dec(smainfoasci[120:136])/3600000
  qregard=hex2dec(smainfoasci[144:152])/10
  qregardcounter=hex2dec(smainfoasci[160:176])/3600000
  qsurplus=hex2dec(smainfoasci[184:192])/10
  qsurpluscounter=hex2dec(smainfoasci[200:216])/3600000
  sregard=hex2dec(smainfoasci[224:232])/10
  sregardcounter=hex2dec(smainfoasci[240:256])/3600000
  ssurplus=hex2dec(smainfoasci[264:272])/10
  ssurpluscounter=hex2dec(smainfoasci[280:296])/3600000
  cosphi=hex2dec(smainfoasci[304:312])/1000
  #L1
  p1regard=hex2dec(smainfoasci[320:328])/10
  p1regardcounter=hex2dec(smainfoasci[336:352])/3600000
  p1surplus=hex2dec(smainfoasci[360:368])/10
  p1surpluscounter=hex2dec(smainfoasci[376:392])/3600000
  q1regard=hex2dec(smainfoasci[400:408])/10
  q1regardcounter=hex2dec(smainfoasci[416:432])/3600000
  q1surplus=hex2dec(smainfoasci[440:448])/10
  q1surpluscounter=hex2dec(smainfoasci[456:472])/3600000
  s1regard=hex2dec(smainfoasci[480:488])/10
  s1regardcounter=hex2dec(smainfoasci[496:512])/3600000
  s1surplus=hex2dec(smainfoasci[520:528])/10
  s1surpluscounter=hex2dec(smainfoasci[536:552])/3600000
  thd1=hex2dec(smainfoasci[560:568])/1000
  v1=hex2dec(smainfoasci[576:584])/1000
  cosphi1=hex2dec(smainfoasci[592:600])/1000
  #L2
  p2regard=hex2dec(smainfoasci[608:616])/10
  p2regardcounter=hex2dec(smainfoasci[624:640])/3600000
  p2surplus=hex2dec(smainfoasci[648:656])/10
  p2surpluscounter=hex2dec(smainfoasci[664:680])/3600000
  q2regard=hex2dec(smainfoasci[688:696])/10
  q2regardcounter=hex2dec(smainfoasci[704:720])/3600000
  q2surplus=hex2dec(smainfoasci[728:736])/10
  q2surpluscounter=hex2dec(smainfoasci[744:760])/3600000
  s2regard=hex2dec(smainfoasci[768:776])/10
  s2regardcounter=hex2dec(smainfoasci[784:800])/3600000
  s2surplus=hex2dec(smainfoasci[808:816])/10
  s2surpluscounter=hex2dec(smainfoasci[824:840])/3600000
  thd2=hex2dec(smainfoasci[848:856])/1000
  v2=hex2dec(smainfoasci[864:872])/1000
  cosphi2=hex2dec(smainfoasci[880:888])/1000
  #L3
  p3regard=hex2dec(smainfoasci[896:904])/10
  
  p3regardcounter=hex2dec(smainfoasci[912:928])/3600000
  p3surplus=hex2dec(smainfoasci[936:944])/10
  p3surpluscounter=hex2dec(smainfoasci[952:968])/3600000
  q3regard=hex2dec(smainfoasci[976:984])/10
  q3regardcounter=hex2dec(smainfoasci[992:1008])/3600000
  q3surplus=hex2dec(smainfoasci[1016:1024])/10
  q3surpluscounter=hex2dec(smainfoasci[1032:1048])/3600000
  s3regard=hex2dec(smainfoasci[1056:1064])/10
  s3regardcounter=hex2dec(smainfoasci[1072:1088])/3600000
  s3surplus=hex2dec(smainfoasci[1096:1104])/10
  s3surpluscounter=hex2dec(smainfoasci[1112:1128])/3600000
  thd3=hex2dec(smainfoasci[1136:1144])/1000
  v3=hex2dec(smainfoasci[1152:1160])/1000
  cosphi3=hex2dec(smainfoasci[1168:1176])/1000
  
  #Returning values
  emparts = {'serial':smaserial,'pregard':pregard,'pregardcounter':pregardcounter,'psurplus':psurplus,'psurpluscounter':psurpluscounter,
  'sregard':sregard,'sregardcounter':sregardcounter,'ssurplus':ssurplus,'ssurpluscounter':ssurpluscounter, 
  'qregard':qregard,'qregardcounter':qregardcounter,'qsurplus':qsurplus,'qsurpluscounter':qsurpluscounter,
  'cosphi':cosphi,
  'p1regard':p1regard,'p1regardcounter':p1regardcounter,'p1surplus':p1surplus,'p1surpluscounter':p1surpluscounter,
  's1regard':s1regard,'s1regardcounter':s1regardcounter,'s1surplus':s1surplus,'s1surpluscounter':s1surpluscounter,
  'q1regard':q1regard,'q1regardcounter':q1regardcounter,'q1surplus':q1surplus,'q1surpluscounter':q1surpluscounter,
  'v1':v1,'thd1':thd1,'cosphi1':cosphi1,
  'p2regard':p2regard,'p2regardcounter':p2regardcounter,'p2surplus':p2surplus,'p2surpluscounter':p2surpluscounter,
  's2regard':s2regard,'s2regardcounter':s2regardcounter,'s2surplus':s2surplus,'s2surpluscounter':s2surpluscounter,
  'q2regard':q2regard,'q2regardcounter':q2regardcounter,'q2surplus':q2surplus,'q2surpluscounter':q2surpluscounter,
  'v2':v2,'thd2':thd2,'cosphi2':cosphi2,
  'p3regard':p3regard,'p3regardcounter':p3regardcounter,'p3surplus':p3surplus,'p3surpluscounter':p3surpluscounter,
  's3regard':s3regard,'s3regardcounter':s3regardcounter,'s3surplus':s3surplus,'s3surpluscounter':s3surpluscounter,
  'q3regard':q3regard,'q3regardcounter':q3regardcounter,'q3surplus':q3surplus,'q3surpluscounter':q3surpluscounter,
  'v3':v3,'thd3':thd3,'cosphi3':cosphi3 }
  return emparts
  
