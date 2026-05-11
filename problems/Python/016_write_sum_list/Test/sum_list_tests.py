import importlib.util, sys

def load(fp):
    spec = importlib.util.spec_from_file_location("s", fp)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def run_tests(fp):
    f = load(fp).sum_list
    cases = [
        ([1,2,3], 6, [1,2,3], "basic sum"),
        ([], 0, [], "empty list"),
        ([-1,1], 0, [-1,1], "negatives cancel"),
        ([10], 10, [10], "single element"),
        ([100,200,300], 600, [100,200,300], "large numbers"),
        ([-5,-3,-2], -10, [-5,-3,-2], "all negatives"),
    ]
    passed=failed=0; results=[]
    for nums,exp,inp,label in cases:
        try:
            r=f(nums)
            if r==exp: passed+=1; results.append({"test":label,"status":"pass"})
            else: failed+=1; results.append({"test":label,"status":"fail","expected":exp,"got":r,"input":inp})
        except Exception as e: failed+=1; results.append({"test":label,"status":"error","message":str(e),"input":inp})
    return {"passed":passed,"failed":failed,"total":len(cases),"results":results}

if __name__=="__main__":
    print(run_tests(sys.argv[1] if len(sys.argv)>1 else "starter.py"))
