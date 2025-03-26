import functools

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.colors import ListedColormap
from matplotlib.ticker import MaxNLocator

plt.rcParams.update({"figure.max_open_warning": 0})

NUM_VOTES = "# candidates selected"
NUM_WINNERS = "# winning candidates selected"


def fig_with_title(_func=None, *, figsize=(6, 6), ytitle=None):
    def decorator_fig(func):
        """Create a figure with the contest name as title."""

        @functools.wraps(func)
        def wrap_func(*args, **kwargs):
            fig = plt.figure(figsize=figsize)
            title = args[0].attrs["title"]
            fig.suptitle(title, y=ytitle)
            value = func(*args, **kwargs)
            assert value is None, f"{func.__name__} should not return a value"
            fig.tight_layout()
            return fig

        return wrap_func

    return decorator_fig if _func is None else decorator_fig(_func)


@fig_with_title
def plot_corr(matrix, symmetric, hide_upper_half=False):
    if not symmetric and hide_upper_half:
        raise ValueError("Cannot hide upper half of non-symmetric correlation matrix.")
    size = matrix.shape[0]
    mask = np.eye(size, dtype=np.bool_)
    limit = np.abs(matrix.values[~mask]).max()
    cmap = matplotlib.colormaps["vlag"]

    if symmetric:
        vmin = -limit
        if hide_upper_half:
            idx = np.triu_indices_from(matrix)
            matrix.values[idx] = 0
    else:
        vmin = 0
        mid = len(cmap.colors) // 2
        cmap = ListedColormap(cmap.colors[mid:])

    ax = sns.heatmap(
        matrix,
        square=True,
        cmap=cmap,
        vmin=vmin,
        vmax=limit,
        cbar_kws={"shrink": 0.8},
    )

    if symmetric:
        ax.set(xlabel="", ylabel="", title="Mutual Correlation")
    else:
        ax.set(
            xlabel="Ballot that voted for",
            ylabel="also voted for",
            title="Overlapping Fraction",
        )


@fig_with_title
def plot_votes(df_votes, stat="count"):
    ax = sns.histplot(df_votes, x="Candidate", weights="Votes", hue="Result", stat=stat)
    ax.tick_params(axis="x", rotation=90)
    ax.set(ylabel="# Votes", title="Vote Count")


@fig_with_title
def plot_ballot_num_winners(df_ballots, stat="count"):
    ax = sns.histplot(df_ballots, x="num_winners", discrete=True, stat=stat)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set(xlabel=NUM_WINNERS, ylabel="# Ballots")


@fig_with_title
def plot_ballot_num_votes(df_ballots, stat="count"):
    ax = sns.histplot(df_ballots, x="num_votes", discrete=True, stat=stat)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set(xlabel=NUM_VOTES, ylabel="# Ballots")


@fig_with_title
def plot_ballot_votes_and_winners(df_ballots, stat="count"):
    ax = sns.histplot(
        df_ballots,
        x="num_votes",
        hue="num_winners",
        multiple="dodge",
        discrete=True,
        stat=stat,
    )
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set(xlabel=NUM_VOTES, ylabel="# Ballots")
    ax.get_legend().set_title(NUM_WINNERS)


@fig_with_title(figsize=(8, 20), ytitle=1.02)
def plot_combos(df_comb):
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

    names = df_comb.columns[:-1]

    ax = sns.heatmap(data, cmap="Blues", cbar=False, xticklabels=names)
    ax.xaxis.tick_top()
    ax.xaxis.set_ticks_position("top")
    ax.xaxis.set_label_position("top")
    ax.set_xlabel("Candidate")
    ax.set_ylabel("Ballot Count for Combination")
    ax.set_title("Ballot Selections")
    plt.xticks(rotation=90)
    plt.yticks(ticks=yticks, labels=ytick_labels, fontsize=6)

    for border in borders:
        ax.axhline(border, color="white", lw=0.2)

    for x in range(len(names)):
        ax.axvline(x, color="white", lw=2)
