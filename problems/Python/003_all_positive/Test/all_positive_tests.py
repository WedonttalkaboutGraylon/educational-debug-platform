import importlib.util, sys

def load(fp):
    spec = importlib.util.spec_from_file_location("s", fp)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def run_tests(fp):
    f = load(fp).all_positive
    cases = [([1,2,3],True,"all pos"),([1,0,3],False,"zero present"),([0,0,0],False,"all zeros"),([-1,2,3],False,"neg present"),([1,2,-3],False,"neg at end"),([100,200],True,"large pos"),([1],True,"single pos"),([0],False,"single zero"),([1,2,0,4],False,"zero middle")]
    passed=failed=0; results=[]
    for nums,exp,label in cases:
        try:
            r=f(nums)
            if r==exp: passed+=1; results.append({"test":label,"status":"pass"})
            else: failed+=1; results.append({"test":label,"status":"fail","expected":exp,"got":r})
        except Exception as e: failed+=1; results.append({"test":label,"status":"error","message":str(e)})
    return {"passed":passed,"failed":failed,"total":len(cases),"results":results}

if __name__=="__main__":
    print(run_tests(sys.argv[1] if len(sys.argv)>1 else "starter.py"))
