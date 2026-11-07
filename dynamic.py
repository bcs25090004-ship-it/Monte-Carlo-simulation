import multiprocessing as mp
import random
import time

# 1. Worker function: fetches chunks from task_queue until None is received
def dynamic_worker(task_queue, result_queue):
    while True:
        task = task_queue.get()
        if task is None:  # Sentinel value to stop process
            break
        
        chunk_size, seed = task
        random.seed(seed)
        
        count = 0
        for _ in range(chunk_size):
            x = random.random()
            y = random.random()
            if x * x + y * y <= 1.0:
                count += 1
                
        result_queue.put(count)

# 2. Main Dynamic Scheduling Function
def dynamic_parallel_monte_carlo(total_samples, num_processes, chunk_size=50000):
    task_queue = mp.Queue()
    result_queue = mp.Queue()
    
    # Divide total samples into small task chunks
    num_chunks = total_samples // chunk_size
    remainder = total_samples % chunk_size
    
    # Populate the task queue
    for i in range(num_chunks):
        task_queue.put((chunk_size, 42 + i))
        
    if remainder > 0:
        task_queue.put((remainder, 42 + num_chunks))
        num_chunks += 1

    # Add poison pills (None) to terminate workers gracefully
    for _ in range(num_processes):
        task_queue.put(None)

    # Spawn worker processes
    processes = []
    for _ in range(num_processes):
        p = mp.Process(target=dynamic_worker, args=(task_queue, result_queue))
        p.start()
        processes.append(p)

    # Collect partial results from the result queue
    total_inside = 0
    for _ in range(num_chunks):
        total_inside += result_queue.get()

    # Wait for all processes to complete
    for p in processes:
        p.join()

    pi_estimate = (4 * total_inside) / total_samples
    return pi_estimate

if __name__ == "__main__":
    TOTAL_SAMPLES = 10_000_000
    NUM_PROCESSES = 8
    CHUNK_SIZE = 50_000

    print("Running Dynamic Scheduling Monte Carlo Simulation...")
    start_time = time.time()
    pi_result = dynamic_parallel_monte_carlo(TOTAL_SAMPLES, NUM_PROCESSES, CHUNK_SIZE)
    elapsed_time = time.time() - start_time

    print(f"[Dynamic Parallel ({NUM_PROCESSES} procs)] Time: {elapsed_time:.4f}s | Pi: {pi_result:.6f}")