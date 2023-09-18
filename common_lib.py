import time
from pathlib import Path

import pandas as pd

DATA_ITEMS = ["cvr", "contest", "office", "candidate", "mark"]


def timer(func):
    # This function shows the execution time of
    # the function object passed
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
def read_proc(path):
    path_proc = Path("data") / "processed" / path
    return {item: pd.read_parquet(path_proc / f"{item}.pq") for item in DATA_ITEMS}


@timer
def write_proc(data_proc, path):
    path_proc = Path("data") / "processed" / path
    path_proc.mkdir(parents=True, exist_ok=True)
    for item in DATA_ITEMS:
        data_proc[item].to_parquet(path_proc / f"{item}.pq")


def create_title(row):
    title = f"{row.level}:{row.jurisdiction}:{row.office}"
    if type(row.district) is str:
        title += f":{row.district}"
    return title
