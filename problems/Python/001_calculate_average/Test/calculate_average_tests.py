import importlib.util, sys

def load(fp):
    spec = importlib.util.spec_from_file_location("s", fp)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def run_tests(fp):
    f = load(fp).calculate_average
    cases = [([10,20,30],20.0,"basic"),([1,2,3,4,5],3.0,"five nums"),([100],100.0,"single"),([0,0,0],0.0,"zeros"),([-10,10],0.0,"neg pos"),([1,1,1,1],1.0,"same"),([7,14,21,28],17.5,"multiples")]
    passed=failed=0; results=[]
    for nums,exp,label in cases:
        try:
            r=f(nums)
            if abs(r-exp)<1e-9: passed+=1; results.append({"test":label,"status":"pass"})
            else: failed+=1; results.append({"test":label,"status":"fail","expected":exp,"got":r})
        except Exception as e: failed+=1; results.append({"test":label,"status":"error","message":str(e)})
    return {"passed":passed,"failed":failed,"total":len(cases),"results":results}

if __name__=="__main__":
    print(run_tests(sys.argv[1] if len(sys.argv)>1 else "starter.py"))
