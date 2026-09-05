import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import plotly.express as px




def apply_theme(fig, ax):
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    grey = "#888888"
    ax.tick_params(colors=grey, labelsize=9)
    for part in (ax.xaxis.label, ax.yaxis.label, ax.title):
        part.set_color(grey)
    for spine in ax.spines.values():
        spine.set_edgecolor(grey)
    return fig, ax

def missing_values_chart(df: pd.DataFrame):
    missing = df.isnull().sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(missing.index, missing.values, color="#a855f7")
    ax.set_title("Missing Values per Column")
    ax.set_ylabel("Missing Count")
    apply_theme(fig, ax)
    return fig

def column_detail_grid(df: pd.DataFrame, col: str):
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    is_numeric = pd.api.types.is_numeric_dtype(df[col])

    if is_numeric:
        axes[0, 0].hist(df[col].dropna(), bins=20, color="#a855f7")
        axes[0, 0].set_title("Histogram")
        axes[0, 1].boxplot(df[col].dropna())
        axes[0, 1].set_title("Box Plot")
    else:
        axes[0, 0].axis("off")
        axes[0, 0].text(0.1, 0.5, "Histogram: numeric columns only")
        axes[0, 1].axis("off")
        axes[0, 1].text(0.1, 0.5, "Box Plot: numeric columns only")

    top10 = df[col].value_counts().head(10)
    axes[1, 0].barh(top10.index.astype(str), top10.values,
                     color="#a855f7")
    axes[1, 0].set_title("Top 10 Values")

    axes[1, 1].axis("off")
    axes[1, 1].text(0.1, 0.5, "Missing-over-time\n(needs run history)",
                     fontsize=10)

    for ax in axes.flat:
        apply_theme(fig, ax)

    fig.tight_layout()
    return fig

def correlation_heatmap(df: pd.DataFrame):
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.shape[1] < 2:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.axis("off")
        ax.text(0.1, 0.5, "Need at least 2 numeric columns")
        apply_theme(fig, ax)
        return fig

    variances = numeric_df.var().sort_values(ascending=False)
    top_cols = variances.head(15).index
    corr = numeric_df[top_cols].corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, cmap="coolwarm", center=0,
                annot=True, fmt=".2f", ax=ax,
                cbar_kws={"label": "correlation"})
    ax.set_title(f"Correlation Heatmap (top {len(top_cols)} "
                 f"of {numeric_df.shape[1]} by variance)")
    apply_theme(fig, ax)
    return fig

def outlier_boxplot(df: pd.DataFrame, col: str):
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.boxplot(x=df[col].dropna(), ax=ax, color="#a855f7")
    ax.set_title(f"Outlier Check: {col}")
    apply_theme(fig, ax)
    return fig

def interactive_scatter(df: pd.DataFrame, x_col: str, y_col: str):
    fig = px.scatter(
        df, x=x_col, y=y_col, color=y_col,
        color_continuous_scale="Viridis",
        title=f"{x_col} vs {y_col}")
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#888888")
    return fig