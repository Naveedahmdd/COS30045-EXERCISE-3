"""Create Exercise 3 charts from the supplied television registration data."""

from pathlib import Path
import textwrap

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data" / "tv_2026_02_15.csv"
OUTPUT = ROOT / "assets" / "img"

NAVY = "#07182d"
YELLOW = "#f5c518"
BLUE = "#277da1"
GREY = "#657383"
LIGHT = "#e8edf2"


def load_data():
    data = pd.read_csv(DATA)
    filtered = data[
        data["SoldIn"].fillna("").str.contains("Australia")
        & data["Availability Status"].eq("Available")
        & data["SubmitStatus"].eq("Approved")
    ].copy()

    numeric_columns = [
        "screensize",
        "Star2",
        "Avg_mode_power",
        "Labelled energy consumption (kWh/year)",
    ]
    for column in numeric_columns:
        filtered[column] = pd.to_numeric(filtered[column], errors="coerce")

    filtered = filtered.dropna(subset=numeric_columns)
    filtered["inches"] = filtered["screensize"] / 2.54
    filtered["rounded_inches"] = filtered["inches"].round().astype(int)
    return data, filtered


def style_axes(axis):
    axis.spines[["top", "right", "left"]].set_visible(False)
    axis.spines["bottom"].set_color("#aeb8c2")
    axis.grid(axis="y", color=LIGHT, linewidth=1, zorder=0)
    axis.tick_params(axis="both", colors=GREY, labelsize=10, length=0)


def save_common_sizes(data):
    counts = data["rounded_inches"].value_counts().head(8).sort_values()
    fig, axis = plt.subplots(figsize=(10, 5.8))
    colors = [YELLOW if size in (55, 65, 75) else BLUE for size in counts.index]
    bars = axis.barh([f'{size}"' for size in counts.index], counts.values, color=colors, zorder=3)
    axis.bar_label(bars, padding=7, color=NAVY, fontsize=10, fontweight="bold")
    axis.set_title("55, 65 and 75 inches dominate the available range", loc="left", color=NAVY, fontsize=18, fontweight="bold", pad=18)
    axis.set_xlabel("Number of available models", color=GREY, labelpad=12)
    axis.set_xlim(0, counts.max() * 1.16)
    style_axes(axis)
    fig.tight_layout()
    fig.savefig(OUTPUT / "common-tv-sizes.png", dpi=180, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def save_size_energy_scatter(data):
    x = data["inches"].to_numpy()
    y = data["Labelled energy consumption (kWh/year)"].to_numpy()
    coefficients = np.polyfit(x, y, 1)
    trend_x = np.linspace(x.min(), x.max(), 100)
    trend_y = np.polyval(coefficients, trend_x)

    fig, axis = plt.subplots(figsize=(10, 6.2))
    axis.scatter(x, y, s=14, color=BLUE, alpha=0.18, edgecolors="none", zorder=2)
    axis.plot(trend_x, trend_y, color=YELLOW, linewidth=3, zorder=4, label="Linear trend")
    axis.set_title("Larger screens generally use more energy", loc="left", color=NAVY, fontsize=18, fontweight="bold", pad=18)
    axis.set_xlabel("Screen size (inches)", color=GREY, labelpad=12)
    axis.set_ylabel("Labelled energy consumption (kWh/year)", color=GREY, labelpad=12)
    axis.set_xlim(10, 120)
    axis.set_ylim(0, 2800)
    axis.legend(frameon=False, loc="upper left")
    style_axes(axis)
    axis.grid(axis="x", color=LIGHT, linewidth=1, zorder=0)
    fig.tight_layout()
    fig.savefig(OUTPUT / "size-vs-energy.png", dpi=180, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def save_star_rating_comparison(data):
    comparable = data[data["inches"].between(54, 56)]
    summary = comparable.groupby("Star2").agg(
        models=("Submit_ID", "size"),
        median_kwh=("Labelled energy consumption (kWh/year)", "median"),
    )
    summary = summary[summary["models"] >= 5]

    fig, axis = plt.subplots(figsize=(10, 5.8))
    labels = [f"{rating:g} ★" for rating in summary.index]
    colors = [YELLOW if rating >= 5 else BLUE for rating in summary.index]
    bars = axis.bar(labels, summary["median_kwh"], color=colors, zorder=3)
    axis.bar_label(bars, labels=[f"{value:.0f}" for value in summary["median_kwh"]], padding=5, color=NAVY, fontsize=9, fontweight="bold")
    axis.set_title("For 55-inch TVs, more stars mean lower typical energy use", loc="left", color=NAVY, fontsize=18, fontweight="bold", pad=18)
    axis.set_xlabel("Energy star rating", color=GREY, labelpad=12)
    axis.set_ylabel("Median labelled consumption (kWh/year)", color=GREY, labelpad=12)
    axis.set_ylim(0, 850)
    style_axes(axis)
    fig.tight_layout()
    fig.savefig(OUTPUT / "star-rating-55-inch.png", dpi=180, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def save_storyboard():
    panels = [
        ("1. Start with the choice", "Show which TV sizes buyers see most often."),
        ("2. Reveal the pattern", "Plot screen size against yearly energy use."),
        ("3. Explain the impact", "Compare typical consumption by size group."),
        ("4. Make comparison fair", "Hold size near 55 inches and compare stars."),
        ("5. State limitations", "Explain registration data and modelling limits."),
        ("6. End with action", "Compare size, kWh/year and stars before buying."),
    ]
    fig, axes = plt.subplots(2, 3, figsize=(13, 7.2))
    fig.patch.set_facecolor("#f7f9fb")
    for number, (axis, (title, text)) in enumerate(zip(axes.flat, panels), start=1):
        axis.set_facecolor("#fff6b8")
        axis.set_xticks([])
        axis.set_yticks([])
        for spine in axis.spines.values():
            spine.set_color("#e6cf40")
            spine.set_linewidth(1.5)
        axis.text(0.08, 0.78, title, transform=axis.transAxes, color=NAVY, fontsize=14, fontweight="bold", va="top")
        wrapped_text = "\n".join(textwrap.wrap(text, width=34))
        axis.text(0.08, 0.57, wrapped_text, transform=axis.transAxes, color="#39485a", fontsize=11, va="top", linespacing=1.45)
        axis.text(0.88, 0.12, f"0{number}", transform=axis.transAxes, color="#b69b00", fontsize=20, fontweight="bold", ha="right")
    fig.suptitle("Exercise 3 website storyboard", x=0.04, ha="left", color=NAVY, fontsize=22, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.92), h_pad=1.5, w_pad=1.5)
    fig.savefig(OUTPUT / "storyboard.png", dpi=160, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)


def write_summary(source, filtered):
    correlation = filtered["screensize"].corr(filtered["Labelled energy consumption (kWh/year)"])
    comparable = filtered[filtered["inches"].between(54, 56)]
    summary = {
        "source_records": len(source),
        "analysed_records": len(filtered),
        "size_energy_correlation": round(correlation, 3),
        "most_common_size_inches": int(filtered["rounded_inches"].value_counts().index[0]),
        "most_common_size_models": int(filtered["rounded_inches"].value_counts().iloc[0]),
        "comparable_55_models": len(comparable),
        "comparable_55_min_kwh": int(comparable["Labelled energy consumption (kWh/year)"].min()),
        "comparable_55_max_kwh": int(comparable["Labelled energy consumption (kWh/year)"].max()),
    }
    pd.Series(summary, name="value").to_csv(ROOT / "analysis" / "analysis-summary.csv", header=True)


if __name__ == "__main__":
    OUTPUT.mkdir(parents=True, exist_ok=True)
    source_data, cleaned_data = load_data()
    save_common_sizes(cleaned_data)
    save_size_energy_scatter(cleaned_data)
    save_star_rating_comparison(cleaned_data)
    save_storyboard()
    write_summary(source_data, cleaned_data)
    print(f"Created four visualisations from {len(cleaned_data):,} analysed records.")
