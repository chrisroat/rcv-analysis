import warnings

from analysis_lib import *
from common_lib import read_proc_contest, write_figs
from plotting import *


def make_all_figs(df, stat="count", corr_hide_upper_half=False):
    figs = {}

    matrix_sym = corr_matrix(df, symmetric=True)
    figs["corr"] = plot_corr(
        matrix_sym, symmetric=True, hide_upper_half=corr_hide_upper_half
    )

    matrix_asym = corr_matrix(df, symmetric=False)
    figs["frac"] = plot_corr(matrix_asym, symmetric=False)

    df_votes = election_results(df)
    figs["votes"] = plot_votes(df_votes, stat)

    df_ballots = ballot_stats(df)
    figs["num_winners"] = plot_ballot_num_winners(df_ballots, stat)

    df_ballots = ballot_stats(df)
    figs["num_votes"] = plot_ballot_num_votes(df_ballots, stat)

    df_ballots = ballot_stats(df)
    figs["num_votes_winners"] = plot_ballot_votes_and_winners(df_ballots, stat)

    df_combos = ballot_combos(df)
    figs["combos"] = plot_combos(df_combos)

    return figs


if __name__ == "__main__":
    warnings.simplefilter(action="ignore", category=FutureWarning)

    sf_mark_query = "is_vote & ~is_ambiguous"
    data = [
        (
            "2020/ca/county/santa_clara/general",
            "2020 Mountain View City Council",
            {
                "contest_query": "(jurisdiction == 'Mountain View') & (office == 'Council')",
            },
            "city/mountain_view/council",
        ),
        (
            "2022/ca/county/santa_clara/general",
            "2022 Mountain View City Council",
            {
                "contest_query": "(jurisdiction == 'Mountain View') & (office == 'Council')",
            },
            "city/mountain_view/council",
        ),
        (
            "2020/ca/county/santa_clara/general",
            "2020 Los Altos City Council",
            {
                "contest_query": "(jurisdiction == 'Los Altos') & (office == 'Council')",
            },
            "city/los_altos/council",
        ),
        (
            "2022/ca/county/santa_clara/general",
            "2022 Los Altos City Council",
            {
                "contest_query": "(jurisdiction == 'Los Altos') & (office == 'Council')",
            },
            "city/los_altos/council",
        ),
        (
            "2020/ca/city/san_francisco/general",
            "2020 SF School Board",
            {
                "contest_query": "contest_id == 8",
                "mark_query": sf_mark_query,
            },
            "school_district/san_francisco/board",
        ),
        (
            "2020/ca/city/san_francisco/general",
            "2020 SF Community College District",
            {
                "contest_query": "contest_id == 9",
                "mark_query": sf_mark_query,
            },
            "community_college_district/san_francisco/board",
        ),
    ]

    for path, title, kwargs, contest_path in data:
        print(title)
        df = read_proc_contest(path, title, **kwargs)
        figs = make_all_figs(df)
        write_figs(path, contest_path, figs)
