#!/usr/bin/env python

# Copyright 2009  Steve Conklin 
# steve at conklinhouse dot com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.


# This software emulates the external floppy disk drive used
# by the Brother Electroknit KH-930E computerized knitting machine.
# It may work for other models, but has only been tested with the
# Brother KH-930E
#
# This emulates the disk drive and stores the saved data from
# the knitting machine on the linux file system. It does not
# read or write floppy disks.
#
# The disk drive used by the brother knitting machine is the same
# as a Tandy PDD1 drive. This software does not support the entire
# command API of the PDD1, only what is required for the knitting
# machine.
#

#
# Notes about data storage:
#
# The external floppy disk is formatted with 80 sectors of 1024
# bytes each. These sectors are numbered (internally) from 0-79.
# When starting this emulator, a base directory is specified.
# In this directory the emulator creates 80 files, one for each
# sector. These are kept sync'd with the emulator's internal
# storage of the same sectors. For each sector, there are two
# files, nn.dat, and nn.id, where 00 <= nn <= 79.
#
# The knitting machine uses two sectors for each saved set of
# information, which are referred to in the knitting machine
# manual as 'tracks' (which they were on the floppy disk). Each
# pair of even/odd numbered sectors is a track. Tracks are
# numbered 1-40. The knitting machine always writes sectors
# in even/odd pairs, and when the odd sector is written, both
# sectors are concatenated to a file named fileqq.dat, where
# qq is the sector number.
#

# The Knitting machine does not parse the returned hex ascii values
# unless they are ALL UPPER CASE. Lower case characters a-f appear
# to parse az zeros.

# You will need the (very nice) pySerial module, found here:
# http://pyserial.wiki.sourceforge.net/pySerial

import sys
import os
import os.path
import string
from array import *
import serial

version = '2.0'

#
# Note that this code makes a fundamental assumption which
# is only true for the disk format used by the brother knitting
# machine, which is that there is only one logical sector (LS) per
# physical sector (PS). The PS size is fixed at 1280 bytes, and
# the brother uses a LS size of 1024 bytes, so only one can fit.
#

class DiskSector():
    def __init__(self, fn):
        self.sectorSz = 1024
        self.idSz = 12
        self.data = ''
        self.id = ''
        #self.id = array('c')

        dfn = fn + ".dat"
        idfn = fn + ".id"

        try:
            try:
                self.df = open(dfn, 'r+')
            except IOError:
                self.df = open(dfn, 'w')

            try:
                self.idf = open(idfn, 'r+')
            except IOError:
                self.idf = open(idfn, 'w')

            dfs = os.path.getsize(dfn)
            idfs = os.path.getsize(idfn)

        except:
            print 'Unable to open files using base name <%s>' % fn
            raise

        try:
            if dfs == 0:
                # New or empty file
                self.data = ''.join([chr(0) for num in xrange(self.sectorSz)])
                self.writeDFile()
            elif dfs == self.sectorSz:
                # Existing file
                self.data = self.df.read(self.sectorSz)
            else:
                print 'Found a data file <%s> with the wrong size' % dfn
                raise IOError
        except:
            print 'Unable to handle data file <%s>' % fn
            raise

        try:
            if idfs == 0:
                # New or empty file
                self.id = ''.join([chr(0) for num in xrange(self.idSz)])
                self.writeIdFile()
            elif idfs == self.idSz:
                # Existing file
                self.id = self.idf.read(self.idSz)
            else:
                print 'Found an ID file <%s> with the wrong size, is %d should be %d' % (idfn, idfs, self.idSz)
                raise IOError
        except:
            print 'Unable to handle id file <%s>' % fn
            raise

        return

    def __del__(self):
        return

    def format(self):
        self.data = ''.join([chr(0) for num in xrange(self.sectorSz)])
        self.writeDFile()
        self.id = ''.join([chr(0) for num in xrange(self.idSz)])
        self.writeIdFile()

    def writeDFile(self):
        self.df.seek(0)
        self.df.write(self.data)
        self.df.flush()
        return

    def writeIdFile(self):
        self.idf.seek(0)
        self.idf.write(self.id)
        self.idf.flush()
        return

    def read(self, length):
        if length != self.sectorSz:
            print 'Error, read of %d bytes when expecting %d' % (length, self.sectorSz)
            raise IOError
        return self.data

    def write(self, indata):
        if len(indata) != self.sectorSz:
            print 'Error, write of %d bytes when expecting %d' % (len(indata), self.sectorSz)
            raise IOError
        self.data = indata
        self.writeDFile()
        return

    def getSectorId(self):
        return self.id

    def setSectorId(self, newid):
        if len(newid) != self.idSz:
            print 'Error, bad id length of %d bytes when expecting %d' % (len(newid), self.id)
            raise IOError
        self.id = newid
        self.writeIdFile()
        print 'Wrote New ID: ',
        self.dumpId()
        return

    def dumpId(self):
        for i in self.id:
            print '%02X ' % ord(i),
        print

class Disk():
    """
    Fields:
        self.lastDatFilePath : string
    """
    
    def __init__(self, basename):
        self.numSectors = 80
        self.Sectors = []
        self.filespath = ""
        ""
        self.lastDatFilePath = None
        # Set up disk Files and internal buffers

        # if absolute path, just accept it
        if os.path.isabs(basename):
            dirpath = basename
        else:
            dirpath = os.path.abspath(basename)

        if os.path.exists(dirpath):
            if not os.access(dirpath, os.R_OK | os.W_OK):
                print 'Directory <%s> exists but cannot be accessed, check permissions' % dirpath
                raise IOError
            elif not os.path.isdir(dirpath):
                print 'Specified path <%s> exists but is not a directory' % dirpath
                raise IOError
        else:
            try:
                os.mkdir(dirpath)
            except:
                print 'Unable to create directory <%s>' % dirpath
                raise IOError

        self.filespath = dirpath
        # we have a directory now - set up disk sectors
        for i in range(self.numSectors):
            fname = os.path.join(dirpath, '%02d' % i)
            ds = DiskSector(fname)
            self.Sectors.append(ds)
        return

    def __del__(self):
        return

    def format(self):
        for i in range(self.numSectors):
            self.Sectors[i].format()
        return

    def findSectorID(self, psn, id):
        for i in range(psn, self.numSectors):
            sid = self.Sectors[i].getSectorId()
            if id == sid:
                return '00' + '%02X' % i + '0000'
        return '40000000'

    def getSectorID(self, psn):
        return self.Sectors[psn].getSectorId()

    def setSectorID(self, psn, id):
        self.Sectors[psn].setSectorId(id)
        return

    def writeSector(self, psn, lsn, indata):
        self.Sectors[psn].write(indata)
        if psn % 2:
            filenum =  ((psn-1)/2)+1
            filename =  'file-%02d.dat' % filenum
            # we wrote an odd sector, so create the
            # associated file
            fn1 = os.path.join(self.filespath, '%02d.dat' % (psn-1))
            fn2 = os.path.join(self.filespath, '%02d.dat' % psn)
            outfn =  os.path.join(self.filespath, filename)
            cmd = 'cat %s %s > %s' % (fn1, fn2, outfn)
            os.system(cmd)
            self.lastDatFilePath = outfn
        return

    def readSector(self, psn, lsn):
        return self.Sectors[psn].read(1024)

class PDDemulator():

    def __init__(self, basename):
        self.listeners = [] # list of PDDEmulatorListener
        self.verbose = True
        self.noserial = False
        self.ser = None
        self.disk = Disk(basename)
        self.FDCmode = False
        # bytes per logical sector
        self.bpls = 1024
        self.formatLength = {'0':64, '1':80, '2': 128, '3': 256, '4': 512, '5': 1024, '6': 1280}
        return

    def __del__(self):
        return

    def open(self, cport='/dev/ttyUSB0'):
        if self.noserial is False:
            self.ser = serial.Serial(port=cport, baudrate=9600, parity='N', stopbits=1, timeout=1, xonxoff=0, rtscts=0, dsrdtr=0)
#            self.ser.setRTS(True)
            if self.ser == None:
                print 'Unable to open serial device %s' % cport
                raise IOError
        return

    def close(self):
        if self.noserial is not False:
            if ser:
                ser.close()
        return

    def dumpchars(self):
        num = 1
        while 1:
            inc = self.ser.read()
            if len(inc) != 0:
                print 'flushed 0x%02X (%d)' % (ord(inc), num)
                num = num + 1
            else:
                break
        return

    def readsomechars(self, num):
        sch =  self.ser.read(num)
        return sch

    def readchar(self):
        inc = ''
        while len(inc) == 0:
            inc = self.ser.read()
        return inc
            
    def writebytes(self, bytes):
        self.ser.write(bytes)
        return

    def readFDDRequest(self):
        inbuf = []
        # read through a carriage return
        # parameters are seperated by commas
        while 1:
            inc = self.readchar()
            if inc == '\r':
                break
            elif inc == ' ':
                continue
            else:
                inbuf.append(inc)

        all = string.join(inbuf, '')
        rv =  all.split(',')
        return rv

    def getPsnLsn(self, info):
        psn = 0
        lsn = 1
        if len(info) >= 1 and info[0] != '':
            val = int(info[0])
            if psn <= 79:
                psn = val
        if len(info) > 1 and info[1] != '':
            val = int(info[0])
        return psn, lsn

    def readOpmodeRequest(self, req):
        buff = array('b')
        sum = req
        reqlen = ord(self.readchar())
        buff.append(reqlen)
        sum = sum + reqlen

        for x in range(reqlen, 0, -1):
            rb = ord(self.readchar())
            buff.append(rb)
            sum = sum + rb

        # calculate ckecksum
        sum = sum % 0x100
        sum = sum ^ 0xFF

        cksum = ord(self.readchar())
        
        if cksum == sum:
            return buff
        else:
            if self.verbose:
                print 'Checksum mismatch!!'
            return None

    def handleRequests(self):
        synced = False
        while True:
            self.handleRequest()
        # never returns
        return

    def handleRequest(self, blocking = True):
        if not blocking:
            if self.ser.inWaiting() == 0:
                return
        inc = self.readchar()
        if self.FDCmode:
            self.handleFDCmodeRequest(inc)
        else:
            # in OpMode, look for ZZ
            #inc = self.readchar()
            if inc != 'Z':
                return
            inc = self.readchar()
            if inc == 'Z':
                self.handleOpModeRequest()

    def handleOpModeRequest(self):
        req = ord(self.ser.read())
        print 'Request: 0X%02X' % req
        if req == 0x08:
            # Change to FDD emulation mode (no data returned)
            inbuf = self.readOpmodeRequest(req)
            if inbuf != None:
                # Change Modes, leave any incoming serial data in buffer
                self.FDCmode = True
        else:
            print 'Invalid OpMode request code 0X%02X received' % req
        return

    def handleFDCmodeRequest(self, cmd):
        # Commands may be followed by an optional space
        # PSN (physical sector) range 0-79
        # LSN (logical sector) range 0-(number of logical sectors in a physical sector)
        # LSN defaults to 1 if not supplied
        #
        # Result code information (verbatim from the Tandy reference):
        #
        # After the drive receives a command in FDC-emulation mode, it transmits
        # 8 byte characters which represent 4 bytes of status code in hexadecimal.
        #
        # * The first and second bytes contain the error status. A value of '00'
        #   indicates that no error occurred
        #
        # * The third and fourth bytes usually contain the number of the physical
        #   sector where data is kept in the buffer
        #
        #   For the D, F, and S commands, the contents of these bytes are different.
        #   See the command descriptions in these cases.
        #
        # * The fifth-eighth bytes usual show the logical sector length of the data
        #   kept in the RAM buffer, except the third and fourth digits are 'FF'
        #
        #   In the case of an S, C, or M command -- or an F command that ends in
        #   an error -- the bytes contain '0000'
        #

        if cmd == '\r':
            return

        if cmd == 'Z':
            # Hmmm, looks like we got the start of an Opmode Request
            inc = self.readchar()
            if inc == 'Z':
                # definitely!
                print 'Detected Opmode Request in FDC Mode, switching to OpMode'
                self.FDCmode = False
                self.handleOpModeRequest()

        elif cmd == 'M':
            # apparently not used by brother knitting machine
            print 'FDC Change Modes'
            raise
            # following parameter - 0=FDC, 1=Operating

        elif cmd == 'D':
            # apparently not used by brother knitting machine
            print 'FDC Check Device'
            raise
            # Sends result in third and fourth bytes of result code
            # See doc - return zero for disk installed and not swapped

        elif cmd == 'F'or cmd == 'G':
            #rint 'FDC Format',
            info = self.readFDDRequest()

            if len(info) != 1:
                print 'wrong number of params (%d) received, assuming 1024 bytes per sector' % len(info)
                bps = 1024
            else:
                try:
                    bps = self.formatLength[info[0]]
                except KeyError:
                    print 'Invalid code %c for format, assuming 1024 bytes per sector' % info[0]
                    bps = 1024
            # we assume 1024 because that's what the brother machine uses
            if self.bpls != bps:
                print 'Bad news, differing sector sizes'
                self.bpls = bps

            self.disk.format()

            # But this is probably more correct
            self.writebytes('00000000')

            # After a format, we always start out with OPMode again
            self.FDCmode = False

        elif cmd == 'A':
            # Followed by physical sector number (0-79), defaults to 0
            # returns ID data, not sector data
            info = self.readFDDRequest()
            psn, lsn = self.getPsnLsn(info)
            print 'FDC Read ID Section %d' % psn
            
            try:
                id = self.disk.getSectorID(psn)
            except:
                print 'Error getting Sector ID %d, quitting' % psn
                self.writebytes('80000000')
                raise

            self.writebytes('00' + '%02X' % psn + '0000')

            # see whether to send data
            go = self.readchar()
            if go == '\r':
                self.writebytes(id)

        elif cmd == 'R':
            # Followed by Physical Sector Number PSN and Logical Sector Number LSN
            info = self.readFDDRequest()
            psn, lsn = self.getPsnLsn(info)
            print 'FDC Read one Logical Sector %d' % psn
            
            try:
                sd = self.disk.readSector(psn, lsn)
            except:
                print 'Failed to read Sector %d, quitting' % psn
                self.writebytes('80000000')
                raise

            self.writebytes('00' + '%02X' % psn + '0000')

            # see whether to send data
            go = self.readchar()
            if go == '\r':
                self.writebytes(sd)

        elif cmd == 'S':
            # We receive (optionally) PSN, (optionally) LSN
            # This is not documented well at all in the manual
            # What is expected is that all sectors will be searched
            # and the sector number of the first matching sector
            # will be returned. The brother machine always sends
            # PSN = 0, so it is unknown whether searching should
            # start at Sector 0 or at the PSN sector
            info = self.readFDDRequest()
            psn, lsn = self.getPsnLsn(info)
            print 'FDC Search ID Section %d' % psn

            # Now we must send status (success)
            self.writebytes('00' + '%02X' % psn + '0000')

            #self.writebytes('00000000')

            # we receive 12 bytes here
            # compare with the specified sector (formatted is apparently zeros)
            id = self.readsomechars(12)
            print 'checking ID for sector %d' % psn

            try:
                status = self.disk.findSectorID(psn, id)
            except:
                print "FAIL"
                status = '30000000'
                raise

            print 'returning %s' % status
                    # guessing - doc is unclear, but says that S always ends in 0000
                    # MATCH 00000000
                    # MATCH 02000000
                    # infinite retries 10000000
                    # infinite retries 20000000
                    # blinking error 30000000
                    # blinking error 40000000
                    # infinite retries 50000000
                    # infinite retries 60000000
                    # infinite retries 70000000
                    # infinite retries 80000000

            self.writebytes(status)

            # Stay in FDC mode

        elif cmd == 'B' or cmd == 'C':
            # Followed by PSN 0-79, defaults to 0
            # When received, send result status, if not error, wait
            # for data to be written, then after write, send status again
            info = self.readFDDRequest()
            psn, lsn = self.getPsnLsn(info)
            print 'FDC Write ID section %d' % psn

            self.writebytes('00' + '%02X' % psn + '0000')

            id = self.readsomechars(12)

            try:
                self.disk.setSectorID(psn, id)
            except:
                print 'Failed to write ID for sector %d, quitting' % psn
                self.writebytes('80000000')
                raise

            self.writebytes('00' + '%02X' % psn + '0000')

        elif cmd == 'W' or cmd == 'X':
            info = self.readFDDRequest()
            psn, lsn = self.getPsnLsn(info)
            print 'FDC Write logical sector %d' % psn

            # Now we must send status (success)
            self.writebytes('00' + '%02X' % psn + '0000')

            indata = self.readsomechars(1024)
            try:
                self.disk.writeSector(psn, lsn, indata)
                for l in self.listeners:
                    l.dataReceived(self.disk.lastDatFilePath)
                print 'Saved data in dat file: ', self.disk.lastDatFilePath
            except:
                print 'Failed to write data for sector %d, quitting' % psn
                self.writebytes('80000000')
                raise

            self.writebytes('00' + '%02X' % psn + '0000')

        else:
            print 'Unknown FDC command <0x02%X> received' % ord(cmd)

        # return to Operational Mode
        return

class PDDEmulatorListener:
    def dataReceived(self, fullFilePath):
        pass
        
# meat and potatos here

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print '%s version %s' % (sys.argv[0], version)
        print 'Usage: %s basedir serialdevice' % sys.argv[0]
        sys.exit()

    print 'Preparing . . . Please Wait'
    emu = PDDemulator(sys.argv[1])

    emu.open(cport=sys.argv[2])

    print 'Emulator Ready!'
    try:
        while 1:
            emu.handleRequests()
    except (KeyboardInterrupt):
        pass

    emu.close()
