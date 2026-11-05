import time
import random
import multiprocessing as mp

#1. Serial Baseline
def serial_monte_carlo(num_samples):
    count = 0
    for _ in range(num_samples):
        x = random.random()
        y = random.random()
        if x*x + y*y <= 1.0:
            count += 1
    return count
   
#2.0 static multiprocessing
def static_worker(sample_per_worker, seed):
    random.seed(seed)
    count = 0
    for _ in range(sample_per_worker):
        x = random.random()
        y = random.random()
        if x*x + y*y <= 1.0:
            count += 1
    return count

#3.0 Static scheduling
def static_parallel_monte_carlo(total_samples, num_processes):
    samples_per_process = total_samples // num_processes
    tasks = [(samples_per_process, 42 + i) for i in range(num_processes)]

    with mp.Pool(processes=num_processes) as pool:
        results = pool.starmap(static_worker, tasks)

    return sum(results)

if __name__ == "__main__":
    mp.freeze_support()
    N = 50_000_000 # Number of samples
    P = 8 # Number of processes

    #--Serial Baseline--
    t0 = time.time()
    serial_hits = serial_monte_carlo (N)
    t_serial = time.time() - t0
    pi_serial = 4 * serial_hits / N
    print(f"[Serial Baseline] Time: {t_serial:.4f}s | Pi: {pi_serial:.6f}")

    #--Static Scheduling--
    t1 = time.time()
    static_hits = static_parallel_monte_carlo(N, P)
    t_static = time.time() - t1
    pi_static = 4 * static_hits / N
    print(f"[Static Parallel ({P} procs)] Time: {t_static:.4f}s | Pi: {pi_static:.6f}")

    #calculate speedup
    speedup = t_serial / t_static
    print(f"Speedup: {speedup:.2f}x")