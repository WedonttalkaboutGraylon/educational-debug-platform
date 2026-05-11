import importlib.util, sys

def load(fp):
    spec = importlib.util.spec_from_file_location("s", fp)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def run_tests(fp):
    f = load(fp).find_maximum
    cases = [([3,7,2,9,4],9,"max at end"),([1,2,3,4,5],5,"sorted asc"),([5,4,3,2,1],5,"sorted desc"),([3,3,3],3,"all same"),([-5,-1,-3],-1,"negatives"),([0,100,50],100,"max middle"),([42],42,"single"),([-10,0,10],10,"mixed")]
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
