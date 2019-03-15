import json
from fastavro import writer, reader, parse_schema
import fastavro
from fastavro.six import MemoryIO


def test_schemaless_write_read():
    # schema registry 통해 write된 bytes
    value = b'\x00\x00\x00\x00*\xc6\x94\x8e\x8a\t\x0e1540551\x04\x04\x04\x01\x00\x00\x00\x14STXV\xed\x83\x80\xec\x9b\x8c\nJ\x89\x86\x13\xbdB@cRc\xe7\x86\xb8_@\x02\xc6\xbd\x88\x01\x02\x16\x00>\xeb\x94\x94\xec\x95\x84\xeb\x9c\xa8\xea\xb0\xa4\xeb\x9f\xac\xeb\xa6\xac1\xec\x98\xa4\xed\x94\xbc\xec\x8a\xa4\xed\x85\x94f\x90\xbb\x08S\xc0B@\xbf\xc0\xacP\xa4\xb0_@\x02\xf0\x8a\xfb\x02\x02\x94\xe5\x03\x02\xfc\xaa\x03\x8e+\x98\x9b\x05\x88\x0e'

    schema_string = """
    {"type":"record","name":"Call","fields":[{"name":"id","type":"long"},{"name":"user_id","type":"string"},{"name":"retry_count","type":"int"},{"name":"taxi_kind","type":{"type":"enum","name":"TAXI_KIND","symbols":["MEDIUM","LARGE","DELUXE","LUXURY"]},"default":"MEDIUM"},{"name":"dispatch_item","type":{"type":"enum","name":"DISPATCH_ITEM","symbols":["INSTANT","PRIOR","NORMAL"]},"default":"NORMAL"},{"name":"creditcard_enabled","type":"boolean"},{"name":"return_taxi","type":"boolean"},{"name":"inapp_payment","type":"boolean"},{"name":"origin","type":{"type":"record","name":"Location","fields":[{"name":"location_type","type":{"type":"enum","name":"LOCATION_TYPE","doc":"POI,구주소,새주소,행정구역,사용자지정(좌표없음),나머지케이스,null","symbols":["PLACE","JIBUN","ROAD","REGION","USER","UNKNOWN","NULL"]},"default":"NULL"},{"name":"name","type":"string"},{"name":"lat","type":"double"},{"name":"lng","type":"double"},{"name":"region_code","type":["null","int"],"default":null},{"name":"biz_region_code","type":["null","int"],"default":null}]}},{"name":"destination","type":"Location"},{"name":"route","type":["null",{"type":"record","name":"Route","fields":[{"name":"distance","type":"int"},{"name":"time","type":"int"},{"name":"fare","type":"int"},{"name":"toll","type":"int"}]}],"default":null}]}
    """

    schema = json.loads(schema_string)
    parsed_schema = parse_schema(schema)

    new_file = MemoryIO()
    new_file.write(value)
    new_file.seek(5)

    new_record = fastavro.schemaless_reader(new_file, parsed_schema)
    print(new_record)
