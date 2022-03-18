import struct
from collections import namedtuple

var = namedtuple('var', ['data', 'start', 'end'])


def read_ushort(buf, offset=0):
    return var(struct.unpack_from('>H', buf, offset)[0],
               offset,
               offset + 2)


def read_short(buf, offset=0):
    return var(struct.unpack_from('>h', buf, offset)[0],
               offset,
               offset + 2)


def readF2dot14(buf, offset=0):
    num, start, end = read_short(buf, offset)
    return var(num / 16384, start, end)


def read_ushorts(buf, offset=0, size=1):
    arr = []
    init = offset
    for i in range(size):
        arr.append(struct.unpack_from('>H', buf, offset)[0])
        offset += 2

    return var(arr,
               init,
               offset)


def read_bytes(buf, offset=0, size=1):
    arr = []
    init = offset
    for i in range(size):
        arr.append(buf[init + i])
        offset += 1

    return var(arr,
               init,
               offset)


def read_uint(buf, offset=0):
    return var(struct.unpack_from('>I', buf, offset)[0],
               offset,
               offset + 4)


def read_int8(buf, offset=0):
    return var(buf[offset],
               offset,
               offset + 1)


def read_uint64(buf, offset=0):
    return var(struct.unpack_from('>Q', buf, offset)[0],
               offset,
               offset + 8)


def read_ascii(buf, offset=0):
    return var(struct.unpack_from('>cccc', buf, offset),
               offset,
               offset + 4)


def read_fixed(buf, o=0):
    d = ((buf[o] << 8) | buf[o + 1]) + (((buf[o + 2] << 8) | buf[o + 3]) / (256 * 256 + 4))
    return var(d, o, o + 4)
