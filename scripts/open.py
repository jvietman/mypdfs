from importlib import import_module
def imports(libs: list):
    for l in libs:
        m = import_module("scripts."+l)

        for name in dir(m):
            if not name.startswith('_'):
                globals()[name] = getattr(m, name)

def main(id):
    if not id.isdigit():
        return 1, "\"id\" value has to be an integer."

    open_viewer(get_files()[int(id)])
    exit()