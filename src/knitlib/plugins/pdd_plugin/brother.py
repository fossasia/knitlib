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
import array
#import os
#import os.path
#import string
from array import *
import ctypes

__version__ = '1.0'

methodWithPointers = False
methodWithPointers = True # uncomment this to use new, more precise method of finding patterns in the dat file, based on kh940 format documentation from https://github.com/stg/knittington/blob/master/doc/kh940_format.txt (should work with all kh930 and kh940 models)

# Some file location constants
initPatternOffset = 0x06DF # programmed patterns start here, grow down
currentPatternAddr = 0x07EA # stored in MSN and following byte
currentRowAddr = 0x06FF
nextRowAddr = 0x072F
currentRowNumberAddr = 0x0702
carriageStatusAddr = 0x070F
selectAddr = 0x07EA



# various unknowns which are probably something we care about
unknownList = {'0700':0x0700, '0701':0x0701,
               '0704':0x0704, '0705':0x0705, '0706':0x0706, '0707':0x0707,
               '0708':0x0708, '0709':0x0709, '070A':0x070A, '070B':0x070B,
               '070C':0x070C, '070D':0x070D, '070E':0x070E, '0710':0x0710,
               '0711':0x0711, '0712':0x0712, '0713':0x0713, '0714':0x0714,
               '0715':0x0715}

def nibbles(achar):
    #print '0x%02X' % ord(achar)
    msn = (ord(achar) & 0xF0) >> 4
    lsn = ord(achar) & 0x0F
    return msn, lsn

def hto(hundreds, tens, ones):
    return (100 * hundreds) + (10 * tens) + ones

def roundeven(val):
    return (val+(val%2))

def roundeight(val):
    if val % 8:
        return val + (8-(val%8))
    else:
        return val

def roundfour(val):
    if val % 4:
        return val + (4-(val%4))
    else:
        return val

def nibblesPerRow(stitches):
    # there are four stitches per nibble
    # each row is nibble aligned
    return(roundfour(stitches)/4)

def bytesPerPattern(stitches, rows):
    nibbs = rows * nibblesPerRow(stitches)
    bytes = roundeven(nibbs)/2
    return bytes

def bytesForMemo(rows):
    bytes = roundeven(rows)/2
    return bytes

def bytesPerPatternAndMemo(stitches, rows):
    patbytes = bytesPerPattern(stitches, rows)
    memobytes = bytesForMemo(rows)
    return patbytes + memobytes

class brotherFile(object):

    def __init__(self, fn):
        self.dfn = None
        self.verbose = False
        try:
            try:
                self.df = open(fn, 'rb+')     # YOU MUST HAVE BINARY FORMAT!!!
            except IOError:
                # for now, read only
                raise
                #self.df = open(fn, 'w')
        except:
            print 'Unable to open brother file <%s>' % fn
            raise
        try:
            if methodWithPointers:
                self.data = self.df.read(-1)
            else:
                self.data = self.df.read(2048)
            self.df.close()
            if len(self.data) == 0:
                raise Exception()
        except:
            if methodWithPointers:
                print 'Unable to read 2048 bytes from file <%s>' % fn
            else:
                print 'Unable to read data from file <%s>' % fn
            raise
        self.dfn = fn
        return

    def __del__(self):
        return

    def getIndexedByte(self, index):
        return ord(self.data[index])

    def setIndexedByte(self, index, b):
        # python strings are mutable so we
        # will convert the string to a char array, poke
        # and convert back
        dataarray = array('c')
        dataarray.fromstring(self.data)

        if self.verbose:
            print "* writing ", hex(b), "to", hex(index)
        #print dataarray

        # this is the actual edit
        dataarray[index] = chr(b)

        # save the new string. sure its not very memory-efficient
        # but who cares?
        self.data = dataarray.tostring()
        
    # handy for debugging
    def getFullData(self):
        return self.data

    def getIndexedNibble(self, offset, nibble):
        # nibbles is zero based
        bytes = nibble/2
        m, l = nibbles(self.data[offset-bytes])
        if nibble % 2:
            return m
        else:
            return l

    def getRowData(self, pattOffset, stitches, rownumber):
        row=array('B')
        nibspr = nibblesPerRow(stitches)
        startnib = nibspr * rownumber
        endnib = startnib + nibspr

        for i in range(startnib, endnib, 1):
            nib = self.getIndexedNibble(pattOffset, i)
            row.append(nib & 0x01)
            stitches = stitches - 1
            if stitches:
                row.append((nib & 0x02) >> 1)
                stitches = stitches - 1
            if stitches:
                row.append((nib & 0x04) >> 2)
                stitches = stitches - 1
            if stitches:
                row.append((nib & 0x08) >> 3)
                stitches = stitches - 1
        return row

    def getPatterns(self, patternNumber = None):
        """
        Get a list of custom patterns stored in the file, or
        information for a single pattern.
        Pattern information is stored at the beginning
        of the file, with seven bytes per pattern and
        99 possible patterns, numbered 901-999.
        Returns: A list of tuples:
          patternNumber
          stitches
          rows
          patternOffset
          memoOffset
        """
        patlist = []
        idx = 0
        pptr = initPatternOffset
        for pi in range(1, 100):
            flag = ord(self.data[idx])
            if self.verbose:
                print 'Entry %d, flag is 0x%02X' % (pi, flag)
            idx = idx + 1
            unknown = ord(self.data[idx])
            idx = idx + 1
            rh, rt = nibbles(self.data[idx])
            idx = idx + 1
            ro, sh = nibbles(self.data[idx])
            idx = idx + 1
            st, so = nibbles(self.data[idx])
            idx = idx + 1
            unk, ph = nibbles(self.data[idx])
            idx = idx + 1
            pt, po = nibbles(self.data[idx])
            idx = idx + 1
            rows = hto(rh,rt,ro)
            stitches = hto(sh,st,so)
            patno = hto(ph,pt,po)
            # we have this entry
            if self.verbose:
                print '   Pattern %3d: %3d Rows, %3d Stitches - ' % (patno, rows, stitches)
            if flag != 0:
                # valid entry
                if methodWithPointers:
                    pptr =  len(self.data) -1 - ((flag << 8) + unknown) 
                memoff = pptr
                if self.verbose:
                    print "Memo #",patno, "offset ", memoff
                patoff = pptr - bytesForMemo(rows)
                if self.verbose:
                     print "Pattern #",patno, "offset ", patoff
                pptr = pptr - bytesPerPatternAndMemo(stitches, rows)
                if self.verbose:
                     print "Ending offset ", hex(pptr)
                if patternNumber:
                    if patternNumber == patno:
                        patlist.append({'number':patno, 'stitches':stitches, 'rows':rows, 'memo':memoff, 'pattern':patoff, 'pattend':pptr})
                else:
                    patlist.append({'number':patno, 'stitches':stitches, 'rows':rows, 'memo':memoff, 'pattern':patoff, 'pattend':pptr})
            else:
                break
        return patlist

    def getMemo(self):
        """
        Return an array containing the memo
        information for the pattern currently in memory
        """
        patt = self.patternNumber()
        if patt > 900:
            return self.getPatternMemo(patt)
        else:
            rows = 0 # TODO XXXXXXXXX
        return [0]

    def patternNumber(self):
        sn, pnh = nibbles(self.data[currentPatternAddr])
        pnt, pno = nibbles(self.data[currentPatternAddr+1])
        pattern = hto(pnh,pnt,pno)
        return(pattern)

    def getPatternMemo(self, patternNumber):
        """
        Return an array containing the memo
        information for a custom pattern. The array
        is the same length as the number of rows
        in the pattern.
        """
        list = self.getPatterns(patternNumber)
        if len(list) == 0:
            return None
        memos = array('B')
        memoOff = list[0]['memo']
        rows = list[0]['rows']
        memlen = roundeven(rows)/2
        # memo is padded to en even byte
        for i in range(memoOff, memoOff-memlen, -1):
            msn, lsn = nibbles(self.data[i])
            memos.append(lsn)
            rows = rows - 1
            if (rows):
                memos.append(msn)
                rows = rows - 1
        return memos

    def getPattern(self, patternNumber):
        """
        Return an array containing the pattern
        information for a pattern.
        """
        list = self.getPatterns(patternNumber)
        if len(list) == 0:
            return None
        pattern = []

        patoff = list[0]['pattern']
        rows = list[0]['rows']
        stitches = list[0]['stitches']

        #print 'patoff = 0x%04X' % patoff
        #print 'rows = ', rows
        #print 'stitches = ', stitches
        for i in range(0, rows):
            arow = self.getRowData(patoff, stitches, i)
            #print arow
            pattern.append(arow)
        return pattern

    def displayPattern(self, patternNumber):
        """
        Display a user pattern stored in file saved 
        from the brother knitting machine. Patterns
        in memory are stored with the beginning of the
        pattern at the highest memory address.
        """

        return

    def rowNumber(self):
        sn, rnh = nibbles(self.data[currentRowNumberAddr])
        rnt, rno = nibbles(self.data[currentRowNumberAddr+1])
        rowno = hto(rnh,rnt,rno)
        return(rowno)

    def nextRow(self):
        return self.getRowData(nextRowAddr, 200, 0)
        
    def selectorValue(self):
        return ord(self.data[selectAddr])

    def carriageStatus(self):
        return ord(self.data[carriageStatusAddr])

    def motifData(self):
        motiflist = []
        addr = 0x07FB
        for i in range(6):
            mph, mpt = nibbles(self.data[addr])
            if mph & 8:
                mph = mph - 8
                side = 'right'
            else:
                side = 'left'
            mpo, foo = nibbles(self.data[addr+1])
            mch, mct = nibbles(self.data[addr+2])
            mco, bar = nibbles(self.data[addr+3])
            pos = hto(mph,mpt,mpo)
            cnt = hto(mch,mct,mco)
            motiflist.append({'position':pos, 'copies':cnt, 'side':side})
            addr = addr - 3
        return motiflist

    def patternPosition(self):
        addr = 0x07FE
        foo, ph = nibbles(self.data[addr])
        if ph & 8:
            ph = ph - 8
            side = 'right'
        else:
            side = 'left'
        pt, po = nibbles(self.data[addr+1])
        pos = hto(ph,pt,po)

        return {'position':pos, 'side':side}

    # these are hardcoded for now
    def unknownOne(self):
        info = array('B')
        for i in range(0x06E0, 0x06E5):
            info.append(ord(self.data[i]))
        return info

    def unknownMemoRange(self):
        info = array('B')
        for i in range(0x0731, 0x0787):
            info.append(ord(self.data[i]))
        return info

    def unknownEndRange(self):
        info = array('B')
        for i in range(0x07D0, 0x07E9):
            info.append(ord(self.data[i]))
        return info

    def unknownAddrs(self):
        return unknownList.items()
            
