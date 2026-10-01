from concurrent.futures import ThreadPoolExecutor
from statistics import median
from time import perf_counter

def noop():
    pass

def measure(workers, tasks=10_000):
    start = perf_counter()
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(noop) for _ in range(tasks)]
        for future in futures:
            future.result()
    return perf_counter() - start

previous = None
for workers in (1, 2, 4, 8, 16, 32):
    elapsed = median(measure(workers) for _ in range(7))

    if previous is None:
        print(f"{workers:2} workers: {elapsed * 1000:.2f} ms")
    else:
        prev_workers, prev_elapsed = previous
        incremental = (elapsed - prev_elapsed) / (workers - prev_workers)
        print(
            f"{workers:2} workers: {elapsed * 1000:.2f} ms; "
            f"{incremental * 1e6:+.2f} µs per additional worker"
        )

    previous = workers, elapsed


