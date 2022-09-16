#! /usr/bin/env python3

import logging
import itertools
import time

from slcc.extra_logging import LEVEL_TRACE

class ADN4612TxtParser:
    EXP_HEADER = "# ADN4612 Registers Script"
    EXP_PART_VAL = ["ADN4612ACPZ"]

    def __init__(self, filename):
        self.logger = logging.getLogger(__name__)
        self.filename = filename

    def parse(self, callback=None):
        self.logger.debug("parse called")

        with open(self.filename, "r") as f:
            self.logger.debug("opened %s", self.filename)

            # Check header
            hdr = next(f).strip()
            assert hdr == self.EXP_HEADER, "Txt file header does not match expected"

            # Check part number
            f = itertools.dropwhile(lambda l: l.find("# Part") == 0, f)
            next(f)
            part = next(f).strip().split(": ")[1]
            assert part in self.EXP_PART_VAL, \
                "Part number does not match, expect %s, got %s" % (self.EXP_PART_VAL, part)

            seen_header = False
            seen_postamble = False

            # we are not Python built-in CSV reader, because of delay line in comments
            for line in f:
                line = line.strip()

                if len(line) == 0:
                    continue

                if line.find("Address,Data") == 0:
                    self.logger.debug("Seen \"Address,Data\" header")
                    seen_header = True

                elif seen_header and line[0] != "#":
                    arr0 = line.split(",")
                    reg_addr = int(arr0[0], 16)
                    arr1 = arr0[1].split('#')
                    val = int(arr1[0], 16)

                    self.logger.log(LEVEL_TRACE,
                                    "reg: page = addr = 0x%02x, val = 0x%02x",
                                    reg_addr, val)

                    if callable(callback):
                        callback(reg_addr, val)

            assert seen_header, \
                "Unable to find header (\"Address,Data\") in the file"

            self.logger.info("parsing done")

def main():
    """ Example usage, parses .txt file """
    logging.basicConfig(level=LEVEL_TRACE)
    filename = "example.txt"

    parser = ADN4612TxtParser(filename)
    parser.parse(lambda addr, val: print(addr, val))

if __name__ == "__main__":
    main()
