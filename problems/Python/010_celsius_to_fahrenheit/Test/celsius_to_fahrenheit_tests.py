import importlib.util, sys

def load(fp):
    spec = importlib.util.spec_from_file_location("s", fp)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def run_tests(fp):
    f = load(fp).celsius_to_fahrenheit
    cases = [(0,32.0,"freezing"),(100,212.0,"boiling"),(-40,-40.0,"same point"),(37,98.6,"body temp"),(20,68.0,"room temp")]
    passed=failed=0; results=[]
    for c,exp,label in cases:
        try:
            r=f(c)
            if abs(r-exp)<0.01: passed+=1; results.append({"test":label,"status":"pass"})
            else: failed+=1; results.append({"test":label,"status":"fail","expected":exp,"got":r})
        except Exception as e: failed+=1; results.append({"test":label,"status":"error","message":str(e)})
    return {"passed":passed,"failed":failed,"total":len(cases),"results":results}

if __name__=="__main__":
    print(run_tests(sys.argv[1] if len(sys.argv)>1 else "starter.py"))
