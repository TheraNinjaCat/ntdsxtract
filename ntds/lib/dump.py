# This file is part of ntdsxtract.
#
# ntdsxtract is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ntdsxtract is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ntdsxtract.  If not, see <http://www.gnu.org/licenses/>.

'''
@author:        Csaba Barta
@license:       GNU General Public License 2.0 or later
@contact:       csaba.barta@gmail.com
'''

# Original hex dump code from
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/142812

PY2_FILTER = "".join([chr(byte) if len(repr(chr(byte))) == 3 else "." for byte in range(256)])
PY3_FILTER = b"".join([bytes([byte]) if len(repr(chr(byte))) == 3 else b"." for byte in range(256)])

def to_printable(bin):
    """Change a bytes object into a printable string"""
    try:
        printable = bin.translate(PY3_FILTER).decode("latin-1")
    except ValueError:
        printable = bin.translate(PY2_FILTER)
    except:
        import traceback, sys
        traceback.print_exc()
        sys.exit(1)
    return printable


def dump(src, length=8, indent=0):
    lines = []
    count = 0
    indent = " " * indent
    while src:
        line, src = src[:length], src[length:]
        try:
            hex_line = ' '.join(["{:02x}".format(byte) for byte in line])
        except ValueError:
            hex_line = ' '.join(["{:02x}".format(ord(byte)) for byte in line])
        line = to_printable(line)
        lines.append(
            "{}{:04x}    {}    {}".format(indent, count, hex_line, line)
        )
        count += length
    return "\n".join(lines)