# Monte Carlo Parallel Simulation (CSS3353)

## Project Overview
This project explores parallelization techniques for Monte Carlo simulations using Python's `multiprocessing` library. We evaluate different workload partitioning strategies (Static, Dynamic, and Guided) to optimize computing performance and mitigate potential load imbalances.

## Team Members
* **Elin Tiong Yi Ning** - Baseline implementation & Static Scheduling
* **Ealene Ting Hiong Siew** - Dynamic Scheduling & Task Queue Logic
* **Emely Kong Ning** - Parallelism analysis, Task Dependency Graph 
* **John Eli Anak Ngelai** - Performance Benchmarking

## File Structure
* `static.py` - Contains serial baseline and static parallel Monte Carlo implementation.

## How to Run
Run the static parallel simulation script:
```bash
python static.py