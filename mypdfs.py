import sys, json, os
from importlib import import_module

# definitions
indent = "  "
similarity = 2 # how much to match to be considered similar: max(similar) >= similarity
folder = os.path.dirname(os.path.realpath(__file__))
file = os.path.basename(__file__)
name = os.path.splitext(file)[0]



def load_module(module):
    m = import_module("scripts."+module)
    return m

def help(p):
    global file

    with open(folder+"/info.json", "r") as f:
        info = json.load(f)
        f.close()
    
    m = 1+max([len(to_str(i, " ")) for i in p["syntax"]]) # longest syntax definition, so we can create the spaces
    s = to_str([" " for i in range(m+len(indent))]) # string containing spaces, syntaxes are inserted here, then description is appended
    l = [] # list of already printed options, used to create pretty indents when arguments have similar structure

    print("Usage: "+file+" [options]\n"+info["description"]+"\n\nOptions:")
    print(indent+"--help"+s[6:]+"display this help screen\n")
    for i in range(len(p["syntax"])):
        if len(p["syntax"][i]) == 0:
            u = "*no args*"
        else:
            u = to_str(p["syntax"][i], " ")
            for j in l:
                intersect = str_intersect(p["syntax"][i], j)
                if intersect > 0:
                    u = s[:intersect-1]+"^"+u[intersect:]
                    break
        print(indent+u+s[len(u):]+p["desciption"][i])
        l.append(p["syntax"][i])

def str_intersect(arr1, arr2): # count amount of character are the same (from left to right)
    count = 0
    a = arr1 if len(arr1) < len(arr2) else arr2
    b = arr1 if a == arr2 else arr2
    for i in range(len(a)):
        if a[i] == b[i]:
            count += len(a[i])
        else:
            break
    return count

def to_str(a, space=""):
    s = ""
    for i in a:
        s+=i+space
    return s[:-1]

def match(args, syntax, name, debug=False):
    p = syntax
    
    # render help screen
    if len(args) > 0:
        if args[0] == "--help":
            help(p)
            return

    ss = p["syntax"] # plural, array of syntaxes
    matched = False
    # matched is true, if any args matched while going through syntaxes (if they were similar to a pattern, but didnt exactly match)
    # this is to prevent from accidentally going into an option with a placeholder
    matching = False # if currently matching, or else "matched" doesnt work
    similar = []
    missing = []
    for i in range(len(ss)):
        similar.append(0)
        s = ss[i] # singular syntax
        pass_args = [] # arguments passed to method
        missmatch = False
        matching = False

        if debug: print(str(args)+" = "+str(s))
        for j in range(len(s)): # check all args
            if j >= len(args):
                missing.append(s[j:])
                missmatch = True
                break
            if args[j] == s[j]:
                if debug: print("MATCHED")
                matched = True
                matching = True
            else:
                if (not matched or matching) and s[j][0] == "<" and s[j][-1]==">": # if its a placeholder
                    if debug: print(("matching, " if matching else "")+"placeholder")
                    pass_args.append(args[j])
                else:
                    similar[-1] = str_intersect(args[j], s[j])
                    if debug: print("MISSMATCH")
                    missmatch = True
                    break
        
        if len(s) == 0 and matched:
            if debug: print("ALREADY MATCHED")
            missmatch = True

        if not missmatch:
            try:
                if debug: print("executing \""+p["method"][i]+"\" with passed args: "+str(pass_args))

                m = load_module(p["method"][i])
                m.imports(p["dependencies"])
                status, res = 0, m.main(*pass_args) # response/ return of method
                if type(res) == tuple:
                    status, res = res[0], res[1]

                if res:
                    # if failed & sligtly similar to any argument, show option error
                    if status > 0 < max(similar) < similarity:
                        print(name+": "+args[0]+" is not an option.\nTry 'python "+name+".py --help' for more information.")
                        return
                    print(name+": "+str(res))
                if status > 0: # on error show similar options that couldve worked
                    if max(similar) >= similarity:
                        print("Did you mean '"+ss[similar.index(max(similar))][0]+"'?")
                    print("Try 'python "+name+".py --help' for more information.")
            except ImportError as e:
                print(name+": error on module import or execution of '"+p["method"][i]+"'")
                if debug: print("msg: "+str(e))
            return
    
    if missing:
        ml = [len(i) for i in missing]
        m = missing[ml.index(min(ml))] # find least missing arguments, closest to whats given
        print(name+": missing "+str(len(m))+" argument"+("s" if len(m) > 1 else "")+": '"+to_str(m, " ")+"'\nTry 'python "+name+".py --help' for more information.")
    else:
        print(name+": "+("invalid option '"+to_str(args, " ")+"'" if len(args) > 0 else "no arguments given")+"\nTry 'python "+name+".py --help' for more information.")

if __name__ == "__main__":
    with open(folder+"/parameters.json", "r") as f:
        syntax = json.load(f)
        f.close()
    match(sys.argv[1:], syntax, name, False)