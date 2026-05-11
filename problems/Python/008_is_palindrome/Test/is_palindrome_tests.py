import importlib.util, sys

def load(fp):
    spec = importlib.util.spec_from_file_location("s", fp)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def run_tests(fp):
    f = load(fp).is_palindrome
    cases = [("racecar",True,"racecar"),("hello",False,"hello"),("madam",True,"madam"),("A man a plan a canal Panama",True,"with spaces"),("python",False,"python"),("level",True,"level"),("",True,"empty"),("a",True,"single char")]
    passed=failed=0; results=[]
    for s,exp,label in cases:
        try:
            r=f(s)
            if r==exp: passed+=1; results.append({"test":label,"status":"pass"})
            else: failed+=1; results.append({"test":label,"status":"fail","expected":exp,"got":r})
        except Exception as e: failed+=1; results.append({"test":label,"status":"error","message":str(e)})
    return {"passed":passed,"failed":failed,"total":len(cases),"results":results}

if __name__=="__main__":
    print(run_tests(sys.argv[1] if len(sys.argv)>1 else "starter.py"))
