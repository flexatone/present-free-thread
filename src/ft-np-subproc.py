import time
import numpy as np
import sys
import os
import timeit
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import frame_fixtures as ff
import matplotlib.pyplot as plt
import numpy as np
import typing as tp

sys.path.append(os.getcwd())

import static_frame as sf
from static_frame.core.display_color import HexColor



#-------------------------------------------------------------------------------

class FTTest:
    SUFFIX = '.tmp'

    def __init__(self, fixture: str):
        # use .values to strip out array
        self.npa = ff.parse(fixture).values

    def __call__(self):
        raise NotImplementedError()


# def proc(row): # ess: even squared sum
#     return (row[row % 2 == 0] ** 2).sum()

# PROC_DESCRIPTION = '(row[row % 2 == 0]**2).sum()'

# def proc(row):
#     p = row / row.sum()
#     return -(p * np.log(p + 1e-12)).sum()

# PROC_DESCRIPTION = 'Shannon Entropy'

def proc(row): # ess: even squared sum
    return row.sum()

PROC_DESCRIPTION = 'sum()'



class ArrayMap_Single(FTTest):
    def __call__(self):
        _ = np.fromiter((proc(row) for row in self.npa), dtype=float, count=self.npa.shape[0])


# class ArrayMap_Process_Workers2(FTTest):
#     def __call__(self):
#         _ = self.npa.iter_series(axis=1).apply_pool(proc,
#                 chunksize=10, use_threads=False, max_workers=2)


# class ArrayMap_Process_Workers4(FTTest):
#     def __call__(self):
#         _ = self.npa.iter_series(axis=1).apply_pool(proc,
#                 chunksize=10, use_threads=False, max_workers=4)


# class ArrayMap_Process_Workers8(FTTest):
#     def __call__(self):
#         _ = self.npa.iter_series(axis=1).apply_pool(proc,
#                 chunksize=10, use_threads=False, max_workers=8)


# class ArrayMap_Process_Workers16(FTTest):
#     def __call__(self):
#         _ = self.npa.iter_series(axis=1).apply_pool(proc,
#                 chunksize=10, use_threads=False, max_workers=16)





class ArrayMap_Threads_Workers2(FTTest):
    def __call__(self):

        with ThreadPoolExecutor(max_workers=2) as ex:
            _ = np.fromiter(ex.map(proc, self.npa), dtype=float, count=self.npa.shape[0])

class ArrayMap_Threads_Workers4(FTTest):
    def __call__(self):

        with ThreadPoolExecutor(max_workers=4) as ex:
            _ = np.fromiter(ex.map(proc, self.npa), dtype=float, count=self.npa.shape[0])


class ArrayMap_Threads_Workers8(FTTest):
    def __call__(self):
        with ThreadPoolExecutor(max_workers=8) as ex:
            _ = np.fromiter(ex.map(proc, self.npa), dtype=float, count=self.npa.shape[0])

class ArrayMap_Threads_Workers16(FTTest):
    def __call__(self):
        with ThreadPoolExecutor(max_workers=16) as ex:
            _ = np.fromiter(ex.map(proc, self.npa), dtype=float, count=self.npa.shape[0])







#-------------------------------------------------------------------------------
NUMBER = 4

def scale(v):
    return int(v * 100)


FF_wide_bool = f's({scale(100)},{scale(10_000)})|v(bool)'
FF_wide_int   = f's({scale(100)},{scale(10_000)})|v(int)'
FF_wide_float = f's({scale(100)},{scale(10_000)})|v(float)'

FF_tall_bool = f's({scale(10_000)},{scale(100)})|v(bool)'
FF_tall_int   = f's({scale(10_000)},{scale(100)})|v(int)'
FF_tall_float   = f's({scale(10_000)},{scale(100)})|v(float)'

FF_square_bool = f's({scale(1_000)},{scale(1_000)})|v(bool)'
FF_square_int   = f's({scale(1_000)},{scale(1_000)})|v(int)'
FF_square_float = f's({scale(1_000)},{scale(1_000)})|v(float)'


FIXTURE_MAP = {
    'FF_wide_bool': FF_wide_bool,
    'FF_wide_int': FF_wide_int,
    'FF_wide_float': FF_wide_float,
    'FF_tall_bool': FF_tall_bool,
    'FF_tall_int': FF_tall_int,
    'FF_tall_float': FF_tall_float,
    'FF_square_bool': FF_square_bool,
    'FF_square_int': FF_square_int,
    'FF_square_float': FF_square_float,
    }


#-------------------------------------------------------------------------------

def seconds_to_display(seconds: float, number: int) -> str:
    seconds /= number
    if seconds < 1e-4:
        return f'{seconds * 1e6: .1f} (µs)'
    if seconds < 1e-1:
        return f'{seconds * 1e3: .1f} (ms)'
    return f'{seconds: .1f} (s)'

def plot_performance(frame: sf.Frame,
        *,
        number: int,
    ):
    fixture_total = len(frame['fixture'].unique())
    cat_total = len(frame['category'].unique())
    name_total = len(frame['name'].unique())

    fig, axes = plt.subplots(cat_total, fixture_total)

    # for legend
    name_replace = {
        ArrayMap_Single.__name__: 'sequential',
        ArrayMap_Threads_Workers2.__name__: 'max_workers=2',
        ArrayMap_Threads_Workers4.__name__: 'max_workers=4',
        ArrayMap_Threads_Workers8.__name__: 'max_workers=8',
        ArrayMap_Threads_Workers16.__name__: 'max_workers=16',
    }

    name_order = {
        ArrayMap_Single.__name__: 0,
        ArrayMap_Threads_Workers2.__name__: 11,
        ArrayMap_Threads_Workers4.__name__: 12,
        ArrayMap_Threads_Workers8.__name__: 13,
        ArrayMap_Threads_Workers16.__name__: 14,
    }

    # cmap = plt.get_cmap('terrain')
    cmap = plt.get_cmap('plasma')
    color_count = name_total
    color = cmap(np.arange(color_count) / color_count)

    # categories are read, write
    # import ipdb; ipdb.set_trace()
    for cat_count, (cat_label, cat) in enumerate(frame.iter_group_items('category')):
        for fixture_count, (fixture_label, fixture) in enumerate(
                cat.iter_group_items('fixture')):
            ax = axes[cat_count][fixture_count]

            # set order
            fixture = fixture.sort_values('name', key=lambda s:s.iter_element().map_all(name_order))
            results = fixture['time'].values.tolist()
            names = fixture['name'].values.tolist()
            x = np.arange(len(results))
            names_display = [name_replace[l] for l in names]
            post = ax.bar(names_display, results, color=color)

            # ax.set_ylabel()
            title = f'{cat_label}\n{FIXTURE_SHAPE_MAP[fixture_label]}'
            ax.set_title(title, fontsize=8)
            ax.set_box_aspect(0.75) # makes taller tan wide
            time_max = fixture['time'].max()
            time_min = fixture["time"].min()

            y_ticks = [0, time_min, time_max * 0.5, time_max]
            y_labels = ['',
                    seconds_to_display(time_min, number),
                    seconds_to_display(time_max * 0.5, number),
                    seconds_to_display(time_max, number),
                    ]

            if time_min > time_max * 0.333:
                # remove the min if it is greater than quarter
                y_ticks.pop(1)
                y_labels.pop(1)
            ax.set_yticks(y_ticks)
            ax.set_yticklabels(y_labels, fontsize=4)

            # ax.set_xticks(x, names_display, rotation='vertical')
            ax.tick_params(
                    axis='x',
                    which='both',
                    bottom=False,
                    top=False,
                    labelbottom=False,
                    )

    fig.set_size_inches(5.5, 3.5) # width, height
    fig.legend(post, names_display, loc='center right', fontsize=6)
    # horizontal, vertical
    count = ff.parse(FF_tall_bool).size

    fig.text(.05, .96, f'Array Row Processing: {count:.0e} Elements, {NUMBER} Iterations', fontsize=10)

    shape_map = {shape: FIXTURE_SHAPE_MAP[shape] for shape in frame['fixture'].unique()}
    shape_msg = ' / '.join(f'{v}: {k}' for k, v in shape_map.items())
    proc_msg = f'Processor: {PROC_DESCRIPTION}'

    msg = [get_versions(), shape_msg, proc_msg]
    fig.text(0.05, .87, '\n'.join(msg), fontsize=6)

    # fig.text(.05, .90, get_versions(), fontsize=6)
    # fig.text(.05, .89, shape_msg, fontsize=6)
    # fig.text(.05, .86, f'Processor: {PROC_DESCRIPTION}', fontsize=6)

    fp = '/tmp/ft-np-perf.png'

    plt.subplots_adjust(
            left=0.10,
            bottom=0.05,
            right=0.75,
            top=0.75,
            wspace=.5, # width
            hspace=1,
            )
    # plt.rcParams.update({'font.size': 22})
    plt.savefig(fp, dpi=600)

    if sys.platform.startswith('linux'):
        os.system(f'eog {fp}&')
    else:
        os.system(f'open {fp}')


#-------------------------------------------------------------------------------

def get_versions() -> str:
    import platform
    py_version = sys.version[:sys.version.find('(')].strip()
    return f'OS: {platform.system()} / Python: {py_version} / NumPy: {np.__version__}'

FIXTURE_SHAPE_MAP = {
    '100x1': 'Tall',
    '10x10': 'Square',
    '1x100': 'Wide',
    '1000x10': 'Tall',
    '100x100': 'Square',
    '10x1000': 'Wide',
    '10000x100': 'Tall',
    '1000x1000': 'Square',
    '100x10000': 'Wide',
    '100000x1000': 'Tall',
    '10000x10000': 'Square',
    '1000x100000': 'Wide',
}


def fixture_to_pair(label: str, fixture_name: str) -> tp.Tuple[str, str, str]:
    # get a title
    fixture = FIXTURE_MAP[fixture_name]
    f = ff.parse(fixture) # we inefficiently parse here just to get shape
    return label, f'{f.shape[0]:}x{f.shape[1]}', fixture, fixture_name

CLS_READ = (
    ArrayMap_Single,
    ArrayMap_Threads_Workers2,
    ArrayMap_Threads_Workers4,
    ArrayMap_Threads_Workers8,
    ArrayMap_Threads_Workers16,
    )

CLS_MAP = {cls.__name__: cls for cls in CLS_READ}

def run_test(subproc: bool = True):

    py_exet = Path.home() / '.env314t-ft/bin/python3'
    py_exe = Path.home()  / '.env314-ft/bin/python3'
    entry_fp = Path(__file__).resolve()
    records = []

    for fixture_category, fixture_label, fixture, fixture_name in (
            # fixture_to_pair('bool', 'FF_wide_bool'),
            fixture_to_pair('int', 'FF_wide_int'),
            # fixture_to_pair('float', 'FF_wide_float'),

            # fixture_to_pair('bool', 'FF_tall_bool'),
            fixture_to_pair('int', 'FF_tall_int'),
            # fixture_to_pair('float', 'FF_tall_float'),

            # fixture_to_pair('bool', 'FF_square_bool'),
            fixture_to_pair('int', 'FF_square_int'),
            # fixture_to_pair('float', 'FF_square_float'),
            ):


        for py, gil_label in ((py_exe, 'GIL'), (py_exet, 'no-GIL')):
            for cls in CLS_READ:
                # category = f'{fixture_category}-{gil_label}'
                category = gil_label
                record = [cls.__name__, NUMBER, category, fixture_label]
                print(record)


                if subproc:
                    cmd = [str(py), str(entry_fp),  '--cls', cls.__name__, '--fixture', fixture_name]
                    try:
                        proc_result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                        result = float(proc_result.stdout.strip())
                    except subprocess.CalledProcessError as e:
                        print(f'failed: {" ".join(cmd)}\n{e.stderr}', file=sys.stderr)
                        result = np.nan
                    except (ValueError, OSError) as e:
                        print(f'failed: {" ".join(cmd)}: {e!r}', file=sys.stderr)
                        result = np.nan
                else:
                    runner = cls(fixture)
                    try:
                        result = timeit.timeit(
                                f'runner()',
                                globals=locals(),
                                number=NUMBER)
                    except OSError:
                        result = np.nan
                    finally:
                        pass

                record.append(result)
                records.append(record)

    f = sf.FrameGO.from_records(records,
            columns=('name', 'number', 'category', 'fixture', 'time')
            )


    config = sf.DisplayConfig(
            cell_max_width_leftmost=np.inf,
            cell_max_width=np.inf,
            type_show=False,
            display_rows=200,
            include_index=False,
            )
    print(f.display(config))

    plot_performance(f, number=NUMBER)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Run performance tests')
    parser.add_argument('--cls', type=str, help='Test class name to run')
    parser.add_argument('--fixture', type=str, help='Fixture string to use')

    args = parser.parse_args()

    if args.cls and args.fixture:

        if args.cls not in CLS_MAP:
            print(f"Error: Unknown class '{args.cls}'")
            print(f"Available classes: {', '.join(CLS_MAP.keys())}")
            sys.exit(1)

        _, _, fixture, _ = fixture_to_pair('', args.fixture)

        runner = CLS_MAP[args.cls](fixture)
        result = timeit.timeit(
            f'runner()',
            globals=locals(),
            number=NUMBER
        )
        print(result)
    else:
        # Run full test suite
        run_test()




