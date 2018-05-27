"""
 * Feature-Module for SMA-EM daemon
 * condensed measurement logger
 * by Wenger Florian 2018-03-25
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

def run(emparts,config):
    print("running feature condensedlogger")
    values=config['values'].split(' ')
    serials=config['serials'].split(' ')
    for serial in serials:
        if serial==format(emparts['serial']):
            for value in values:
                #print ("-"+format(value)+('%.4f' % emparts[value]))
                #print (value)
                file = open("/run/shm/em-"+format(serial)+"-"+format(value), "w")
                file.write('%.4f' % emparts[value])
                file.close()

def stopping(emparts,config):
    print("quitting")
    #close files
