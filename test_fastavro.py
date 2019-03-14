from fastavro import writer, reader, parse_schema
import fastavro
from fastavro.six import MemoryIO


schema = {
    'doc': 'A weather reading.',
    'name': 'Weather',
    'namespace': 'weather',
    'type': 'record',
    'fields': [
        {'name': 'station', 'type': 'string'},
        {'name': 'time', 'type': 'long'},
        {'name': 'temp', 'type': 'int'},
        {'name': 'kind', 'type': {"type": "enum", "name": "kind", "symbols": ["FOO", "BAR"]}, "default": "FOO"},
    ],
}
parsed_schema = parse_schema(schema)

# 'records' can be an iterable (including generator)
records = [
    {u'station': u'011990-99999', u'temp': 0, u'time': 1433269388, u'kind': 'FOO'},
    {u'station': u'011990-99999', u'temp': 22, u'time': 1433270389, u'kind': 'BAR'},
    {u'station': u'011990-99999', u'temp': -11, u'time': 1433273379, u'kind': 'FOO'},
    {u'station': u'012650-99999', u'temp': 111, u'time': 1433275478, u'kind': 'BAR'},
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

    # bytes로 변환?
    new_file.seek(0)

    new_record = fastavro.schemaless_reader(new_file, parsed_schema)
    assert records[0] == new_record