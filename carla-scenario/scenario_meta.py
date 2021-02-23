import os
import ast
from glob import glob


def search_classes(base_dir):
    results = []
    for filename in glob(f"{base_dir}/*.py"):
        module_name = os.path.splitext(os.path.basename(filename))[0]
        with open(filename, 'r') as r:
            p = ast.parse(r.read())
            classes = [f"{base_dir}.{module_name}.{node.name}" for node in ast.walk(p) if isinstance(node, ast.ClassDef)]
            results.extend(classes)

    return results


def get_class( kls ):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__( module )
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m


if __name__ == '__main__':
    for class_name in search_classes('scenario'):
        print(class_name)
        MyScenario = get_class(class_name)
        s = MyScenario()
        print(s.description)
        print(s.mapName)
        print(s.timeout)
        print(s.make_ego_vehicle(None))
        print('==================')
