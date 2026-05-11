import os
import sys
import json
import subprocess
import tempfile
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

PROBLEMS_DIR = Path(os.environ.get("PROBLEMS_DIR", Path(__file__).parent.parent / "problems"))

# In-memory progress store
_progress: dict = {}


class RunRequest(BaseModel):
    code: str
    language: str = "python"

class SubmitRequest(BaseModel):
    code: str
    problem_id: Optional[str] = ""
    language: Optional[str] = "python"

class ProgressRequest(BaseModel):
    problem_id: str
    completed: bool


def find_problem_dir(problem_id: str, language: str) -> Path | None:
    lang_map = {"python": "Python", "typescript": "TypeScript", "cpp": "CPP"}
    lang_folder = lang_map.get(language.lower(), "Python")
    lang_dir = PROBLEMS_DIR / lang_folder
    if not lang_dir.exists():
        return None
    for folder in lang_dir.iterdir():
        if folder.is_dir() and folder.name == problem_id:
            return folder
    return None


def run_python(code: str, timeout: int = 10) -> dict:
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False, encoding="utf-8") as f:
        f.write(code)
        tmp = f.name
    try:
        result = subprocess.run(
            [sys.executable, tmp],
            capture_output=True, text=True, timeout=timeout
        )
        return {"stdout": result.stdout, "stderr": result.stderr, "returncode": result.returncode}
    except subprocess.TimeoutExpired:
        return {"stdout": "", "stderr": "Timed out after 10 seconds. Check for infinite loops.", "returncode": -1}
    except Exception as e:
        return {"stdout": "", "stderr": str(e), "returncode": -1}
    finally:
        try: os.unlink(tmp)
        except: pass


def run_typescript(code: str, timeout: int = 10) -> dict:
    with tempfile.NamedTemporaryFile(suffix=".ts", mode="w", delete=False, encoding="utf-8") as f:
        f.write(code)
        tmp = f.name
    try:
        result = subprocess.run(
            ["npx", "ts-node", "--skip-project", tmp],
            capture_output=True, text=True, timeout=timeout
        )
        return {"stdout": result.stdout, "stderr": result.stderr, "returncode": result.returncode}
    except subprocess.TimeoutExpired:
        return {"stdout": "", "stderr": "Timed out.", "returncode": -1}
    except Exception as e:
        return {"stdout": "", "stderr": str(e), "returncode": -1}
    finally:
        try: os.unlink(tmp)
        except: pass


def run_cpp(code: str, timeout: int = 15) -> dict:
    with tempfile.NamedTemporaryFile(suffix=".cpp", mode="w", delete=False, encoding="utf-8") as f:
        f.write(code)
        tmp_cpp = f.name
    tmp_exe = tmp_cpp.replace(".cpp", "")
    try:
        compile_result = subprocess.run(
            ["g++", tmp_cpp, "-o", tmp_exe, "-std=c++17"],
            capture_output=True, text=True, timeout=30
        )
        if compile_result.returncode != 0:
            return {"stdout": "", "stderr": compile_result.stderr, "returncode": compile_result.returncode}
        run_result = subprocess.run([tmp_exe], capture_output=True, text=True, timeout=timeout)
        return {"stdout": run_result.stdout, "stderr": run_result.stderr, "returncode": run_result.returncode}
    except subprocess.TimeoutExpired:
        return {"stdout": "", "stderr": "Timed out.", "returncode": -1}
    except FileNotFoundError:
        return {"stdout": "", "stderr": "g++ not found.", "returncode": -1}
    except Exception as e:
        return {"stdout": "", "stderr": str(e), "returncode": -1}
    finally:
        try: os.unlink(tmp_cpp)
        except: pass
        try: os.unlink(tmp_exe)
        except: pass


@app.get("/")
def root():
    return {"status": "Educational Debug Platform API running"}


@app.get("/problems")
def list_problems():
    problems = []
    if not PROBLEMS_DIR.exists():
        return problems
    for lang_folder in sorted(PROBLEMS_DIR.iterdir()):
        if not lang_folder.is_dir():
            continue
        for prob_folder in sorted(lang_folder.iterdir()):
            if not prob_folder.is_dir():
                continue
            meta_path = None
            for f in prob_folder.iterdir():
                if f.name.endswith("_metadata.json"):
                    meta_path = f
                    break
            if not meta_path:
                meta_path = prob_folder / "metadata.json"
            if meta_path and meta_path.exists():
                with open(meta_path, encoding="utf-8") as f:
                    try:
                        meta = json.load(f)
                        meta["folder"] = prob_folder.name
                        meta["completed"] = _progress.get(prob_folder.name, False)
                        problems.append(meta)
                    except:
                        pass
    return problems


@app.get("/problems/{language}/{problem_id}")
def get_problem(language: str, problem_id: str):
    prob_dir = find_problem_dir(problem_id, language)
    if not prob_dir:
        return {"error": "Problem not found"}

    meta_path = None
    for f in prob_dir.iterdir():
        if f.name.endswith("_metadata.json"):
            meta_path = f
            break
    if not meta_path:
        meta_path = prob_dir / "metadata.json"

    if not meta_path or not meta_path.exists():
        return {"error": "Metadata not found"}

    with open(meta_path, encoding="utf-8") as f:
        meta = json.load(f)

    ext_map = {"python": ".py", "typescript": ".ts", "cpp": ".cpp"}
    ext = ext_map.get(language.lower(), ".py")
    starter_code = ""
    for f in prob_dir.iterdir():
        if f.name.endswith(f"_starter{ext}") or f.name == f"starter{ext}":
            with open(f, encoding="utf-8") as sf:
                starter_code = sf.read()
            break

    meta["folder"] = prob_dir.name
    meta["starter_code"] = starter_code
    meta["completed"] = _progress.get(problem_id, False)
    return meta


@app.post("/run")
def run_code(req: RunRequest):
    lang = req.language.lower()
    if lang == "python":
        result = run_python(req.code)
    elif lang == "typescript":
        result = run_typescript(req.code)
    elif lang == "cpp":
        result = run_cpp(req.code)
    else:
        return {"output": "", "error": f"Language '{req.language}' not supported.", "success": False}
    return {"output": result["stdout"], "error": result["stderr"], "success": result["returncode"] == 0}


@app.post("/submit")
def submit_code(req: SubmitRequest):
    if not req.problem_id:
        return {"error": "No problem ID provided.", "passed": False}

    prob_dir = find_problem_dir(req.problem_id, req.language or "python")
    if not prob_dir:
        return {"error": f"Problem not found.", "passed": False}

    ext_map = {"python": ".py", "typescript": ".ts", "cpp": ".cpp"}
    ext = ext_map.get((req.language or "python").lower(), ".py")

    with tempfile.NamedTemporaryFile(suffix=ext, mode="w", delete=False, encoding="utf-8") as f:
        f.write(req.code)
        tmp_path = f.name

    try:
        test_file = None
        for search_dir in [prob_dir / "Test", prob_dir]:
            if search_dir.exists():
                for tf in sorted(search_dir.iterdir()):
                    if tf.suffix == ".py" and "test" in tf.name.lower():
                        test_file = tf
                        break
            if test_file:
                break

        if not test_file:
            return {"error": "No test file found.", "passed": False}

        result = subprocess.run(
            [sys.executable, str(test_file), tmp_path],
            capture_output=True, text=True, timeout=15
        )

        output_text = result.stdout.strip()
        if not output_text:
            return {"error": f"Test runner produced no output. {result.stderr}", "passed": False}

        try:
            test_results = eval(output_text)
        except:
            try:
                test_results = json.loads(output_text)
            except:
                return {"error": "Could not parse test output.", "passed": False}

        passed = test_results.get("failed", 1) == 0
        if passed:
            _progress[req.problem_id] = True

        return {
            "passed": passed,
            "results": test_results.get("results", []),
            "summary": f"{test_results.get('passed', 0)}/{test_results.get('total', 0)} tests passed"
        }

    except subprocess.TimeoutExpired:
        return {"error": "Submission timed out.", "passed": False}
    except Exception as e:
        return {"error": str(e), "passed": False}
    finally:
        try: os.unlink(tmp_path)
        except: pass


@app.post("/progress")
def update_progress(req: ProgressRequest):
    _progress[req.problem_id] = req.completed
    return {"status": "ok"}


@app.get("/progress")
def get_progress():
    return _progress


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
