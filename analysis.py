import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.ticker import MaxNLocator
from scipy.cluster import hierarchy


def go(df):
    for _, df_contest in df.groupby(["contest_id"]):
        fig_corr = plot_corr(df_contest)
        fig_corr.show()
        fig_results, df_results = get_results(df_contest)
        fig_results.show()
        print(df_results)


def plot_corr(df):
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(6, 12))
    title = get_title(df)
    fig.suptitle(title)
    pivot_table = df.pivot_table(
        index=["contest_id", "cvr_id"],
        columns="name",
        aggfunc="size",
        fill_value=0,
    )
    corr = pivot_table.corr()
    plot(corr, axes[0])
    frac = pivot_table.T.dot(pivot_table) / pivot_table.sum()
    plot(frac, axes[1], is_frac=True)
    fig.tight_layout()
    return fig


def get_title(df):
    office_cols = ["level", "jurisdiction", "office", "district"]
    df = df[office_cols].drop_duplicates()
    assert df.shape[0] == 1
    vals = df.iloc[0].to_dict()
    title = "{level} {jurisdiction} {office}".format(**vals)
    if np.isnan(vals["district"]):
        title = "{level} {jurisdiction} {office}".format(**vals)
    else:
        title = "{level} {jurisdiction} {office} {district}".format(**vals)
    return title


def plot(matrix, ax, is_frac=False):
    matrix = cluster_order(matrix)
    size = matrix.shape[0]
    mask = np.triu(np.repeat(True, size))
    limit = np.abs(matrix.values[~mask]).max()
    if is_frac:
        cmap = "Reds"
        vmin = 0
    else:
        cmap = "vlag"
        vmin = -limit
    sns.heatmap(
        matrix,
        square=True,
        cmap=cmap,
        vmin=vmin,
        vmax=limit,
        ax=ax,
        cbar_kws={"shrink": 0.8},
    )
    if is_frac:
        ax.set_title("Overlapping Fraction")
        ax.set_xlabel("total")
        ax.set_ylabel("with")
    else:
        ax.set_title("Mutual Correlation")
        ax.set_xlabel("")
        ax.set_ylabel("")


def cluster_order(df):
    pdist = hierarchy.distance.pdist(df.values)
    linkage = hierarchy.linkage(pdist, method="complete")
    idx = hierarchy.fcluster(linkage, 0.5 * pdist.max(), "distance")
    idx = np.argsort(idx)
    return df.iloc[idx, idx]


def get_results(df):
    vote_for = df["vote_for"].unique()
    assert len(vote_for) == 1
    vote_for = vote_for[0]
    df_votes = df.groupby(["candidate_id", "name"]).size().to_frame("votes")
    df_votes = df_votes.sort_values("votes", ascending=False)
    df_votes["result"] = ""
    df_votes.iloc[:vote_for, df_votes.columns.get_loc("result")] = "winner"

    winners = df_votes[df_votes["result"] == "winner"].index
    winners = winners.get_level_values("candidate_id")

    df_stats = df.copy()
    df_stats["is_winner"] = df_stats["candidate_id"].isin(winners)
    df_stats = df_stats.groupby("cvr_id")["is_winner"]
    df_stats = df_stats.agg(num_marks="count", num_winners="sum")

    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(6, 18))
    sns.histplot(df_stats, x="num_winners", discrete=True, stat="percent", ax=axes[0])
    sns.histplot(df_stats, x="num_marks", discrete=True, stat="percent", ax=axes[1])
    sns.histplot(
        df_stats,
        x="num_marks",
        hue="num_winners",
        multiple="dodge",
        discrete=True,
        stat="percent",
        ax=axes[2],
    )

    axes[0].xaxis.set_major_locator(MaxNLocator(integer=True))
    axes[1].xaxis.set_major_locator(MaxNLocator(integer=True))
    axes[2].xaxis.set_major_locator(MaxNLocator(integer=True))

    fig.tight_layout()

    return fig, df_votes
