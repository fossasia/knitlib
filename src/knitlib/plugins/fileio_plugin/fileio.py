# -*- coding: utf-8 -*-


from struct import pack
from os.path import basename

""" directory entries """
dosfn = lambda f: "%-8.8s%-3.3s" % tuple((f.upper() + '.').split('.'))[:2]
dirent = lambda f, o, l: pack('<11s15xHI', dosfn(basename(f)), o, l)
blocks = lambda n, b: n / b + (n % b > 0)
accum = lambda vs, v0: reduce(lambda l, r: l + [r + l[-1]], vs, [v0])

""" expand FAT entry to components """
nybbles = lambda vs: sum(((v & 0xf, (v >> 4) & 0xf, (v >> 8) & 0xf) for v in vs), ())

""" convert each pair to byte value """
n2bytes = lambda ns: [pack('B', o * 0x10 + e) for e, o in zip(ns[0::2], ns[1::2])]


def mkimg(filename, blobs):
    """ writes image to the disk """
    f = open(filename, "w")
    for off, data in blobs:
        f.seek(512 * off)
        f.write(''.join(data))
    f.close()


def mkfat12(opts, files):
    if '-h' in opts:
        print "Usage: [-b MBR] [-o output] [-s sector count] files..."
        return

    param = opts.get
    """ file data retrieval contents"""
    con = [file(f).read() for f in files]
    lens = [len(c) for c in con]
    """ offset calculating """
    ofs = accum((blocks(l, 512) for l in lens), 2)
    """ FAT encoding """
    fat = n2bytes(nybbles((b in ofs) and 0xfff or b for b in range(1, ofs[-1] + 1)))
    fn = param('-o', "a.raw")
    op = open(param('-b', "mbr.raw")).read()
    """ parameter """
    para = param('-s', "2880")
    """ integer value of parameter"""
    ip = int(para) - 1
    pax = pack('512x')
    mkimg(fn, [(0, [op]), (1, fat), (10, fat), (19, [dirent(*e) for e in zip(files, ofs, lens)])] + [(31 + o, [c]) for o, c in zip(ofs, con)] + [(ip, [pax])])
