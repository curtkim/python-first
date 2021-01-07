# from scapy3k.all import *
import sys

print(' - Encoding : ', sys.getdefaultencoding())
# print (' - Version  : ', sys.version)

import math
import pprint
import datetime
import pandas as pd
from scapy.all import *  # https://scapy.readthedocs.io/en/latest/installation.html

## http://velodynelidar.com/docs/notes/63-9277%20Rev%20D%20HDL-32E%20Application%20Note%20-%20Packet%20Structure%20%20Timing%20Definition.pdf
HDL_32_vertical_angle = [-30.67, -9.33, -29.33, -8.0, -28.0, -6.67, -26.67, -5.33, -25.33, -4.0, -24.0, -2.67, -22.67,
                         -1.33, -21.33, 0.0, -20.0, 1.33, -18.67, 2.67, -17.33, 4.0, -16.0, 5.33, -14.67, 6.67, -13.33,
                         8.0, -12.0, 9.33, -10.67, 10.67]


# 1 Block = 1 Firing Sequence
def reader_pcap_payload_block(timestamp, payload_block_id, payload_block, prev_azimuth, verbose, verbose_data, debug):
    if hex(payload_block[0]) == '0x0' and hex(payload_block[1]) == '0x0':
        print(' -- Weird Payload with azimuth as zero')
        return [], 0
    else:
        a = hex(payload_block[0]).split('0x')[1]
        if len(a) == 1: a = '0' + a
        b = hex(payload_block[1]).split('0x')[1]
        if len(b) == 1: b = '0' + b
        azimuth = int(b + a, 16) / 100.0  # in degrees
        azimuth_radians = round(math.radians(azimuth), 3)
        if verbose:
            print(' - Id : ', payload_block_id, ' || Azimuth : ', azimuth, 'degrees', ' || Azimuth : ', azimuth_radians,
                  'radians')

        if azimuth <= prev_azimuth:
            print('  ----> Error in azimuth : Prev : ', prev_azimuth, ' Current : ', azimuth)
            print('  ----> Payload Block : ', payload_block, hex(payload_block[1]), hex(payload_block[0]))

        # if debug:
        #     print (payload_block)
        channel_count = int(len(payload_block[2:]) / 3)
        idx_data = 2

        vertical_angles = []
        max_channels = -1
        if channel_count >= 32 and channel_count <= 64:
            max_channels = 32
            vertical_angles = list(HDL_32_vertical_angle)

        if max_channels == len(vertical_angles):
            res_blocks = []
            for k in range(max_channels):
                a = hex(payload_block[idx_data]).split('0x')[1]
                idx_data += 1
                b = hex(payload_block[idx_data]).split('0x')[1]
                idx_data += 1
                dist = (int(b + a, 16) * 2.0) / 1000.0  # in metres

                reflectivity = int(hex(payload_block[idx_data]).split('0x')[1], 16)
                idx_data += 1

                # Convert to XYZ
                ## Points with distances less than one meter should be ignored.
                vertical_angle_radian = math.radians(vertical_angles[k])
                x = round(dist * math.cos(vertical_angle_radian) * math.sin(azimuth_radians), 3)
                y = round(dist * math.cos(vertical_angle_radian) * math.cos(azimuth_radians), 3)
                z = round(dist * math.sin(vertical_angle_radian), 3)

                if verbose_data:
                    print(' - k : ', k, ' || Dist : ', dist, ' || Reflectivity : ', reflectivity)
                    print('          -- X : ', x, 'Y:', y, 'Z:', z)

                if int(abs(dist)) != 0:
                    res_blocks.append([x, y, z, reflectivity, azimuth, timestamp])

            return res_blocks, azimuth

        else:
            print('   --->  Vertical Angles len : ', len(vertical_angles), ' || Channel Count:', channel_count)
            print('   ---> Block : ', payload_block)
            return [], azimuth


def reader_pcap_file(url_pcap, verbose, verbose_data, debug):
    url_pcap_filename = url_pcap.split('.pcap')[0]
    pcap_reader = PcapReader(url_pcap)
    res = []  # "X","Y","Z","intensity","laser_id","azimuth","distance_m","adjustedtime","timestamp","vertical_angle"

    initial_datetime = datetime(2013, 7, 12, 23, 16, 29)
    save_file_count = 0
    flag_stop = 0
    prev_azimuth = 0.0
    pkts_read = 0
    for id_pkt, pkt in enumerate(pcap_reader):
        # if id_pkt < 130 or id_pkt > 153:
        #     continue

        pkt_datetime = datetime.fromtimestamp(pkt.time)
        delta = pkt_datetime - initial_datetime
        if verbose:
            print(' ----------------- Pkt : {0} - {1} ({2}) || Delta ({3}sec, {4}micro-sec) -------------------'.format(
                id_pkt, pkt_datetime, pkt.time, delta.seconds, delta.microseconds))
        payload = pkt.load  # each data packet contains (12 data blocks - HDL32)
        payload_blocks = payload.split(b'\xff\xee')
        idx_block = range(len(payload_blocks))

        if verbose and id_pkt == 0:
            print(' - Type of Packet : ', type(pkt))
            print(' - Pkt Fields : ', pkt.fields, ' || Desc : ', pkt.fields_desc)
            print(' - Pkt Time : ', pkt_datetime, '(', pkt.time, ')', ' || Pkt Len : ', pkt.wirelen)
            print(' - Load Type : ', type(payload), ' || Load Len : ',
                  len(payload))  # 1206 bytes in Velodyne data formatw

            print(' - No. of Blocks : ', len(payload_blocks[1:]), ' || Len of each block : ', len(payload_blocks[1]),
                  '\n')
            print(' - Sample Payload Block : ', payload_blocks[1], '|| ', ' Type : ', type(payload_blocks[1]), '\n')

        for id_payload_block, payload_block in enumerate(payload_blocks):
            if len(payload_block) >= 98:
                if id_payload_block in idx_block:
                    tmp_res, prev_azimuth_ = reader_pcap_payload_block(int(pkt.time), id_payload_block, payload_block,
                                                                       prev_azimuth, verbose, verbose_data, debug)
                    prev_azimuth = float(prev_azimuth_)
                    res.extend(tmp_res)
                    if prev_azimuth > 359.7 and pkts_read > 10:
                        flag_stop = 1

        pkts_read += 1

        # if id_pkt > 10:
        if flag_stop:
            # Step1 - Write file
            df = pd.DataFrame.from_records(res, columns=['x', 'y', 'z', 'intensity', 'azimuth', 'timestamp'])
            tmp_filename = url_pcap_filename + '_' + str(save_file_count) + '.csv'
            df.to_csv(tmp_filename, index=False)

            # Step2 - Reset Vars
            flag_stop = 0
            prev_azimuth = 0.0
            pkts_read = 0
            res = []
            save_file_count += 1

            print(' ======================= Saving - {0} ================= \n'.format(tmp_filename))
            if save_file_count > 10:
                break


if __name__ == "__main__":
    # https://midas3.kitware.com/midas/folder/12978
    url_pcap = '4_intersecton_w_police_car.pcap'
    verbose = 1
    verbose_data = 0
    debug = 0
    reader_pcap_file(url_pcap, verbose, verbose_data, debug)
    # print (count) #90532
