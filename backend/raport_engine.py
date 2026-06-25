import math
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

APP_VERSION = "2.1.1-web.1"


def cell(ax, x, y, w, h, text="", size=12, bold=True):
    ax.add_patch(Rectangle((x, y), w, h, facecolor="white", edgecolor="black", linewidth=1.1))
    if str(text).strip():
        ax.text(
            x + w / 2,
            y + h / 2,
            str(text),
            ha="center",
            va="center",
            fontsize=size,
            fontweight="bold" if bold else "normal",
            family="DejaVu Sans",
        )


def normalize(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "weather": data.get("weather", "-"),
        "operator": data.get("operator", ""),
        "inspection": data.get("inspection", ""),
        "company": data.get("company", ""),
        "city": data.get("city", ""),
        "street": data.get("street", ""),
        "start_manhole": data.get("start_manhole", ""),
        "end_manhole": data.get("end_manhole", ""),
        "distance": float(data.get("distance", 0)),
        "level_difference": float(data.get("level_difference", 0)),
        "filming_date": data.get("filming_date", ""),
        "diameter": data.get("diameter", ""),
    }


def create_report(data: dict[str, Any], output_path: str | Path) -> dict[str, Any]:
    d = normalize(data)
    distance = d["distance"]
    level_difference = d["level_difference"]

    if distance <= 0:
        raise ValueError("Distance must be greater than 0.")

    x_values = np.arange(0, distance + 0.3, 0.3)
    y_values = x_values * (level_difference / distance)
    x_max = int(math.ceil(distance))

    fig = plt.figure(figsize=(18, 10), facecolor="white")

    header = fig.add_axes([0.055, 0.755, 0.89, 0.205])
    header.set_xlim(0, 1)
    header.set_ylim(0, 1)
    header.axis("off")

    xs = [0, .15, .262, .402, .52, .632, .735, .82, .91, 1]
    ys = [0, .145, .43, .565, .835, 1]

    cell(header, xs[0], ys[0], xs[1] - xs[0], ys[5] - ys[0], "W", 70)
    cell(header, xs[1], ys[4], xs[9] - xs[1], ys[5] - ys[4], "")

    cell(header, xs[1], ys[3], xs[2] - xs[1], ys[4] - ys[3], "Vreme", 14)
    cell(header, xs[2], ys[3], xs[3] - xs[2], ys[4] - ys[3], "Operator", 14)
    cell(header, xs[3], ys[3], xs[4] - xs[3], ys[4] - ys[3], "Inspectie", 14)
    cell(header, xs[4], ys[2], xs[6] - xs[4], ys[4] - ys[2], d["company"], 14)
    cell(header, xs[6], ys[2], xs[9] - xs[6], ys[4] - ys[2], "Edas Exim", 17)

    cell(header, xs[1], ys[2], xs[2] - xs[1], ys[3] - ys[2], d["weather"], 13)
    cell(header, xs[2], ys[2], xs[3] - xs[2], ys[3] - ys[2], d["operator"], 13)
    cell(header, xs[3], ys[2], xs[4] - xs[3], ys[3] - ys[2], d["inspection"], 13)

    labels = ["Localitate", "Strada", "Camin inceput", "Camin sfarsit", "Distanta\ninspectata", "Panta (CM)", "Data filmare", "Diametru"]
    values = [d["city"], d["street"], d["start_manhole"], d["end_manhole"], f"{distance:.2f}", f"{level_difference:g}", d["filming_date"], d["diameter"]]

    for index, label in enumerate(labels, start=1):
        cell(header, xs[index], ys[1], xs[index + 1] - xs[index], ys[2] - ys[1], label, 12)
        cell(header, xs[index], ys[0], xs[index + 1] - xs[index], ys[1] - ys[0], values[index - 1], 13)

    ax = fig.add_axes([0.055, 0.080, 0.89, 0.545])
    ax.plot(x_values, y_values, marker="s", markersize=4, linewidth=2.2, color="#DBA13A")
    ax.set_title(
        f"Tronson {d['start_manhole']} → {d['end_manhole']}\nLungime: {distance:.2f} m, Diferență nivel: {level_difference:g} cm",
        fontsize=15,
        family="DejaVu Sans",
    )
    ax.set_xlabel("Metri parcurși (grid 1m)", fontsize=12)
    ax.set_ylabel("Diferență de nivel (cm)", fontsize=12)
    ax.set_xlim(0, x_max)
    ax.set_ylim(-100, 500)
    ax.set_xticks(np.arange(0, x_max + 1, 1))
    ax.set_yticks(np.arange(-100, 501, 50))
    ax.grid(True, which="major", linestyle=":", linewidth=0.65, color="#999999", alpha=0.75)

    for spine in ax.spines.values():
        spine.set_linewidth(1.1)
        spine.set_color("#333333")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    return {
        "image_path": str(output_path),
        "distance": distance,
        "level_difference": level_difference,
        "start_manhole": d["start_manhole"],
        "end_manhole": d["end_manhole"],
    }
