import sys, subprocess, tempfile, os

def run_tests(solution_path):
    results = []
    tests = [("fibonacci(0)", 0, 0),("fibonacci(1)", 1, 1),("fibonacci(6)", 6, 8),("fibonacci(10)", 10, 55),("fibonacci(2)", 2, 1)]
    passed = failed = 0
    solution_code = open(solution_path).read().split("int main()")[0]
    for name, arg, expected in tests:
        test_code = f"""
#include <iostream>
using namespace std;
{solution_code}
int main() {{
    cout << fibonacci({arg}) << endl;
    return 0;
}}
"""
        with tempfile.NamedTemporaryFile(suffix=".cpp", mode="w", delete=False) as f:
            f.write(test_code); tmp_cpp = f.name
        tmp_exe = tmp_cpp.replace(".cpp","")
        try:
            cr = subprocess.run(["g++", tmp_cpp, "-o", tmp_exe, "-std=c++17"], capture_output=True, text=True, timeout=30)
            if cr.returncode != 0: results.append({"test":name,"status":"error","message":cr.stderr}); failed+=1; continue
            rr = subprocess.run([tmp_exe], capture_output=True, text=True, timeout=10)
            got = int(rr.stdout.strip())
            if got == expected: results.append({"test":name,"status":"pass","expected":expected,"got":got}); passed+=1
            else: results.append({"test":name,"status":"fail","expected":expected,"got":got}); failed+=1
        except Exception as e: results.append({"test":name,"status":"error","message":str(e)}); failed+=1
        finally:
            try: os.unlink(tmp_cpp)
            except: pass
            try: os.unlink(tmp_exe)
            except: pass
    print({"passed":passed,"failed":failed,"total":passed+failed,"results":results})

if __name__ == "__main__": run_tests(sys.argv[1])
