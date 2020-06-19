# https://eli.thegreenplace.net/2009/08/29/co-routines-as-an-alternative-to-state-machines/

def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        next(cr)
        return cr
    return start


@coroutine
def unwrap_protocol(header='\x61',
                    footer='\x62',
                    dle='\xAB',
                    after_dle_func=lambda x: x,
                    target=None):
    """ Simplified framing (protocol unwrapping)
        co-routine.
    """
    # Outer loop looking for a frame header
    #
    while True:
        byte = (yield)
        frame = ''

        if byte == header:
            # Capture the full frame
            #
            while True:
                byte = (yield)
                if byte == footer:
                    target.send(frame)
                    break
                elif byte == dle:
                    byte = (yield)
                    frame += after_dle_func(byte)
                else:
                    frame += byte


@coroutine
def frame_receiver():
    """ A simple co-routine "sink" for receiving
        full frames.
    """
    while True:
        frame = (yield)
        for c in frame:
            print(hex(ord(c)))
        print(frame)
        print("-------------")

bytes = ''.join(chr(b) for b in
            [0x70, 0x24,
             0x61, 0x99, 0xAF, 0xD1, 0x62,
             0x56, 0x62,
             0x61, 0xAB, 0xAB, 0x14, 0x62,
             0x7
            ])

unwrapper = unwrap_protocol(target=frame_receiver())

for byte in bytes:
    unwrapper.send(byte)