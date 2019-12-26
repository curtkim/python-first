from fastavro import writer, reader, parse_schema
import fastavro
from fastavro.six import MemoryIO


schema = {
    'name': 'Call',
    'type': 'record',
    'fields': [
        {"name": "id", "type": "long"},
        {"name": "origin", "type":
            {"type": "record", "name": "Location",
             "fields": [
                 {"name": "name", "type": "string"},
                 {"name": "lat", "type": "double"},
                 {"name": "lng", "type": "double"},
                 {"name": "region_code", "type": ["null", "int"]},
             ]
             }
         },
        {"name": "destination", "type": "Location"},
    ],
}

parsed_schema = parse_schema(schema)

records = [
    {
        'id': 1,
        'origin': {'name': '강남역', 'lat': 37, 'lng': 127, 'region_code': 1234567},
        'destination': {'name': '서울역', 'lat': 37.1, 'lng': 127.1, 'region_code': 1234568}
    }
]


def test_write_read():
    new_file = MemoryIO()
    writer(new_file, parsed_schema, records)
    new_file.seek(0)
    new_records = list(reader(new_file, parsed_schema))

    assert new_records == records


def test_schemaless_write_read():
    new_file = MemoryIO()
    fastavro.schemaless_writer(new_file, parsed_schema, records[0])

    new_file.seek(0)
    new_record = fastavro.schemaless_reader(new_file, parsed_schema)
    assert records[0] == new_record

