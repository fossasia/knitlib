#!/usr/bin/env python

import sys


if len(sys.argv) != 2:
    print 'Usage: %s file.dat' % sys.argv[0]
    print 'Splits a 2K file.dat file into two 1K track files track0.dat and track1.dat'
    sys.exit()



infile = open(sys.argv[1], 'rb')

track0file = open("track0.dat", 'wb')
track1file = open("track1.dat", 'wb')

t0dat = infile.read(1024)
t1dat = infile.read(1024)


track0file.write(t0dat)
track0file.close()

track1file.write(t1dat)
track1file.close()
