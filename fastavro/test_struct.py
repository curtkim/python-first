import struct

MAGIC_BYTE = 0


def test_pack_unpack():
    """
        > : big-endian
        h : short(2 bytes)
        l : long(4 bytes)
        from https://docs.python.org/2/library/struct.html
    """
    assert isinstance(struct.pack('>hhl', 1, 2, 3), bytes)
    assert b'\x00\x01\x00\x02\x00\x00\x00\x03' == struct.pack('>hhl', 1, 2, 3)
    assert (1, 2, 3) == struct.unpack('>hhl', b'\x00\x01\x00\x02\x00\x00\x00\x03')

    assert b'\x00' == struct.pack('b', MAGIC_BYTE)
    assert b'\x00\x00\x00*' == struct.pack('>I', 42)
