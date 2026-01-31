import os
import sys
import time
import random
import statistics

# ensure src is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from MatchingAndVerifying import GaleShapley, verify

try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None


def generate_prefs(n, seed=None):
    if seed is not None:
        random.seed(seed)
    hospitals = []
    students = []
    for _ in range(n):
        perm = list(range(n))
        random.shuffle(perm)
        hospitals.append(perm[:])
    for _ in range(n):
        perm = list(range(n))
        random.shuffle(perm)
        students.append(perm[:])
    return hospitals, students


def run_bench(ns, trials=3, seed=0):
    results = []  # list of (n, match_time, verify_time)
    for n in ns:
        match_times = []
        verify_times = []
        for t in range(trials):
            hospitals, students = generate_prefs(n, seed=seed + t)

            t0 = time.perf_counter()
            pairs = GaleShapley(n, hospitals, students)
            t1 = time.perf_counter()
            match_times.append(t1 - t0)

            t2 = time.perf_counter()
            _ = verify(n, hospitals, students, pairs)
            t3 = time.perf_counter()
            verify_times.append(t3 - t2)

        results.append((n, statistics.mean(match_times), statistics.mean(verify_times)))
        print(f"n={n}: match={results[-1][1]:.6f}s, verify={results[-1][2]:.6f}s")
    return results


def save_csv(results, path):
    with open(path, "w") as f:
        f.write("n,match_time,verify_time\n")
        for n, mt, vt in results:
            f.write(f"{n},{mt},{vt}\n")


def plot_results(results, outpath):
    if plt is None:
        return
    ns = [r[0] for r in results]
    mt = [r[1] for r in results]
    vt = [r[2] for r in results]

    plt.figure(figsize=(8,5))
    plt.plot(ns, mt, marker='o', label='Matcher (Gale-Shapley)')
    plt.plot(ns, vt, marker='o', label='Verifier')
    plt.xlabel('n (number of hospitals/students)')
    plt.ylabel('time (seconds)')
    plt.title('Scalability: matching and verifying')
    plt.legend()
    plt.grid(True)
    plt.savefig(outpath)
    plt.close()


def main():
    ns = [1,2,4,8,16,32,64,128,256,512]
    trials = 5
    print("Running benchmarks")

    results = run_bench(ns, trials=trials, seed=42)

    os.makedirs('outputs', exist_ok=True)
    csv_path = os.path.join('outputs', 'times.csv')
    png_path = os.path.join('outputs', 'benchmark.png')
    save_csv(results, csv_path)
    plot_results(results, png_path)

    print(f"Wrote CSV to {csv_path}")
    if plt is not None:
        print(f"Wrote plot to {png_path}")
    print("Done.")


if __name__ == '__main__':
    main()
