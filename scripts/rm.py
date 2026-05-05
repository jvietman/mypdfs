import os

from importlib import import_module
def imports(libs: list):
    for l in libs:
        m = import_module("scripts."+l)

        for name in dir(m):
            if not name.startswith('_'):
                globals()[name] = getattr(m, name)

def main(id1, id2=""):
    if not id1.isdigit():
        return 1, "\""+("from" if id2 else "id")+"\" value has to be an integer."
        
    x = int(id1)
    y = x+1
    if id2:
        if id2.isdigit():
            y = int(id2)+1
        else:
            return 1, "\"to\" value has to be an integer."

    if get_files()[x:y]:
        for i in get_files()[x:y]:
            print("removing "+os.path.basename(i))
            os.remove(i)
        return 0, str(y-x)+" pdfs removed!"
    else:
        return 0, "pdf"+("s" if id2 else "")+" of ind"+("ices "+id1+" to "+id2 if id2 else "ex "+id1)+" do"+("" if id2 else "es")+"nt exist"