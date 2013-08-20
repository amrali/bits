"""
Parse aria2 control file
http://sourceforge.net/apps/trac/aria2/wiki/ControlFileFormat
"""

import os
import sys
import struct
import StringIO

from pprint import pprint

class ControlFile(object):
    """Represents the structure of the control file."""

    def __init__(self, path):
        self._path = os.path.expanduser(path)
        self._data = None
        self.fields = {}

    def refresh(self):
        """Refresh the fields."""
        with open(self._path, 'rb') as fd:
            self._data = fd.read()
        self._parse()

    def _parse(self):
        if not self._data:
            raise RuntimeError("Must read the data first")
        buf = StringIO.StringIO(self._data)
        self.fields['VERSION'] = struct.unpack(">H", buf.read(2))[0]
        ext = struct.unpack(">I", buf.read(4))[0]
        self.fields['EXTENSION'] = "InfoHashCheck" if ext & 1 else None
        ihl = self.fields['INFO_HASH_LENGTH'] = struct.unpack(">I", buf.read(4))[0]
        self.fields['INFO_HASH'] = struct.unpack(">{}B".format(ihl),
                buf.read(ihl))
        self.fields['PIECE_LENGTH'] = struct.unpack(">I", buf.read(4))[0]
        self.fields['TOTAL_LENGTH'] = struct.unpack(">Q", buf.read(8))[0]
        self.fields['UPLOAD_LENGTH'] = struct.unpack(">Q", buf.read(8))[0]
        bfl = self.fields['BITFIELD_LENGTH'] = struct.unpack(">I", buf.read(4))[0]
        self.fields['BITFIELD'] = struct.unpack(">{}B".format(bfl),
                buf.read(bfl))
        nifp = self.fields['NUM_IN_FLIGHT_PIECE'] = struct.unpack(">I",
                buf.read(4))[0]
        in_flight_pieces = []
        for i in xrange(nifp):
            piece = {}
            piece['INDEX'] = struct.unpack(">I", buf.read(4))[0]
            piece['LENGTH'] = struct.unpack(">I", buf.read(4))[0]
            bl = piece['BITFIELD_LENGTH'] = struct.unpack(">I", buf.read(4))[0]
            piece['BITFIELD'] = struct.unpack(">{}B".format(bl), buf.read(bl))
            in_flight_pieces.append(piece)
        self.fields['IN_FLIGHT_PIECES'] = in_flight_pieces

if __name__ == '__main__':
    path = sys.argv[1]
    cf = ControlFile(path)
    cf.refresh()
    pprint(cf.fields)

