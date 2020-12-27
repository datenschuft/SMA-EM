"""
 * Feature-Module for SMA-EM daemon
 * Simple measurement to file writer
 * by Wenger Florian 2018-01-30
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

import os,time
sw_debug=0

def run(emparts,config):
    global sw_debug
    values=config['values'].split(' ')
    serials=config['serials'].split(' ')
    statusdir = config.get('statusdir','')
    #prefere shm
    if (statusdir==''):
        statusdir="/run/shm/"
    #fallback to local dir
    if not os.path.isdir(statusdir):
        statusdir=''
    for serial in serials:
        if serial==format(emparts['serial']):
            ts=(format(time.strftime("%H:%M:%S", time.localtime())))
            for value in values:
                if value in emparts.keys():
                    if sw_debug >0:
                        print ('simplewriter: '+ts+" - "+format(value)+': '+('%.4f' % emparts[value]))
                    file = open(statusdir+"em-"+format(serial)+"-"+format(value), "w")
                    file.write('%.4f' % emparts[value])
                    file.close()
                elif sw_debug > 0:
                    print ('simplefswriter: could not find value for '+format(value))

def stopping(emparts,config):
    print("quitting")
    #close files
def config(config):
    global sw_debug
    sw_debug = int(config.get('debug', 0))
    print("simplefswriter: feature enabled")
