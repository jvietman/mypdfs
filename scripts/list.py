import os

from importlib import import_module
def imports(libs: list):
    for l in libs:
        m = import_module("scripts."+l)

        for name in dir(m):
            if not name.startswith('_'):
                globals()[name] = getattr(m, name)

def main():
    print(list_to_str(get_files()))