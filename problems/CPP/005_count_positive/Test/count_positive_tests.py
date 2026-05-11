import subprocess, tempfile, os, sys

def run_tests(filepath):
    test_cases = [([1,-2,3,-4,5],3,"mixed"),([-1,-2,-3],0,"all neg"),([1,2,3],3,"all pos"),([0,1,2],2,"with zero"),([0],0,"just zero")]
    passed=failed=0; results=[]
    for nums, exp, label in test_cases:
        arr_init = ",".join(map(str,nums)); size = len(nums)
        code = open(filepath).read().replace(
            "int arr[] = {1, -2, 3, -4, 5};\n    cout << countPositive(arr, 5)",
            f"int arr[] = {{{arr_init}}};\n    cout << countPositive(arr, {size})"
        )
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
