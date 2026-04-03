"""
Figures 1-4 for the manuscript.

Styling choices:
  - Serif font to match journal body text
  - 250 DPI for print reproduction
  - Colourblind-friendly palettes where possible
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from config import OUTPUT_DIR, EU_LIMITS, TARGET_METALS


def _style():
    sns.set_style("whitegrid")
    sns.set_context("paper", font_scale=1.15)
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "axes.titleweight": "bold",
        "figure.dpi": 250,
    })


def fig1_boxplots(df):
    """Metal concentration distributions by tissue category."""
    _style()
    sub = df[df["metal"].isin(TARGET_METALS)]

    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    axes = axes.ravel()

    for i, metal in enumerate(TARGET_METALS):
        ax = axes[i]
        d = sub[sub["metal"] == metal]
        sns.boxplot(
            data=d, x="tissue_cat", y="log_conc",
            hue="tissue_cat", palette="Set2",
            width=0.6, fliersize=3, ax=ax, legend=False,
        )
        ax.set_title(metal)
        ax.set_xlabel("")
        ax.set_ylabel("log\u2081\u2080(\u00B5g/g)" if i % 4 == 0 else "")
        ax.tick_params(axis="x", rotation=45, labelsize=7)

    axes[7].set_visible(False)

    fig.suptitle(
        "Figure 1. Heavy metal concentrations by tissue category "
        "(log\u2081\u2080 \u00B5g/g w.w.)",
        fontweight="bold", y=1.01,
    )
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "figure1.png"),
                bbox_inches="tight")
    plt.close(fig)


def fig2_heatmap(df):
    """Mean concentration heatmap: tissue x metal."""
    _style()
    pivot = df.pivot_table(
        values="log_conc", index="tissue",
        columns="metal", aggfunc="mean",
    )

    fig, ax = plt.subplots(figsize=(13, 7))
    sns.heatmap(
        pivot, annot=True, fmt=".2f", cmap="YlOrRd",
        linewidths=0.5, ax=ax,
        cbar_kws={"label": "Mean log\u2081\u2080(\u00B5g/g w.w.)"},
    )
    ax.set_title(
        "Figure 2. Mean heavy metal concentrations by tissue and metal",
        fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "figure2.png"),
                bbox_inches="tight")
    plt.close(fig)


def fig3_species(df):
    """Edible-muscle species comparison with EU limit lines."""
    _style()
    edible = df[df["edible"] == "yes"]
    metals = ["As", "Cd", "Hg", "Pb"]
    sub = edible[edible["metal"].isin(metals)]
    if sub.empty:
        return

    fig, axes = plt.subplots(1, 4, figsize=(16, 5))

    for i, metal in enumerate(metals):
        ax = axes[i]
        d = sub[sub["metal"] == metal]
        sns.barplot(
            data=d, x="species", y="conc",
            hue="species", palette="muted",
            errorbar="sd", capsize=0.1,
            err_kws={"linewidth": 1.2},
            ax=ax, legend=False,
        )
        ax.set_title(metal, fontweight="bold")
        ax.set_xlabel("")
        ax.set_ylabel("\u00B5g/g w.w." if i == 0 else "")
        ax.tick_params(axis="x", rotation=30, labelsize=7)

        if metal in EU_LIMITS:
            ax.axhline(
                EU_LIMITS[metal], color="red", ls="--",
                lw=1.5, alpha=0.7, label="EU limit",
            )
            ax.legend(fontsize=7, loc="upper right")

    fig.suptitle(
        "Figure 3. Toxic metal concentrations in edible muscle "
        "by species",
        fontweight="bold", y=1.04,
    )
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "figure3.png"),
                bbox_inches="tight")
    plt.close(fig)


def fig4_provenance(df):
    """Verification levels and source distribution."""
    _style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    vc = df["verification"].value_counts()
    colours = ["#4CAF50", "#FF9800", "#f44336"]
    ax1.pie(vc, labels=vc.index, autopct="%1.0f%%",
            colors=colours[:len(vc)], startangle=90)
    ax1.set_title("Data verification level", fontweight="bold")

    pc = df["paper_id"].value_counts()
    ax2.barh(range(len(pc)), pc.values, color="#2196F3")
    ax2.set_yticks(range(len(pc)))
    ax2.set_yticklabels(pc.index, fontsize=8)
    ax2.set_xlabel("Data points")
    ax2.set_title("Source studies", fontweight="bold")
    ax2.invert_yaxis()

    fig.suptitle("Figure 4. Dataset provenance",
                 fontweight="bold", y=1.01)
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "figure4.png"),
                bbox_inches="tight")
    plt.close(fig)


def generate_all(df):
    """Render all four manuscript figures."""
    fig1_boxplots(df)
    fig2_heatmap(df)
    fig3_species(df)
    fig4_provenance(df)
    print(f"\n  Figures 1-4 saved to {OUTPUT_DIR}/")
