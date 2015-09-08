#!/usr/bin/python3
# coding=utf-8
"""
 * 
 * by Wenger Florian 2015-09-02
 * wenger@unifox.at
 *
 * endless loop (until ctrl+c) displays measurement from SMA Energymeter
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
import signal
import sys

# listen to the broadcasts; SMA-Energymeter sends its measurements to 239.12.255.254:9522
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

# abort-signal
signal.signal(signal.SIGINT, abortprogram)
    
    
# prepare listen to socket-Multicast
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


# processing received messages
while True:
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
  #
  # Output...
  # don't know what P,Q and S means: 
  # http://en.wikipedia.org/wiki/AC_power or http://de.wikipedia.org/wiki/Scheinleistung
  # thd = Total_Harmonic_Distortion http://de.wikipedia.org/wiki/Total_Harmonic_Distortion
  # cos phi is always positive, no matter what quadrant 
  print ('\n')
  print ('SMA-EM Serial:{}'.format(smaserial))
  # print ('NOTE: I\'m not sure about the direction of Q (cap. ind.)')
  print ('----sum----')
  print ('P: regard:{}W {}kWh surplus:{}W {}kWh'.format(pregard,pregardcounter,psurplus,psurpluscounter))
  print ('S: regard:{}VA {}kVAh surplus:{}VA {}VAh'.format(sregard,sregardcounter,ssurplus,ssurpluscounter))
  print ('Q: cap {}var {}kvarh ind {}var {}kvarh'.format(qregard,qregardcounter,qsurplus,qsurpluscounter))
  print ('cos phi:{}°'.format(cosphi))
  print ('----L1----')
  print ('P: regard:{}W {}kWh surplus:{}W {}kWh'.format(p1regard,p1regardcounter,p1surplus,p1surpluscounter))
  print ('S: regard:{}VA {}kVAh surplus:{}VA {}kVAh'.format(s1regard,s1regardcounter,s1surplus,s1surpluscounter))
  print ('Q: cap {}var {}kvarh ind {}var {}kvarh'.format(q1regard,q1regardcounter,q1surplus,q1surpluscounter))
  print ('U: {}V thd:{}% cos phi:{}°'.format(v1,thd1,cosphi1))
  print ('----L2----')
  print ('P: regard:{}W {}kWh surplus:{}W {}kWh'.format(p2regard,p2regardcounter,p2surplus,p2surpluscounter))
  print ('S: regard:{}VA {}kVAh surplus:{}VA {}kVAh'.format(s2regard,s2regardcounter,s2surplus,s2surpluscounter))
  print ('Q: cap {}var {}kvarh ind {}var {}kvarh'.format(q2regard,q2regardcounter,q2surplus,q2surpluscounter))
  print ('U: {}V thd:{}% cos phi:{}°'.format(v2,thd2,cosphi2))
  print ('----L3----')
  print ('P: regard:{}W {}kWh surplus:{}W {}kWh'.format(p3regard,p3regardcounter,p3surplus,p3surpluscounter))
  print ('S: regard:{}VA {}kVAh surplus:{}VA {}kVAh'.format(s3regard,s3regardcounter,s3surplus,s3surpluscounter))
  print ('Q: cap {}var {}kvarh ind {}var {}kvarh'.format(q3regard,q3regardcounter,q3surplus,q3surpluscounter))
  print ('U: {}V thd:{}% cos phi:{}°'.format(v3,thd3,cosphi3))
