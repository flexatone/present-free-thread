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
    t0 = time()
    a2 = np.fromiter((f(row) for row in a1), dtype=float, count=a1.shape[0])
    print(time() - t0)
    print(a2.shape)


    with ThreadPoolExecutor() as ex:
        t0 = time()
        a3 = np.fromiter(ex.map(f, a1), dtype=float, count=a1.shape[0])
        print(time() - t0)
        print(a3.shape)

if __name__ == '__main__':
    main()