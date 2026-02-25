"""
chart_generator.py — Renders a Matplotlib chart and returns it as a base64 string.
"""

import io
import base64

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend — safe for servers
import matplotlib.pyplot as plt
import pandas as pd


def generate_chart(df: pd.DataFrame, chart_decision: dict) -> str:
    """
    Generate a chart image from the cleaned DataFrame using Matplotlib.

    Supported chart types: line, bar, scatter, pie.

    Args:
        df            : Cleaned Pandas DataFrame.
        chart_decision: Dict returned by openai_service with keys
                        chart_type, x_axis, y_axis, group_by.

    Returns:
        Base64-encoded PNG image string (UTF-8, no data-URI prefix).
    """
    chart_type = chart_decision.get("chart_type", "bar").lower()
    x_col = chart_decision.get("x_axis")
    y_col = chart_decision.get("y_axis")
    group_col = chart_decision.get("group_by")

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#1e1e2e")
    ax.set_facecolor("#1e1e2e")
    ax.tick_params(colors="#cdd6f4")
    ax.title.set_color("#cdd6f4")
    ax.xaxis.label.set_color("#cdd6f4")
    ax.yaxis.label.set_color("#cdd6f4")
    for spine in ax.spines.values():
        spine.set_edgecolor("#45475a")

    palette = ["#89b4fa", "#a6e3a1", "#fab387", "#f38ba8", "#cba6f7"]

    try:
        if chart_type == "line":
            if group_col and group_col in df.columns:
                for i, (name, group) in enumerate(df.groupby(group_col)):
                    ax.plot(group[x_col], group[y_col], label=str(name),
                            color=palette[i % len(palette)])
                ax.legend(facecolor="#313244", labelcolor="#cdd6f4")
            else:
                ax.plot(df[x_col], df[y_col], color=palette[0])

        elif chart_type == "bar":
            if group_col and group_col in df.columns:
                pivot = df.pivot_table(index=x_col, columns=group_col,
                                       values=y_col, aggfunc="sum")
                pivot.plot(kind="bar", ax=ax, color=palette)
                ax.legend(facecolor="#313244", labelcolor="#cdd6f4")
            else:
                ax.bar(df[x_col], df[y_col], color=palette[0])

        elif chart_type == "scatter":
            ax.scatter(df[x_col], df[y_col], color=palette[0], alpha=0.7)

        elif chart_type == "pie":
            values = df[y_col]
            labels = df[x_col]
            ax.pie(values, labels=labels, autopct="%1.1f%%",
                   colors=palette, textprops={"color": "#cdd6f4"})

        else:
            # Fallback: bar chart
            ax.bar(df[x_col], df[y_col], color=palette[0])

        ax.set_title(f"{chart_type.capitalize()} Chart — {y_col} vs {x_col}")
        ax.set_xlabel(x_col)
        if chart_type != "pie":
            ax.set_ylabel(y_col)

        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

    except Exception as exc:
        # If rendering fails, produce an error chart
        ax.text(0.5, 0.5, f"Chart error:\n{exc}", transform=ax.transAxes,
                ha="center", va="center", color="#f38ba8", fontsize=12)

    # Encode to base64
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")
