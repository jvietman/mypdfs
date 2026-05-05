import os, sys, json, subprocess

with open(os.path.dirname(os.path.realpath(__file__))+"/config.json", "r") as f:
    viewer = json.load(f)["viewer"]
    f.close()

def open_viewer(file):
    subprocess.run([viewer, file]) 

# get all pdf files in current dir
def get_files() -> list[str]:
    files = []
    for f in os.listdir():
        if f.endswith(".pdf"):
            files.append(os.getcwd()+"/"+f)
    
    return list(reversed(files))

# turns lists into string with each element having an id
def list_to_str(l: list) -> str:
    if not l:
        return "No elements found"
    
    out = ""
    for i in range(len(l)):
        if i > 0:
            out += "\n"
        out += "("+str(i)+"): "+os.path.basename(l[i])
    return out