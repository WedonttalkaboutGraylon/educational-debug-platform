import importlib.util, sys

def load(fp):
    spec = importlib.util.spec_from_file_location("s", fp)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def run_tests(fp):
    f = load(fp).is_prime
    cases = [(2,True,"2 is prime"),(3,True,"3 is prime"),(4,False,"4 not prime"),(9,False,"9 not prime"),(7,True,"7 is prime"),(25,False,"25 not prime"),(1,False,"1 not prime"),(0,False,"0 not prime"),(13,True,"13 is prime")]
    passed=failed=0; results=[]
    for n,exp,label in cases:
        try:
            r=f(n)
            if r==exp: passed+=1; results.append({"test":label,"status":"pass"})
            else: failed+=1; results.append({"test":label,"status":"fail","expected":exp,"got":r})
        except Exception as e: failed+=1; results.append({"test":label,"status":"error","message":str(e)})
    return {"passed":passed,"failed":failed,"total":len(cases),"results":results}

if __name__=="__main__":
    print(run_tests(sys.argv[1] if len(sys.argv)>1 else "starter.py"))
