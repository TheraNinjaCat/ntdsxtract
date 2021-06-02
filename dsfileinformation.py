#!/usr/bin/env python
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

from __future__ import print_function
import argparse
import datetime
import binascii
import struct

import sys
import ntds.version
from ntds.dstime import dsGetDBLogTimeStampStr
from ntds.lib.dump import dump

class NTDSHeader:
    def __init__(self, header):
        self.header = header
        self.checksum = binascii.hexlify(header[0:4][::-1]).decode("utf-8")
        self.signature = binascii.hexlify(header[4:8][::-1]).decode("utf-8")
        self.file_format_version = binascii.hexlify(header[8:12][::-1]).decode("utf-8")
        self.file_type = binascii.hexlify(header[12:16][::-1]).decode("utf-8")
        self.db_time = binascii.hexlify(header[16:24][::-1]).decode("utf-8")

        self.creation_time = dsGetDBLogTimeStampStr(header[28:36])
        self.consistent_time = dsGetDBLogTimeStampStr(header[64:72])
        self.attach_time = dsGetDBLogTimeStampStr(header[72:80])
        self.detach_time = dsGetDBLogTimeStampStr(header[88:96])
        self.recovery_time = dsGetDBLogTimeStampStr(header[244:252])

        self.w_major_version = struct.unpack("I", header[216:220])[0]
        self.w_minor_version = struct.unpack("I", header[220:224])[0]
        self.w_build_number = struct.unpack("I", header[224:228])[0]
        self.w_service_pack = struct.unpack("I", header[228:232])[0]

        self.page_size = struct.unpack('I', header[236:240])[0]

    def __str__(self):
        return "\n".join((
            "Header checksum:     {}".format(self.checksum),
            "Signature:           {}".format(self.signature),
            "File format version: {}".format(self.file_format_version),
            "File type:           {}".format(self.file_type),
            "Page size:           {} bytes".format(self.page_size),
            "DB time:             {}".format(self.db_time),
            "Windows version:     {}.{} ({}) Service pack {}".format(
                self.w_major_version,
                self.w_minor_version,
                self.w_build_number,
                self.w_service_pack
            ),
            "Creation time:       {}".format(self.creation_time),
            "Attach time:         {}".format(self.attach_time),
            "Detach time:         {}".format(self.detach_time if self.detach_time else "database is in a dirty state"),
            "Consistent time      {}".format(self.consistent_time),
            "Recovery time:       {}".format(self.recovery_time),
            "Header dump (first 672 bytes): ",
            dump(self.header[:672], 16, 4)
        ))


def main():
    """Main function for reading information from the ntds.dit file"""
    args = parse_args()
    
    print("\n[+] Started at {}\n".format(datetime.datetime.now()), file=sys.stderr)

    with open(args.ntds, "rb") as ntds_file:
        ntds_header = NTDSHeader(ntds_file.read(8192))
    
    print(ntds_header, "\n")


class CustomParser(argparse.ArgumentParser):
    def error(self, message):
        print("Error: {}\n".format(message), file=sys.stderr)
        self.print_help()
        sys.exit(2)


def parse_args():
    """Argument parsing"""
    parser = CustomParser(
        description="DSFileInformation v{}\nExtracts information related to the NTDS.DIT database file".format(ntds.version.version),
        usage="%(prog)s <ntds.dit>",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("ntds", help="NTDS.DIT database file.")
    parser.add_argument("--debug", action="store_true", help="Turn on detailed error messages and stack trace")
    parser.add_argument("--version", action="version", version="DSFileInformation v{}".format(ntds.version.version))

    return parser.parse_args()


if __name__ == "__main__":
    main()