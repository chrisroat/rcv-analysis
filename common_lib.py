import functools
import time
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

DATA_ITEMS = ["cvr", "contest", "office", "candidate", "mark"]
PIL_KWARGS = {"optimize": True}


def timer(func):
    # This function shows the execution time of
    # the function object passed
    @functools.wraps(func)
    def wrap_func(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        print(f"{func.__name__}: {(t2-t1):.1f}s")
        return result

    return wrap_func


def transform(contest, transformers):
    for regex, transformer in transformers:
        match = regex.match(contest)
        if match:
            return tuple(extract(match, t) for t in transformer)
    raise ValueError(f"No regex found for {contest}")


def extract(match, extractor):
    return match.group(extractor) if isinstance(extractor, int) else extractor


@timer
def read_proc_contest(path, title, contest_query=None, mark_query=None):
    data_proc = read_proc(path)

    df_contest = data_proc["contest"]
    df_office = data_proc["office"]
    df = df_contest.join(df_office)
    if contest_query:
        df = df.query(contest_query)

    assert (
        len(df.index.get_level_values("contest_id").unique()) == 1
    ), f"query specified multiple contest: {contest_query}"

    df_mark = data_proc["mark"]
    if mark_query:
        df_mark = df_mark.query(mark_query)

    df_candidate = data_proc["candidate"][["Candidate", "Party"]]

    df = df.join(df_mark).join(df_candidate)
    df.attrs["name"] = "single_contest_full_data"
    df.attrs["path"] = str(path)
    df.attrs["title"] = title
    return df


def read_proc(path):
    path_proc = Path("data") / "processed" / path
    result = {}
    for item in DATA_ITEMS:
        df = pd.read_parquet(path_proc / f"{item}.pq")
        df.attrs["name"] = item
        df.attrs["path"] = str(path)
        result[item] = df
    return result


@timer
def write_proc(path, data_proc):
    path_proc = Path("data") / "processed" / path
    path_proc.mkdir(parents=True, exist_ok=True)
    for item in DATA_ITEMS:
        data_proc[item].to_parquet(path_proc / f"{item}.pq")


@timer
def write_figs(path, contest_path, figs):
    path_figs = Path("data") / "figures" / path / contest_path
    path_figs.mkdir(parents=True, exist_ok=True)
    for name, fig in figs.items():
        fig.savefig(path_figs / f"{name}.png", pil_kwargs=PIL_KWARGS)
        plt.close(fig)


def create_title(row):
    title = f"{row.level}:{row.jurisdiction}:{row.office}"
    if type(row.district) is str:
        title += f":{row.district}"
    return title
