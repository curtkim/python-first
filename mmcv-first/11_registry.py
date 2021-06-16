import converters.converter1
from converters.builder import CONVERTERS


converter_cfg = dict(type='Converter1', a='a', b='b')
converter = CONVERTERS.build(converter_cfg)

assert isinstance(converter, converters.converter1.Converter1)
assert converter.a == 'a'
