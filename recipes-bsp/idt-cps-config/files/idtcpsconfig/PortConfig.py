#! /usr/bin/env python3

from collections import namedtuple


class PortConfig(namedtuple("PortConf", ["source", "polarity", "term", "output"])):
    def __str__(self):
        return "PortConfig(source = {source:2d}, pol = {polarity}, term = {term}, output = {output}" \
                .format(**self._asdict())

    @classmethod
    def from_byte(cls, byte):
        if isinstance(byte, bytes):
            assert len(byte) == 1
            byte = int(byte[0])

        source = byte & 0xF
        polarity = (byte >> 5) & 0x1
        term = (byte >> 6) & 0x1
        output = (byte >> 7) & 0x1
        return PortConfig(source, polarity, term, output)

    def to_byte(self):
        tmp = 0
        tmp |= self.source
        tmp |= self.polarity << 5
        tmp |= self.term << 6
        tmp |= self.output << 7
        return bytes([tmp])

