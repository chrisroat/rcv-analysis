import numpy as np
from scipy.cluster import hierarchy


def corr_matrix(df, symmetric):
    pivot_table = df.pivot_table(
        index="cvr_id", columns="Candidate", aggfunc="size", fill_value=0
    )

    if symmetric:
        corr = pivot_table.corr()
    else:
        corr = pivot_table.T.dot(pivot_table) / pivot_table.sum()

    pdist = hierarchy.distance.pdist(corr.values)
    linkage = hierarchy.linkage(pdist, method="complete")
    idx = hierarchy.fcluster(linkage, 0.5 * pdist.max(), "distance")
    idx = np.argsort(idx)
    corr = corr.iloc[idx, idx]
    corr.attrs.update(df.attrs)
    return corr


def election_results(df):
    vote_for = df["vote_for"].unique()
    assert len(vote_for) == 1
    vote_for = vote_for[0]
    df_votes = df.groupby(["candidate_id", "Candidate"]).size().to_frame("Votes")
    df_votes = df_votes.sort_values("Votes", ascending=False)
    df_votes["Result"] = "Eliminated"
    df_votes.iloc[:vote_for, df_votes.columns.get_loc("Result")] = "Winner"
    df_votes.attrs.update(df.attrs)
    return df_votes


def ballot_stats(df):
    df_votes = election_results(df)
    winners = df_votes[df_votes["Result"] == "Winner"]
    winners = winners.index.get_level_values("candidate_id")

    df_ballots = df.copy()
    is_winner = df_ballots.index.get_level_values("candidate_id").isin(winners)
    df_ballots["is_winner"] = is_winner
    df_ballots = df_ballots.groupby("cvr_id")["is_winner"]
    df_ballots = df_ballots.agg(num_votes="count", num_winners="sum")
    df_ballots.attrs.update(df.attrs)
    return df_ballots


def ballot_combos(df):
    matrix = corr_matrix(df, symmetric=True)
    names = matrix.index.tolist()
    df_comb = df.pivot_table(
        columns="Candidate", index="cvr_id", aggfunc="size", fill_value=0
    )
    df_comb = df_comb.groupby(names).size()
    df_comb = df_comb.reset_index(name="Votes").sort_values("Votes", ascending=False)
    df_comb.attrs.update(df.attrs)
    return df_comb
