import importlib.util, sys

def load(fp):
    spec = importlib.util.spec_from_file_location("s", fp)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def run_tests(fp):
    f = load(fp).reverse_list
    cases = [([1,2,3],[3,2,1],"basic"),([4,5,6,7],[7,6,5,4],"four items"),([1],[1],"single"),([1,2],[2,1],"two items"),([5,5,5],[5,5,5],"all same")]
    passed=failed=0; results=[]
    for lst,exp,label in cases:
        try:
            r=f(lst)
            if r==exp: passed+=1; results.append({"test":label,"status":"pass"})
            else: failed+=1; results.append({"test":label,"status":"fail","expected":exp,"got":r})
        except Exception as e: failed+=1; results.append({"test":label,"status":"error","message":str(e)})
    return {"passed":passed,"failed":failed,"total":len(cases),"results":results}

if __name__=="__main__":
    print(run_tests(sys.argv[1] if len(sys.argv)>1 else "starter.py"))
