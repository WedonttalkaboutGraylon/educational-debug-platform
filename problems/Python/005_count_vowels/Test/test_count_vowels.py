import sys, importlib.util
def load_solution(path):
    spec = importlib.util.spec_from_file_location("solution", path); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
def run_tests(solution_path):
    mod = load_solution(solution_path); results = []
    tests = [("count_vowels('hello')", lambda: mod.count_vowels("hello"), 2),("count_vowels('')", lambda: mod.count_vowels(""), 0),("count_vowels('AEIOU')", lambda: mod.count_vowels("AEIOU"), 5),("count_vowels('rhythm')", lambda: mod.count_vowels("rhythm"), 0),("count_vowels('Hello World')", lambda: mod.count_vowels("Hello World"), 3)]
    passed = failed = 0
    for name, fn, expected in tests:
        try:
            got = fn()
            if got == expected: results.append({"test":name,"status":"pass","expected":expected,"got":got}); passed+=1
            else: results.append({"test":name,"status":"fail","expected":expected,"got":got}); failed+=1
        except Exception as e: results.append({"test":name,"status":"error","message":str(e)}); failed+=1
    print({"passed":passed,"failed":failed,"total":passed+failed,"results":results})
if __name__ == "__main__": run_tests(sys.argv[1])
