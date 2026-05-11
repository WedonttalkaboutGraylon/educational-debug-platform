import importlib.util, sys

def load(fp):
    spec = importlib.util.spec_from_file_location("s", fp)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def run_tests(fp):
    f = load(fp).count_negatives
    cases = [
        ([-1,2,-3,4], 2, "two negatives"),
        ([1,2,3], 0, "no negatives"),
        ([0,-1], 1, "zero not negative"),
        ([], 0, "empty list"),
        ([-1,-2,-3], 3, "all negative"),
        ([0,0,0], 0, "all zeros"),
    ]
    passed=failed=0; results=[]
    for nums,exp,label in cases:
        try:
            r=f(nums)
            if r==exp: passed+=1; results.append({"test":label,"status":"pass"})
            else: failed+=1; results.append({"test":label,"status":"fail","expected":exp,"got":r,"input":nums})
        except Exception as e: failed+=1; results.append({"test":label,"status":"error","message":str(e),"input":nums})
    return {"passed":passed,"failed":failed,"total":len(cases),"results":results}

if __name__=="__main__":
    print(run_tests(sys.argv[1] if len(sys.argv)>1 else "starter.py"))
