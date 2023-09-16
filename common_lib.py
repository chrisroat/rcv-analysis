import time
from pathlib import Path


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


def get_paths(path):
    data = Path("data")
    raw_path = data / "raw" / path
    processed_path = data / "processed" / path
    return raw_path, processed_path


def transform(contest, transformers):
    for regex, transformer in transformers:
        match = regex.match(contest)
        if match:
            return tuple(extract(match, t) for t in transformer)
    raise ValueError(f"No regex found for {contest}")


def extract(match, extractor):
    return match.group(extractor) if isinstance(extractor, int) else extractor


@timer
def write(df_cvr, df_contest, df_office, df_candidate, df_mark, out_path):
    out_path.mkdir(parents=True, exist_ok=True)
    df_cvr.to_parquet(out_path / "cvr.pq")
    df_contest.to_parquet(out_path / "contest.pq")
    df_office.to_parquet(out_path / "office.pq")
    df_candidate.to_parquet(out_path / "candidate.pq")
    df_mark.to_parquet(out_path / "mark.pq")
