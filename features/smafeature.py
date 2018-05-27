"""
 * Feature-Module for SMA-EM daemon
 * sample class for features
 * other features extends this class
 * by Wenger Florian 2018-05-27
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
class smafeature:
    def __init__(self):
        #print("initialisation of feature")
        self.__config = {}
    def loadconfig(self,config):
        self.__config = config
        print("----config----")
        print(self.__config)
        print("----config end----")
    def getconfig(self):
        return self.__config
    def run(self,emparts):
        print("prozessing emparts ... is not implemented !")
    def cleanup(self):
        print("cleanup housekeeping of feature ... is not implemented !")
