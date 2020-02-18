#! /usr/bin/env python3

import logging
import itertools
import time

from slcc.extra_logging import LEVEL_TRACE

class SiLabsTxtParser:
    EXP_HEADER = "# Si534x/7x/8x/9x Registers Script"
    EXP_PART_VAL = "Si5341"

    def __init__(self, filename):
        self.logger = logging.getLogger(__name__)
        self.filename = filename

    def parse(self, callback=None):
        """ Parses the Si Labs txt file and calls callback for each register write

        Args:
            callback: format ((reg addr, page), value)
        """

        with open(self.filename, "r") as f:
            self.logger.debug("opened %s", self.filename)

            # Check header
            hdr = next(f).strip()
            assert hdr == self.EXP_HEADER, "Txt file header does not match expected"

            # Check part number
            f = itertools.dropwhile(lambda l: l.find("# Part") == 0, f)
            next(f)
            part = next(f).strip().split(": ")[1]
            assert part == self.EXP_PART_VAL, \
                "Part number does not match, expect %s, got %s" % (self.EXP_PART_VAL, part)

            seen_header = False

            # we are not Python built-in CSV reader, because of delay line in comments
            for line in f:
                line = line.strip()

                if len(line) == 0:
                    continue

                if line.find("Address,Data") == 0:
                    self.logger.debug("Seen \"Address,Data\" header")
                    seen_header = True

                elif line.find("# Delay") == 0:
                    self.logger.debug("Seen delay line: %s", line)
                    arr = line.split(" ")
                    line_val = int(arr[2])
                    line_units = arr[3]

                    assert line_units == "msec", \
                        "This script was written with the assumption that delay is in msec"

                    time.sleep(line_val/1000)

                elif seen_header and line[0] != "#":
                    arr = line.split(",")
                    full_addr = int(arr[0], 16)
                    val = int(arr[1], 16)

                    page = (full_addr >> 8) & 0xFF
                    reg_addr = full_addr & 0xFF

                    self.logger.log(LEVEL_TRACE,
                                    "reg: page = 0x%02x, addr = 0x%02x, val = 0x%02x",
                                    page, reg_addr, val)

                    if callable(callback):
                        callback((reg_addr, page), val)

            assert seen_header, \
                "Unable to find header (\"Address,Data\") in the file"

            self.logger.info("parsing done")

def main():
    """ Example usage, parses .txt file """
    logging.basicConfig(level=LEVEL_TRACE)
    filename = "example.txt"

    parser = SiLabsTxtParser(filename)
    parser.parse(lambda addr, val: print(addr, val))

if __name__ == "__main__":
    main()
