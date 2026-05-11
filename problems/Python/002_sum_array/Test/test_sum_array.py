import sys, importlib.util
def load_solution(path):
    spec = importlib.util.spec_from_file_location("solution", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
def run_tests(solution_path):
    mod = load_solution(solution_path)
    results = []
    tests = [("sum_array([1,2,3])", lambda: mod.sum_array([1,2,3]), 6),("sum_array([])", lambda: mod.sum_array([]), 0),("sum_array([-1,1])", lambda: mod.sum_array([-1,1]), 0),("sum_array([10,20,30])", lambda: mod.sum_array([10,20,30]), 60),("sum_array([5])", lambda: mod.sum_array([5]), 5)]
    passed = failed = 0
    for name, fn, expected in tests:
        try:
            got = fn()
            if got == expected: results.append({"test":name,"status":"pass","expected":expected,"got":got}); passed+=1
            else: results.append({"test":name,"status":"fail","expected":expected,"got":got}); failed+=1
        except Exception as e: results.append({"test":name,"status":"error","message":str(e)}); failed+=1
    print({"passed":passed,"failed":failed,"total":passed+failed,"results":results})
if __name__ == "__main__": run_tests(sys.argv[1])
