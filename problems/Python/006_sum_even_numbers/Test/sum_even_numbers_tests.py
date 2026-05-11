import importlib.util, sys

def load(fp):
    spec = importlib.util.spec_from_file_location("s", fp)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def run_tests(fp):
    f = load(fp).sum_even
    cases = [([1,2,3,4,5,6],12,"mixed"),([1,3,5],0,"all odd"),([2,4,6],12,"all even"),([0],0,"zero"),([10,20,30],60,"tens"),([-2,-4,1],(-6),"negatives")]
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
