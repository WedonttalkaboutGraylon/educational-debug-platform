import subprocess, tempfile, os, sys

def run_tests(filepath):
    test_cases = [(0,1,"zero"),(1,1,"one"),(2,2,"two"),(3,6,"three"),(4,24,"four"),(5,120,"five")]
    passed=failed=0; results=[]
    for n, exp, label in test_cases:
        code = open(filepath).read().replace("cout << factorial(5)","cout << factorial(" + str(n) + ")")
        with tempfile.NamedTemporaryFile(suffix=".cpp", mode="w", delete=False) as f:
            f.write(code); tmp_cpp = f.name
        exe = tmp_cpp.replace(".cpp","")
        try:
            subprocess.run(["g++", tmp_cpp, "-o", exe], capture_output=True, timeout=10)
            r = subprocess.run([exe], capture_output=True, text=True, timeout=5)
            got = int(r.stdout.strip())
            if got == exp: passed+=1; results.append({"test":label,"status":"pass"})
            else: failed+=1; results.append({"test":label,"status":"fail","expected":exp,"got":got})
        except Exception as e: failed+=1; results.append({"test":label,"status":"error","message":str(e)})
        finally:
            for f in [tmp_cpp, exe]:
                try: os.unlink(f)
                except: pass
    return {"passed":passed,"failed":failed,"total":len(test_cases),"results":results}

if __name__=="__main__":
    print(run_tests(sys.argv[1] if len(sys.argv)>1 else "starter.cpp"))
