# COP4533 — Programming Assignment 1: Matching and Verifying

**Students:** Constantinos Papanicolaou; UFID: 77981864

- **Files:**
  - Input example: [data/example.in](data/example.in)
  - Example output: [outputs/example.out](outputs/example.out)
  - Benchmark CSV: [outputs/times.csv](outputs/times.csv)
  - Benchmark plot: [outputs/benchmark.png](outputs/benchmark.png)

- **Run matcher and verifier:**
  - Using system Python (from project root):
    `python src/MatchingAndVerifying.py`

  - Using project virtualenv:
    `C:/Users/papan/OneDrive/Desktop/COP4533---Programming-Assignment-1/.venv/Scripts/python.exe src/MatchingAndVerifying.py`

  The script reads `data/example.in` and writes `outputs/example.out` as well as printing a verifier result

- **Run benchmark (Task C):**
  - Ensure `matplotlib` is installed in the environment, then run:
    `python src/benchmark.py`

  - Or with the project venv:
    `C:/Users/papan/OneDrive/Desktop/COP4533---Programming-Assignment-1/.venv/Scripts/python.exe src/benchmark.py`

  This generates `outputs/times.csv` as well as `outputs/benchmark.png` to view the graph.

- **Dependencies / assumptions:**
  - Python 3
  - `matplotlib`

