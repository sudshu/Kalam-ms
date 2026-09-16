#!/usr/bin/env python3
"""Generate the demo manuscript's figures.

Everything plotted here is SYNTHETIC. The numbers are invented to exercise Kalam's
figure and review skills; they are not a scientific result and must not be cited.

The point of this script is to show the shape a Kalam figure script takes:
self-contained, deterministic (fixed seed), vector-PDF output written straight into
`figures/main/` and `figures/si/`, one function per display item, and every reported
statistic taken from `RESULTS` rather than re-derived from a random draw -- so the
figure can never drift away from the numbers in the text.

Usage:
    python figures/make_demo_figures.py          # from the manuscript directory
Requires: matplotlib, numpy.
"""
from __future__ import annotations

import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
MAIN = HERE / "main"
SI = HERE / "si"
RNG = np.random.default_rng(20260902)

# --- house style: readable at print size, vector output, no chartjunk -------------
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 9,
    "axes.labelsize": 10,
    "axes.titlesize": 10,
    "axes.titlelocation": "left",
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 200,
    "savefig.bbox": "tight",
    "pdf.fonttype": 42,          # embed as TrueType so text stays selectable
})

# Single source of truth for every number the figures display. These must match
# drafts/main_text.md; /km-deep-read checks figure-text agreement.
RESULTS = {
    "sites": ["Wet", "Moist", "Seasonal", "Dry"],
    "site_median_d20": [4.2, 2.7, 1.1, 0.3],     # Mg C ha-1
    "pooled_median_d20": 1.9,
    "pooled_ci_d20": (-0.6, 5.4),
    "placebo_median": 0.05,
    "placebo_ci": (-0.7, 0.8),
    "fraction_positive": 0.73,
    "attribution": {"Lower cumulative NPP": 68, "Extra respiration": 27,
                    "Turnover interactions": 5},
    "threshold_percentiles": [85, 90, 95],
    "threshold_medians": [1.6, 1.9, 2.1],
    "numerical_tests": {"Optimizer seed": 0.04, "Monthly vs daily forcing": 0.06},
}

C_EXTREME = "#B4451F"
C_COUNTER = "#2E6F9E"
C_NEUTRAL = "#8A8A8A"
C_MID = "#D69A6A"

#: Spread of the per-site parameter ensembles. Chosen so the pooled fraction with
#: positive D20 reproduces RESULTS["fraction_positive"]; see _check_spread().
SITE_SPREAD = 2.9


def _site_ensembles():
    """200 parameter sets per site, drawn around the reported site medians."""
    return {s: RNG.normal(m, SITE_SPREAD, 200)
            for s, m in zip(RESULTS["sites"], RESULTS["site_median_d20"])}


def _interval(ax, x, median, ci, color, label):
    """A median dot with a 95% interval whisker, labelled above.

    ``label`` is passed in rather than formatted from ``median`` so the printed
    precision matches the text exactly, with no invented trailing digit.
    """
    ax.plot([x, x], ci, color=color, lw=1.4, solid_capstyle="round")
    ax.scatter([x], [median], color=color, s=28, zorder=3)
    ax.text(x, ci[1] + 0.3, label, ha="center", fontsize=8, color=color)


def figure1():
    """Design and trajectories: what the paired experiment does to one site."""
    fig, axes = plt.subplots(1, 3, figsize=(7.6, 2.4), layout="constrained")
    yrs = np.linspace(0, 20, 241)

    # (a) which months the counterfactual replaces
    ax = axes[0]
    extreme_months = np.sort(RNG.choice(240, 26, replace=False))
    ax.vlines(extreme_months / 12, 0, 1, color=C_EXTREME, lw=0.9)
    ax.set(xlim=(0, 20), ylim=(0, 1), yticks=[], xlabel="Year",
           title="a  Hot-dry months")
    ax.spines["left"].set_visible(False)

    # (b) ecosystem carbon in the paired runs
    ax = axes[1]
    base = 148 + 2.1 * (1 - np.exp(-yrs / 9))
    debt = RESULTS["site_median_d20"][0] * (1 - np.exp(-yrs / 6.5))
    ax.plot(yrs, base, color=C_COUNTER, lw=1.6, label="No-extremes counterfactual")
    ax.plot(yrs, base - debt, color=C_EXTREME, lw=1.6, label="Repeated extremes")
    ax.annotate("", xy=(20.2, base[-1]), xytext=(20.2, base[-1] - debt[-1]),
                arrowprops=dict(arrowstyle="<->", lw=0.8, color="k",
                                shrinkA=0, shrinkB=0))
    ax.text(21.0, base[-1] - debt[-1] / 2, r"$D_{20}$", ha="left", va="center")
    ax.set(xlim=(0, 23), xticks=[0, 5, 10, 15, 20],
           xlabel="Year", ylabel=r"Ecosystem C (Mg C ha$^{-1}$)",
           title="b  Wet site")
    ax.legend(frameon=False, loc="lower left")

    # (c) flux recovery after a single event
    ax = axes[2]
    months = np.arange(-6, 25)
    nbp = np.where(months < 0, 0.0, -0.42 * np.exp(-months / 5.5))
    ax.axhspan(-0.08, 0.08, color=C_NEUTRAL, alpha=0.25, lw=0)
    ax.axvline(0, color="k", lw=0.6, ls=":")
    ax.plot(months, nbp, color=C_EXTREME, lw=1.6)
    ax.text(23, 0.045, "baseline IQR", color="#555555", fontsize=8, ha="right")
    ax.set(xlabel="Months since event", ylim=(-0.5, 0.16),
           ylabel=r"NBP anomaly (Mg C ha$^{-1}$ mo$^{-1}$)",
           title="c  Flux recovery")

    fig.savefig(MAIN / "figure1_design_and_trajectories.pdf")
    plt.close(fig)


def figure2():
    """The result: per-site debt, the placebo test, and where the carbon went."""
    ens = _site_ensembles()
    fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.7), layout="constrained",
                             width_ratios=[1.3, 0.8, 1.0])

    # (a) per-site ensembles, reported medians marked
    ax = axes[0]
    parts = ax.violinplot([ens[s] for s in RESULTS["sites"]],
                          showextrema=False, widths=0.85)
    for body in parts["bodies"]:
        body.set(facecolor=C_EXTREME, alpha=0.35, edgecolor="none")
    ax.scatter(range(1, 5), RESULTS["site_median_d20"], color=C_EXTREME, s=20, zorder=3)
    for i, m in enumerate(RESULTS["site_median_d20"], start=1):
        ax.text(i + 0.12, m, f"{m:.1f}", fontsize=8, color=C_EXTREME, va="center")
    ax.axhline(0, color="k", lw=0.6)
    ax.set(xticks=range(1, 5), xticklabels=RESULTS["sites"], ylim=(-8, 13),
           ylabel=r"$D_{20}$ (Mg C ha$^{-1}$)", title="a  Carbon debt by site")

    # (b) reported pooled result against the neutral-splice placebo
    ax = axes[1]
    _interval(ax, 0, RESULTS["pooled_median_d20"], RESULTS["pooled_ci_d20"],
              C_EXTREME, "1.9")
    _interval(ax, 1, RESULTS["placebo_median"], RESULTS["placebo_ci"],
              C_NEUTRAL, "0.05")
    ax.axhline(0, color="k", lw=0.6)
    ax.set(xlim=(-0.7, 1.7), ylim=(-2, 7), xticks=[0, 1],
           xticklabels=["Extremes", "Placebo"],
           ylabel=r"Pooled $D_{20}$ (Mg C ha$^{-1}$)", title="b  Placebo test")

    # (c) process attribution of the pooled median debt
    ax = axes[2]
    bottom = 0.0
    for (lab, share), col in zip(RESULTS["attribution"].items(),
                                 [C_EXTREME, C_MID, C_NEUTRAL]):
        ax.bar(0, share, bottom=bottom, width=0.5, color=col, edgecolor="white", lw=0.8)
        ax.text(0.32, bottom + share / 2, f"{lab}\n{share}%", va="center", fontsize=8)
        bottom += share
    ax.set(xlim=(-0.35, 1.9), ylim=(0, 100), xticks=[],
           ylabel="Share of pooled median debt (%)", title="c  Attribution")

    fig.savefig(MAIN / "figure2_carbon_debt.pdf")
    plt.close(fig)


def figure_s1():
    """Robustness: sensitivity to the choices that define the result."""
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.5), layout="constrained")

    ax = axes[0]
    ax.plot(RESULTS["threshold_percentiles"], RESULTS["threshold_medians"],
            "o-", color=C_EXTREME, lw=1.4, ms=5)
    for p, m in zip(RESULTS["threshold_percentiles"], RESULTS["threshold_medians"]):
        ax.text(p, m + 0.12, f"{m:.1f}", ha="center", fontsize=8, color=C_EXTREME)
    ax.set(xticks=RESULTS["threshold_percentiles"], xlim=(83, 97), ylim=(0, 2.8),
           xlabel="Extreme-definition percentile",
           ylabel=r"Pooled median $D_{20}$ (Mg C ha$^{-1}$)",
           title="a  Threshold sensitivity")

    ax = axes[1]
    labels = list(RESULTS["numerical_tests"])
    values = [RESULTS["numerical_tests"][k] for k in labels]
    ypos = np.arange(len(labels))
    ax.barh(ypos, values, color=C_NEUTRAL, height=0.45)
    for y, v in zip(ypos, values):
        ax.text(v + 0.012, y, f"{v:.2f}", va="center", fontsize=8)
    ax.set(yticks=ypos, yticklabels=labels, xlim=(0, 0.3),
           xlabel=r"Change in pooled median $D_{20}$" "\n" r"(Mg C ha$^{-1}$)",
           title="b  Numerical robustness")

    fig.savefig(SI / "figureS1_robustness.pdf")
    plt.close(fig)


def _check_spread():
    """Warn if SITE_SPREAD stops reproducing the reported positive fraction."""
    ens = np.concatenate(list(_site_ensembles().values()))
    frac = float((ens > 0).mean())
    target = RESULTS["fraction_positive"]
    if abs(frac - target) > 0.03:
        print(f"  warning: ensembles give {frac:.0%} positive D20, text says "
              f"{target:.0%} -- retune SITE_SPREAD")
    else:
        print(f"  ensembles give {frac:.0%} positive D20 (text: {target:.0%})")


if __name__ == "__main__":
    MAIN.mkdir(parents=True, exist_ok=True)
    SI.mkdir(parents=True, exist_ok=True)
    figure1()
    figure2()
    figure_s1()
    _check_spread()
    for f in sorted(MAIN.glob("*.pdf")) + sorted(SI.glob("*.pdf")):
        print(f"wrote {f.relative_to(HERE.parent)}  ({f.stat().st_size / 1024:.0f} kB)")
