import sys, subprocess, tempfile, os, json

def run_tests(solution_path):
    results = []
    tests = [("factorial(0)", 0, 1),("factorial(1)", 1, 1),("factorial(5)", 5, 120),("factorial(10)", 10, 3628800),("factorial(3)", 3, 6)]
    passed = failed = 0
    for name, arg, expected in tests:
        test_code = f"""
#include <iostream>
using namespace std;
long long factorial(int n);
{open(solution_path).read().split("int main()")[0]}
int main() {{
    cout << factorial({arg}) << endl;
    return 0;
}}
"""
        with tempfile.NamedTemporaryFile(suffix=".cpp", mode="w", delete=False) as f:
            f.write(test_code); tmp_cpp = f.name
        tmp_exe = tmp_cpp.replace(".cpp","")
        try:
            compile_result = subprocess.run(["g++", tmp_cpp, "-o", tmp_exe, "-std=c++17"], capture_output=True, text=True, timeout=30)
            if compile_result.returncode != 0:
                results.append({"test":name,"status":"error","message":compile_result.stderr}); failed+=1; continue
            run_result = subprocess.run([tmp_exe], capture_output=True, text=True, timeout=10)
            got = int(run_result.stdout.strip())
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
