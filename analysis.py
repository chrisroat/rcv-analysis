import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.colors import ListedColormap
from matplotlib.ticker import MaxNLocator
from scipy.cluster import hierarchy


def go(df):
    for _, df_contest in df.groupby(["contest_id"]):
        names_ordered = plot_corr(df_contest)
        plot_results(df_contest)
        plot_combos(df_contest, names_ordered)


def plot_corr(df):
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(6, 12))
    title = "NEW TITLE NEEDED"
    fig.suptitle(title)
    pivot_table = df.pivot_table(
        index=["contest_id", "cvr_id"],
        columns="name",
        aggfunc="size",
        fill_value=0,
    )
    corr = pivot_table.corr()
    corr_names = plot(corr, axes[0], symmetric=True)
    frac = pivot_table.T.dot(pivot_table) / pivot_table.sum()
    plot(frac, axes[1], symmetric=False)
    fig.tight_layout()

    return corr_names


def plot(matrix, ax, symmetric):
    matrix = cluster_order(matrix)
    size = matrix.shape[0]
    mask = np.triu(np.repeat(True, size))
    limit = np.abs(matrix.values[~mask]).max()
    cmap = matplotlib.cm.get_cmap("vlag")
    if symmetric:
        vmin = -limit
    else:
        mid = len(cmap.colors) // 2
        cmap = ListedColormap(cmap.colors[mid:])
        vmin = 0
    sns.heatmap(
        matrix,
        square=True,
        cmap=cmap,
        vmin=vmin,
        vmax=limit,
        ax=ax,
        cbar_kws={"shrink": 0.8},
    )
    if symmetric:
        ax.set_title("Mutual Correlation")
        ax.set_xlabel("")
        ax.set_ylabel("")
    else:
        ax.set_title("Overlapping Fraction")
        ax.set_xlabel("total")
        ax.set_ylabel("with")
    return matrix.index.tolist()


def cluster_order(df):
    pdist = hierarchy.distance.pdist(df.values)
    linkage = hierarchy.linkage(pdist, method="complete")
    idx = hierarchy.fcluster(linkage, 0.5 * pdist.max(), "distance")
    idx = np.argsort(idx)
    return df.iloc[idx, idx]


def plot_results(df):
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

    fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(6, 24))
    sns.histplot(
        df_votes, x="name", weights="votes", hue="result", stat="percent", ax=axes[0]
    )
    axes[0].tick_params(axis="x", rotation=90)
    sns.histplot(df_stats, x="num_winners", discrete=True, stat="percent", ax=axes[1])
    sns.histplot(df_stats, x="num_marks", discrete=True, stat="percent", ax=axes[2])
    sns.histplot(
        df_stats,
        x="num_marks",
        hue="num_winners",
        multiple="dodge",
        discrete=True,
        stat="percent",
        ax=axes[3],
    )

    axes[1].xaxis.set_major_locator(MaxNLocator(integer=True))
    axes[2].xaxis.set_major_locator(MaxNLocator(integer=True))
    axes[3].xaxis.set_major_locator(MaxNLocator(integer=True))

    fig.tight_layout()


def plot_combos(df, names):
    df_comb = df.pivot_table(
        columns="name", index="cvr_id", aggfunc="size", fill_value=0
    )
    df_comb = df_comb.groupby(names).size()
    df_comb = df_comb.reset_index(name="Count").sort_values("Count", ascending=False)

    yticks = []
    ytick_labels = []
    borders = [0]
    data = []
    prev = 0
    for i in range(df_comb.shape[0]):
        values = df_comb.iloc[i].tolist()
        *values, count = values
        yticks.append(prev + count // 2)
        ytick_labels.append(count)
        borders.append(borders[-1] + count)
        prev += count
        data.extend([values] * count)

    fig, ax = plt.subplots(figsize=(8, 20))
    ax = sns.heatmap(data, cmap="Blues", ax=ax, cbar=False, xticklabels=names)
    ax.xaxis.tick_top()
    ax.set_ylabel("Ballot Count for Combination")
    plt.xticks(rotation=90)
    plt.yticks(ticks=yticks, labels=ytick_labels, fontsize=6)

    for border in borders:
        ax.axhline(border, color="white", lw=0.2)

    for x in range(len(names)):
        ax.axvline(x, color="white", lw=2)
    fig.tight_layout()
