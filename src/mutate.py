import numpy as np
from concurrent.futures import ThreadPoolExecutor

# def process(args):
#     data, i = args
#     previous = 0 if i == 0 else data[i - 1, -1] # previous may not be set
#     data[i, -1] = previous + data[i, :-1].sum()

# data = np.arange(1_000_000).reshape(10_000, 100)
# data[:, -1] = 0  # Initialize cumsum column
# # data.flags.writeable = False
# expected = data[:, :-1].sum()

# with ThreadPoolExecutor(max_workers=8) as executor:
#     for f in executor.map(process, ((data, i) for i in range(len(data)))):
#         pass

# print(f"Expected: {expected:,}, Found: {data[-1, -1]:,}, Diff: {expected - data[-1, -1]:,}")

data = [0]

def increment(_):
    for _ in range(100_000):
        data[0] += 1  # read, add, write: not atomic

with ThreadPoolExecutor(max_workers=8) as executor:
    executor.map(increment, range(8))

print(f"Expected: {800_000:,}, Found: {data[0]:,}")

# data = np.zeros(1_000, dtype=np.int64)
# window = 10

# def process(start):
#     for _ in range(1_000):
#         data[start:start + window] += 1  # windows overlap their neighbors

# starts = range(0, len(data) - window, window // 2)
# with ThreadPoolExecutor(max_workers=8) as executor:
#     executor.map(process, starts)

# expected = np.zeros_like(data)
# for s in starts:
#     expected[s:s + window] += 1_000
# print(f"Mismatched elements: {(data != expected).sum()} of {len(data)}")

rng = np.random.default_rng(0)
signal = rng.random(1_000_000)
kernel = rng.random(10)
chunk = 100

out = np.zeros(len(signal) + len(kernel) - 1)

def process(start):
    result = np.convolve(signal[start:start + chunk], kernel)
    out[start:start + len(result)] += result  # tails overlap the next chunk

with ThreadPoolExecutor(max_workers=8) as executor:
    executor.map(process, range(0, len(signal), chunk))

expected = np.convolve(signal, kernel)
print(f"Mismatched elements: {(~np.isclose(out, expected)).sum():,} of {len(out):,}")
