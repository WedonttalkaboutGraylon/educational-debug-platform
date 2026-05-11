import importlib.util, sys

def load(fp):
    spec = importlib.util.spec_from_file_location("s", fp)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def run_tests(fp):
    f = load(fp).remove_duplicates
    cases = [([1,2,2,3,3,3],[1,2,3],"basic"),([1,1,1],[1],"all same"),([1,2,3],[1,2,3],"no dups"),([],[],  "empty"),([3,1,2,1,3],[3,1,2],"preserve order")]
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
