"""
 *
 * by david-m-m 2019-Mar-17
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

import binascii

# unit definitions with scaling
sma_units={
    "W":    0.1,
    "Wh":   1.0/3600.0,
    "A":    0.001,
    "V":    0.001,
    "cosphi": 0.001
}

# map of all defined SMA channels
# format: <channel_number>:(<name>,<emparts_name>,<unit_actual>,<unit_total>)
sma_channels={
    # totals
    1:('active_power_consumption','pconsume','W','Wh'),
    2:('active_power_supply','psupply','W','Wh'),
    3:('apparent_power_consumption','sconsume','W','Wh'),
    4:('apparent_power_supply','ssupply','W','Wh'),
    9:('reactive_power_consumption','qconsume','W','Wh'),
    10:('reactive_power_supply','qsupply','W','Wh'),
    13:('powerfactor','cosphi','cosphi'),
    # phase 1
    21:('p1_active_power_consumption','p1consume','W','Wh'),
    22:('p1_active_power_supply','p1supply','W','Wh'),
    23:('p1_apparent_power_consumption','s1consume','W','Wh'),
    24:('p1_apparent_power_supply','s1supply','W','Wh'),
    29:('p1_reactive_power_consumption','q1consume','W','Wh'),
    30:('p1_reactive_power_supply','q1supply','W','Wh'),
    31:('p1_current','thd1','A'),
    32:('p1_voltage','v1','V'),
    33:('p1_powerfactor','cosphi1','cosphi'),
    # phase 2
    41:('p2_active_power_consumption','p2consume','W','Wh'),
    42:('p2_active_power_supply','p2supply','W','Wh'),
    43:('p2_apparent_power_consumption','s2consume','W','Wh'),
    44:('p2_apparent_power_supply','s2supply','W','Wh'),
    49:('p2_reactive_power_consumption','q2consume','W','Wh'),
    50:('p2_reactive_power_supply','q2supply','W','Wh'),
    51:('p2_current','thd2','A'),
    52:('p2_voltage','v2','V'),
    53:('p2_powerfactor','cosphi2','cosphi'),
    # phase 3
    61:('p3_active_power_consumption','p3consume','W','Wh'),
    62:('p3_active_power_supply','p3supply','W','Wh'),
    63:('p3_apparent_power_consumption','s3consume','W','Wh'),
    64:('p3_apparent_power_supply','s3supply','W','Wh'),
    69:('p3_reactive_power_consumption','q3consume','W','Wh'),
    70:('p3_reactive_power_supply','q3supply','W','Wh'),
    71:('p3_current','thd3','A'),
    72:('p3_voltage','v3','V'),
    73:('p3_powerfactor','cosphi3','cosphi'),
}

def decode_OBIS(obis):
  measurement=int.from_bytes(obis[1:2], byteorder='big' )
  raw_type=int.from_bytes(obis[2:3], byteorder='big')
  if raw_type==4:
    datatype='actual'
  elif raw_type==8:
    datatype='counter'
  else:
    print("unknown datatype")
    datatype='unknown'

  return (measurement,datatype)

def decode_speedwire(datagram):
  emparts={}
  # process data only of SMA header is present
  if datagram[0:3]==b'SMA':
    # datagram length
    datalength=int.from_bytes(datagram[12:14],byteorder='big')+8
    # serial number
    emID=int.from_bytes(datagram[20:24],byteorder='big')
    emparts['serial']=emID
    # timestamp
    timestamp=int.from_bytes(datagram[24:28],byteorder='big')
    # decode OBIS data blocks
    # start with header
    position=28
    while position<datalength:
      # decode header
      (measurement,datatype)=decode_OBIS(datagram[position:position+4])
      # decode values
      # actual values
      if datatype=='actual':
        value=int.from_bytes( datagram[position+4:position+8], byteorder='big' )
        position+=8
        emparts[sma_channels[measurement][1]]=value*sma_units[sma_channels[measurement][2]]
      # counter values
      elif datatype=='counter':
        value=int.from_bytes( datagram[position+4:position+12], byteorder='big' )
        position+=12
        emparts[sma_channels[measurement][1]+'counter']=value*sma_units[sma_channels[measurement][3]]*0.001
      else:
        position+=8

  return emparts

