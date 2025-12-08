import numpy as np
from concurrent.futures import ThreadPoolExecutor

def process(args):
    data, i = args
    previous = 0 if i == 0 else data[i - 1, -1] # previous may not be set
    data[i, -1] = previous + data[i, :-1].sum()

data = np.arange(1_000_000).reshape(10_000, 100)
data[:, -1] = 0  # Initialize cumsum column
expected = data[:, :-1].sum()

with ThreadPoolExecutor(max_workers=8) as executor:
    executor.map(process, ((data, i) for i in range(len(data))))

print(f"Expected: {expected:,}, Found: {data[-1, -1]:,}, Diff: {expected - data[-1, -1]:,}")
