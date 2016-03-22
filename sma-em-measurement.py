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

import signal
import sys
import smaem

# clean exit
def abortprogram(signal,frame):
    # Housekeeping -> nothing to cleanup 
    print('STRG + C = end program')
    sys.exit(0)

# abort-signal
signal.signal(signal.SIGINT, abortprogram)

# processing received messages
while True:
  emparts = {}
  emparts=smaem.readem()
  #
  # Output...
  # don't know what P,Q and S means: 
  # http://en.wikipedia.org/wiki/AC_power or http://de.wikipedia.org/wiki/Scheinleistung
  # thd = Total_Harmonic_Distortion http://de.wikipedia.org/wiki/Total_Harmonic_Distortion
  # cos phi is always positive, no matter what quadrant 
  print ('\n')
  print ('SMA-EM Serial:{}'.format(emparts['serial']))
  print ('----sum----')
  print ('P: regard:{}W {}kWh surplus:{}W {}kWh'.format(emparts['pregard'],emparts['pregardcounter'],emparts['psurplus'],emparts['psurpluscounter']))
  print ('S: regard:{}VA {}kVAh surplus:{}VA {}VAh'.format(emparts['sregard'],emparts['sregardcounter'],emparts['ssurplus'],emparts['ssurpluscounter']))
  print ('Q: cap {}var {}kvarh ind {}var {}kvarh'.format(emparts['qregard'],emparts['qregardcounter'],emparts['qsurplus'],emparts['qsurpluscounter']))
  print ('cos phi:{}°'.format(emparts['cosphi']))
  print ('----L1----')
  print ('P: regard:{}W {}kWh surplus:{}W {}kWh'.format(emparts['p1regard'],emparts['p1regardcounter'],emparts['p1surplus'],emparts['p1surpluscounter']))
  print ('S: regard:{}VA {}kVAh surplus:{}VA {}kVAh'.format(emparts['s1regard'],emparts['s1regardcounter'],emparts['s1surplus'],emparts['s1surpluscounter']))
  print ('Q: cap {}var {}kvarh ind {}var {}kvarh'.format(emparts['q1regard'],emparts['q1regardcounter'],emparts['q1surplus'],emparts['q1surpluscounter']))
  print ('U: {}V thd:{}% cos phi:{}°'.format(emparts['v1'],emparts['thd1'],emparts['cosphi1']))
  print ('----L2----')
  print ('P: regard:{}W {}kWh surplus:{}W {}kWh'.format(emparts['p2regard'],emparts['p2regardcounter'],emparts['p2surplus'],emparts['p2surpluscounter']))
  print ('S: regard:{}VA {}kVAh surplus:{}VA {}kVAh'.format(emparts['s2regard'],emparts['s2regardcounter'],emparts['s2surplus'],emparts['s2surpluscounter']))
  print ('Q: cap {}var {}kvarh ind {}var {}kvarh'.format(emparts['q2regard'],emparts['q2regardcounter'],emparts['q2surplus'],emparts['q2surpluscounter']))
  print ('U: {}V thd:{}% cos phi:{}°'.format(emparts['v2'],emparts['thd2'],emparts['cosphi2']))
  print ('----L3----')
  print ('P: regard:{}W {}kWh surplus:{}W {}kWh'.format(emparts['p3regard'],emparts['p3regardcounter'],emparts['p3surplus'],emparts['p3surpluscounter']))
  print ('S: regard:{}VA {}kVAh surplus:{}VA {}kVAh'.format(emparts['s3regard'],emparts['s3regardcounter'],emparts['s3surplus'],emparts['s3surpluscounter']))
  print ('Q: cap {}var {}kvarh ind {}var {}kvarh'.format(emparts['q3regard'],emparts['q3regardcounter'],emparts['q3surplus'],emparts['q3surpluscounter']))
  print ('U: {}V thd:{}% cos phi:{}°'.format(emparts['v3'],emparts['thd3'],emparts['cosphi3']))
  
