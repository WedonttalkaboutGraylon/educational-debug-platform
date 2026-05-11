import sys, importlib.util
def load_solution(path):
    spec = importlib.util.spec_from_file_location("solution", path); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
def run_tests(solution_path):
    mod = load_solution(solution_path); results = []
    tests = [("reverse_string('hello')", lambda: mod.reverse_string("hello"), "olleh"),("reverse_string('a')", lambda: mod.reverse_string("a"), "a"),("reverse_string('')", lambda: mod.reverse_string(""), ""),("reverse_string('Python')", lambda: mod.reverse_string("Python"), "nohtyP"),("reverse_string('12345')", lambda: mod.reverse_string("12345"), "54321")]
    passed = failed = 0
    for name, fn, expected in tests:
        try:
            got = fn()
            if got == expected: results.append({"test":name,"status":"pass","expected":expected,"got":got}); passed+=1
            else: results.append({"test":name,"status":"fail","expected":expected,"got":got}); failed+=1
        except Exception as e: results.append({"test":name,"status":"error","message":str(e)}); failed+=1
    print({"passed":passed,"failed":failed,"total":passed+failed,"results":results})
if __name__ == "__main__": run_tests(sys.argv[1])
