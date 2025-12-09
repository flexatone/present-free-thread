from time import time
from concurrent.futures import ThreadPoolExecutor
import numpy as np


def main():

    a1 = np.arange(100_000_000).reshape(10_000, 10_000)

    def f_x(row):
        return (row**2).sum()

    def f(row): # NOTE: as soon as we do selection
        # return ((row * 0.5)**2).sum()  # this is about equal
        # return (((row * 0.5) + 100)**2).sum()  # FT starts to outperform
        return (row[row % 2 == 0]**2).sum()  # FT way outperforns

    # can use result = np.apply_along_axis(f, axis=1, arr=A)
    print('sequential proc')
    t0 = time()
    a2 = np.fromiter((f(row) for row in a1), dtype=float, count=a1.shape[0])
    print(time() - t0)
    print(a2.shape)

    print('threading proc')
    with ThreadPoolExecutor() as ex:
        t0 = time()
        a3 = np.fromiter(ex.map(f, a1), dtype=float, count=a1.shape[0])
        print(time() - t0)
        print(a3.shape)



def test_sum():
    '''Multi-threading of sum is faster both with and without free-threading because processing is not bound by the GIL.
    '''

    a1 = np.arange(100_000_000).reshape(100, 1_000_000)


    print('np.sum(axis=1)')
    t0 = time()
    a2 = a1.sum(axis=1)
    print(time() - t0)
    print(a2.shape)

    def f(row):
        return row.sum()

    print('sequential row.sum()')
    t0 = time()
    a2 = np.fromiter((f(row) for row in a1), dtype=float, count=a1.shape[0])
    print(time() - t0)
    print(a2.shape)


    print('threaded row.sum()')
    with ThreadPoolExecutor() as ex:
        t0 = time()
        a3 = np.fromiter(ex.map(f, a1), dtype=float, count=a1.shape[0])
        print(time() - t0)
        print(a3.shape)

    # can out perform sum() on an axis
    # 0.014817953109741211
    # (100,)
    # 0.01017308235168457
    # (100,)
    # 0.007255077362060547
    # (100,)

if __name__ == '__main__':
    main()