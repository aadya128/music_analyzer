# visualization/plotter.py
# Stage 9 — Draw energy curve graphs using matplotlib

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd


def plot_energy_curves(df, color_identity, save_path="energy_curves.png"):
    """
    Creates 3 graphs showing how your music energy
    changes across different time periods.
    """

    color_map = {
        "Red"   : "#E74C3C",
        "Yellow": "#F1C40F",
        "Green" : "#2ECC71",
        "Blue"  : "#3498DB"
    }
    bar_color = color_map.get(color_identity, "#9B59B6")

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle(
        "Your Listening Energy Curve",
        fontsize=16,
        fontweight="bold",
        y=1.02
    )

    # ── Graph 1: Energy vs Hour ──────────────────────
    hourly = df.groupby("hour")["energy"].mean().reset_index()

    axes[0].bar(
        hourly["hour"],
        hourly["energy"],
        color=bar_color,
        alpha=0.85,
        edgecolor="white",
        linewidth=0.5
    )
    axes[0].set_title("Energy by Hour of Day", fontweight="bold")
    axes[0].set_xlabel("Hour (IST)")
    axes[0].set_ylabel("Average Energy")
    axes[0].set_ylim(0, 1)
    axes[0].set_xticks(range(0, 24, 2))
    axes[0].axhline(y=0.5, color="gray", linestyle="--", alpha=0.5, linewidth=1)
    axes[0].grid(axis="y", alpha=0.3)

    # ── Graph 2: Energy vs Day of Week ───────────────
    day_order  = ["Monday", "Tuesday", "Wednesday", "Thursday",
                  "Friday", "Saturday", "Sunday"]
    daily      = df.groupby("weekday")["energy"].mean().reindex(day_order).dropna()
    short_days = [d[:3] for d in daily.index]

    axes[1].bar(
        short_days,
        daily.values,
        color=bar_color,
        alpha=0.85,
        edgecolor="white",
        linewidth=0.5
    )
    axes[1].set_title("Energy by Day of Week", fontweight="bold")
    axes[1].set_xlabel("Day")
    axes[1].set_ylabel("Average Energy")
    axes[1].set_ylim(0, 1)
    axes[1].axhline(y=0.5, color="gray", linestyle="--", alpha=0.5, linewidth=1)
    axes[1].grid(axis="y", alpha=0.3)

    # ── Graph 3: Energy vs Month ──────────────────────
    month_order  = ["January", "February", "March", "April",
                    "May", "June", "July", "August",
                    "September", "October", "November", "December"]
    monthly      = df.groupby("month")["energy"].mean().reindex(month_order).dropna()
    short_months = [m[:3] for m in monthly.index]

    axes[2].bar(
        short_months,
        monthly.values,
        color=bar_color,
        alpha=0.85,
        edgecolor="white",
        linewidth=0.5
    )
    axes[2].set_title("Energy by Month", fontweight="bold")
    axes[2].set_xlabel("Month")
    axes[2].set_ylabel("Average Energy")
    axes[2].set_ylim(0, 1)
    axes[2].axhline(y=0.5, color="gray", linestyle="--", alpha=0.5, linewidth=1)
    axes[2].grid(axis="y", alpha=0.3)

    # ── Final Touches ─────────────────────────────────
    plt.tight_layout()

    threshold_line = mpatches.Patch(
        color="gray",
        label="0.5 threshold (above = high energy)"
    )
    fig.legend(
        handles=[threshold_line],
        loc="lower center",
        ncol=1,
        bbox_to_anchor=(0.5, -0.08)
    )

    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    print(f"\n Graph saved to {save_path}")
    plt.close()