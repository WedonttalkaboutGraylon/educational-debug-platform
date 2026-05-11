import importlib.util, sys, math

def load(fp):
    spec = importlib.util.spec_from_file_location("s", fp)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def run_tests(fp):
    f = load(fp).factorial
    cases = [
        (0, 1, "zero"),
        (1, 1, "one"),
        (5, 120, "five"),
        (10, 3628800, "ten"),
        (-1, -1, "negative returns -1"),
        (-100, -1, "large negative returns -1"),
        (20, math.factorial(20), "twenty"),
        (50, math.factorial(50), "large input no crash"),
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
