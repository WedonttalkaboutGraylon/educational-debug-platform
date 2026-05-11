import sys, importlib.util
def load_solution(path):
    spec = importlib.util.spec_from_file_location("solution", path); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
def run_tests(solution_path):
    mod = load_solution(solution_path); results = []
    tests = [("is_prime(2)", lambda: mod.is_prime(2), True),("is_prime(1)", lambda: mod.is_prime(1), False),("is_prime(7)", lambda: mod.is_prime(7), True),("is_prime(9)", lambda: mod.is_prime(9), False),("is_prime(13)", lambda: mod.is_prime(13), True),("is_prime(0)", lambda: mod.is_prime(0), False)]
    passed = failed = 0
    for name, fn, expected in tests:
        try:
            got = fn()
            if got == expected: results.append({"test":name,"status":"pass","expected":expected,"got":got}); passed+=1
            else: results.append({"test":name,"status":"fail","expected":expected,"got":got}); failed+=1
        except Exception as e: results.append({"test":name,"status":"error","message":str(e)}); failed+=1
    print({"passed":passed,"failed":failed,"total":passed+failed,"results":results})
if __name__ == "__main__": run_tests(sys.argv[1])
