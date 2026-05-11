import importlib.util, sys

def load(fp):
    spec = importlib.util.spec_from_file_location("s", fp)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def run_tests(fp):
    f = load(fp).is_even
    cases = [
        (4, True, "even positive"),
        (7, False, "odd positive"),
        (0, True, "zero is even"),
        (-2, True, "negative even"),
        (-3, False, "negative odd"),
        (100, True, "large even"),
        (1, False, "one is odd"),
    ]
    passed=failed=0; results=[]
    for n,exp,label in cases:
        try:
            r=f(n)
            if r==exp: passed+=1; results.append({"test":label,"status":"pass"})
            else: failed+=1; results.append({"test":label,"status":"fail","expected":exp,"got":r,"input":n})
        except Exception as e: failed+=1; results.append({"test":label,"status":"error","message":str(e),"input":n})
    return {"passed":passed,"failed":failed,"total":len(cases),"results":results}

if __name__=="__main__":
    print(run_tests(sys.argv[1] if len(sys.argv)>1 else "starter.py"))
