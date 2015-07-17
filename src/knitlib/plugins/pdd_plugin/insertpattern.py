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

import sys
import brother
import Image
import array

# import convenience functions from brother module
from brother import roundeven, roundfour, roundeight, nibblesPerRow, bytesPerPattern, bytesForMemo, methodWithPointers

TheImage = None

version = '1.0'

class PatternInserter:
    def __init__(self):
        self.printInfoCallback = self.printInfo
        self.printErrorCallback = self.printError
        self.printPatternCallback = self.printPattern
        
    def printInfo(self, printMsg):
        print printMsg

    def printError(self, printMsg):
        print printMsg

    def printPattern(self, printMsg):
        sys.stdout.write(printMsg)

    def insertPattern(self, oldbrotherfile, pattnum, imgfile, newbrotherfile):

        bf = brother.brotherFile(oldbrotherfile)

        pats = bf.getPatterns()

        # ok got a bank, now lets figure out how big this thing we want to insert is
        TheImage = Image.open(imgfile)
        TheImage.load()

        im_size = TheImage.size
        width = im_size[0]
        self.printInfoCallback( "width:" + str(width))
        height = im_size[1]
        self.printInfoCallback( "height:" +  str(height))



        # find the program entry
        thePattern = None

        for pat in pats:
            if (int(pat["number"]) == int(pattnum)):
                #print "found it!"
                thePattern = pat
        if (thePattern == None):
            raise PatternNotFoundException(pattnum)

        if (height != thePattern["rows"] or width != thePattern["stitches"]):
            raise InserterException("Pattern is the wrong size, the BMP is ",height,"x",width,"and the pattern is ",thePattern["rows"], "x", thePattern["stitches"])

        # debugging stuff here
        x = 0
        y = 0

        x = width - 1
        for y in xrange(height):
            for x in xrange(width):
                value = TheImage.getpixel((x,y))
                if value:
                    self.printPattern('* ')
                else:
                    self.printPattern('  ')
            print " "

        # debugging stuff done

        # now to make the actual, yknow memo+pattern data

        # the memo seems to be always blank. i have no idea really
        memoentry = []
        for i in range(bytesForMemo(height)):
            memoentry.append(0x0)

        # now for actual real live pattern data!
        pattmemnibs = []
        for r in range(height):
            row = []  # we'll chunk in bits and then put em into nibbles
            for s in range(width):
                x = s if methodWithPointers else width-s-1
                value = TheImage.getpixel((x,height-r-1))
                isBlack = (value == 0) if methodWithPointers else (value != 0)
                if (isBlack):
                    row.append(1)
                else:
                    row.append(0)
            #print row
            # turn it into nibz
            for s in range(roundfour(width) / 4):
                n = 0
                for nibs in range(4):
                    #print "row size = ", len(row), "index = ",s*4+nibs

                    if (len(row) == (s*4+nibs)):
                        break       # padding!
                    
                    if (row[s*4 + nibs]):
                        n |= 1 << nibs
                pattmemnibs.append(n)
                #print hex(n),


        if (len(pattmemnibs) % 2):
            # odd nibbles, buffer to a byte
            pattmemnibs.append(0x0)

        #print len(pattmemnibs), "nibbles of data"

        # turn into bytes
        pattmem = []
        for i in range (len(pattmemnibs) / 2):
            pattmem.append( pattmemnibs[i*2] | (pattmemnibs[i*2 + 1] << 4))

        #print map(hex, pattmem)
        # whew. 


        # now to insert this data into the file 

        # now we have to figure out the -end- of the last pattern is
        endaddr = 0x6df

        beginaddr = thePattern["pattend"]
        endaddr = beginaddr + bytesForMemo(height) + len(pattmem)
        self.printInfoCallback("beginning will be at " + str(hex(beginaddr)) +  ", end at " + str(hex(endaddr)))

        # Note - It's note certain that in all cases this collision test is needed. What's happening
        # when you write below this address (as the pattern grows downward in memory) in that you begin
        # to overwrite the pattern index data that starts at low memory. Since you overwrite the info
        # for highest memory numbers first, you may be able to get away with it as long as you don't
        # attempt to use higher memories.
        # Steve

        if beginaddr <= 0x2B8:
            self.printErrorCallback("Sorry, this will collide with the pattern entry data since %s is <= 0x2B8!" % hex(beginaddr))
            #exit

        # write the memo and pattern entry from the -end- to the -beginning- (up!)
        for i in range(len(memoentry)):
            bf.setIndexedByte(endaddr, 0)
            endaddr -= 1

        for i in range(len(pattmem)):
            bf.setIndexedByte(endaddr, pattmem[i])
            endaddr -= 1

        # push the data to a file
        outfile = open(newbrotherfile, 'wb')

        d = bf.getFullData()
        outfile.write(d)
        outfile.close()

class InserterException(Exception):
    def getMessage(self):
        msg = ''
        for arg in self.args:
            if msg != '':
                msg += ' '
            msg += str(arg)
            
        return msg

class PatternNotFoundException(InserterException):
    def __init__(self, patternNumber):
        self.patternNumber = patternNumber
        

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print 'Usage: %s oldbrotherfile pattern# image.bmp newbrotherfile' % sys.argv[0]
        sys.exit()
    inserter = PatternInserter()
    argv = sys.argv
    try:
        inserter.insertPattern(argv[1],argv[2],argv[3],argv[4])
    except PatternNotFoundException as e:
        print 'ERROR: Pattern %d not found' % e.patternNumber
        sys.exit(1)
    except InserterException as e:
        print 'ERROR: ',e.getMessage()
        sys.exit(1)
