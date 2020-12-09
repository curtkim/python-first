## howto

    wget -O target_1280.mp4 https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_1280_10MG.mp4

## dict
- decoding time stamp (DTS) 
- presentation time stamp (PTS)
- "B" frmae  stands for "bidirectional"
- "I" frames "intra" 
- "P" frame "predicted"

## reference
http://dranger.com/ffmpeg/tutorial01.html

## note
- frame = container.decode(stream)
- packet = container._demux(stream)
- packets = codec.parse(chunk)
- frames = codec.decode(packet)

