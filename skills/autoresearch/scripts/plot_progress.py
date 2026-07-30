#!/usr/bin/env python3
"""
Autoresearch Progress Plotter
Renders Karpathy-style autoresearch experiment progress graphs.
"""

import argparse
import json
import os
import sys

def main():
    parser = argparse.ArgumentParser(description="Plot Autoresearch progress graph.")
    parser.add_argument("--log", default="experiment_log.json", help="Path to experiment_log.json")
    parser.add_argument("--out", default="autoresearch_progress.png", help="Output PNG path")
    parser.add_argument("--higher-is-better", action="store_true", help="Set if higher metric value is better")
    args = parser.parse_args()

    if not os.path.exists(args.log):
        print(f"Error: Log file '{args.log}' not found.", file=sys.stderr)
        sys.exit(1)

    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print("Error: matplotlib and numpy are required. Install via pip/uv.", file=sys.stderr)
        sys.exit(1)

    with open(args.log, "r") as f:
        data = json.load(f)

    if not data:
        print("Error: Log file is empty.", file=sys.stderr)
        sys.exit(1)

    exp_nums = [d["exp_num"] for d in data]
    metrics = [d["metric"] for d in data]
    outcomes = [d["outcome"] for d in data]
    hypotheses = [d.get("hypothesis", "") for d in data]

    lower_is_better = not args.higher_is_better

    # Calculate running best
    running_best = []
    current_best = metrics[0]

    for m in metrics:
        if lower_is_better:
            if m < current_best:
                current_best = m
        else:
            if m > current_best:
                current_best = m
        running_best.append(current_best)

    kept_mask = [o == "KEEP" for o in outcomes]
    discard_mask = [o != "KEEP" for o in outcomes]

    fig, ax = plt.subplots(figsize=(14, 7), dpi=300)
    ax.set_facecolor("#fafafa")
    ax.grid(True, color="#e0e0e0", linestyle="-", linewidth=0.5, alpha=0.7)

    # Discarded points (grey)
    if any(discard_mask):
        ax.scatter(
            np.array(exp_nums)[discard_mask],
            np.array(metrics)[discard_mask],
            color="#d0d0d0", alpha=0.6, s=25, label="Discarded", zorder=2
        )

    # Kept points (green)
    if any(kept_mask):
        ax.scatter(
            np.array(exp_nums)[kept_mask],
            np.array(metrics)[kept_mask],
            color="#2ecc71", edgecolor="#1b5e20", linewidth=1.2, s=65, label="Kept", zorder=4
        )

    # Running Best step line
    ax.step(exp_nums, running_best, where="post", color="#27ae60", linewidth=2.0, label="Running best", zorder=3)

    # Annotate kept points
    for i in range(len(data)):
        if outcomes[i] == "KEEP":
            ax.annotate(
                hypotheses[i],
                (exp_nums[i], metrics[i]),
                xytext=(6, 8),
                textcoords="offset points",
                fontsize=8,
                color="#1b5e20",
                rotation=20,
                alpha=0.9
            )

    total_exps = len(data)
    total_kept = sum(kept_mask)
    direction_str = "lower is better" if lower_is_better else "higher is better"
    metric_label = f"Metric ({direction_str})"

    ax.set_title(f"Autoresearch Progress: {total_exps} Experiments, {total_kept} Kept Improvements", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Experiment #", fontsize=11, fontweight="bold")
    ax.set_ylabel(metric_label, fontsize=11, fontweight="bold")
    ax.legend(loc="upper right", frameon=True, facecolor="white", framealpha=0.9)

    plt.tight_layout()
    plt.savefig(args.out, dpi=300)
    plt.close()
    print(f"Saved progress plot to {args.out}")

if __name__ == "__main__":
    main()
