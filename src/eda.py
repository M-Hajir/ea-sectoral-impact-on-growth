

# Imports
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def show_df(df: pd.DataFrame, head: bool = True, describe: bool = False, save: bool = False):
    """
    Show the information about a DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to show.
    head : bool, optional
        Whether to show the head of the DataFrame. The default is True.
    describe : bool, optional
        Whether to show the description of the DataFrame. The default is False.
    save : bool, optional
        Whether to save the DataFrame as a CSV file. The default is False.

    Returns
    -------
    None.
    """
    print(df.info())

    if head:
        display(df.head())

    if describe:
        descriptive_stats = df.describe().T
        descriptive_stats.index.name = "Variable"
        descriptive_stats.rename(columns={"count": "Observations",
                                          "mean": "Mean",
                                          "std": "Standard deviation",
                                          "min": "Minimum",
                                          "25%": "25th percentile",
                                          "50%": "Median",
                                          "75%": "75th percentile",
                                          "max": "Maximum"}, inplace=True)
        display(descriptive_stats.round(2))

        if save:
            descriptive_stats[[
                "Observations",
                "Mean",
                "Standard deviation",
                "Minimum",
                "Maximum"
            ]].to_csv("../results/descriptive_stats.tsv", sep="\t", float_format="%.2f", index=True)


def show_dist(df: pd.DataFrame, column: str):
    """
    Show the distribution of a variable in a DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to show.
    column : str
        The column to show.

    Returns
    -------
    None.
    """
    min = df[column].min()
    max = df[column].max()
    mean = df[column].mean()
    median = df[column].median()

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.02, row_heights=[0.8, 0.2])

    fig.add_trace(go.Histogram(x=df[column], name=column), row=1, col=1)
    fig.update_layout(template="presentation", font_family="Times New Roman",
                      showlegend=False, title=f"Distribution of {column}")
    fig.update_xaxes(title_text="Frequency", row=1, col=1)
    fig.add_shape(type="line", x0=min, y0=0, x1=min, y1=60,
                  line=dict(color="gray", width=2), row=1, col=1)
    fig.add_shape(type="line", x0=max, y0=0, x1=max, y1=60,
                    line=dict(color="gray", width=2), row=1, col=1)
    fig.add_shape(type="line", x0=mean, y0=0, x1=mean, y1=60,
                    line=dict(color="cyan", width=2), row=1, col=1)
    fig.add_shape(type="line", x0=median, y0=0, x1=median, y1=60,
                    line=dict(color="red", width=2), row=1, col=1)

    fig.add_trace(go.Box(x=df[column], name=column), row=2, col=1)
    fig.update_yaxes(title_text="", row=2, col=1, showticklabels=False)

    fig.update_layout(height=600)
    fig.show()


def plot_time_series(df: pd.DataFrame, column: str):
    """
    Plot the time series of a variable in a DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to show.
    column : str
        The column to show.

    Returns
    -------
    None.
    """
    fig = px.line(df, x=df.index.get_level_values("Year"), y=column,
                    color=df.index.get_level_values("Country"),
                    title=f"Time series of {column}")
    fig.update_layout(template="presentation", font_family="Times New Roman",
                        showlegend=True, legend_title_text="Country")


