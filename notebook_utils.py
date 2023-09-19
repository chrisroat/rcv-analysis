from analysis import *
from plotting import *


def make_all_plots(df, stat="count"):
    matrix_sym = corr_matrix(df, symmetric=True)
    plot_corr(matrix_sym, symmetric=True)

    matrix_asym = corr_matrix(df, symmetric=False)
    plot_corr(matrix_asym, symmetric=False)

    df_votes = election_results(df)
    plot_votes(df_votes, stat)

    df_ballots = ballot_stats(df)
    plot_ballot_num_winners(df_ballots, stat)

    df_ballots = ballot_stats(df)
    plot_ballot_num_votes(df_ballots, stat)

    df_ballots = ballot_stats(df)
    plot_ballot_votes_and_winners(df_ballots, stat)

    df_combos = ballot_combos(df)
    plot_combos(df_combos)
