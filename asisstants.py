import os

import matplotlib.pyplot as plt
import pandas as pd

from data_preparetor import CURRENT_DIR

"""Functions to assist"""

GRAPHS_FOLDER = os.path.join(CURRENT_DIR, "saved_graphs")
TEN_WORST_REPORT_PATH = os.path.join(
    CURRENT_DIR, "report_ten_worst", "report_ten_worst_films.csv"
)


def check_path(path) -> bool:
    check: bool = False
    if os.path.exists(path=path):
        check = True
    return check


def save_graph(graph_name, sns_plot, figsize=(12, 4), dpi=200):
    """Saves a graph into saved_graphs dir

    Args:
        graph_name - name of the saving img,
        sns_plot = seaborn instance,
        figsize - size of the img,
        dpi - customizing dots per inch

    Res.: saves a graph into saved_graphs
    """
    try:
        graph_dir = os.path.join(GRAPHS_FOLDER, graph_name)
        plt.Figure(figsize=figsize, dpi=dpi)
        sns_plot
        if not check_path(path=graph_dir):
            plt.savefig(graph_dir)
    except Exception as e:
        print(e)


def find_difference(num1: float, num2: float) -> float:
    return round(num1 - num2, 1)


def create_report(df: "pd.DataFrame"):
    if not check_path(TEN_WORST_REPORT_PATH):
        df.to_csv(TEN_WORST_REPORT_PATH, index=False)


def move_legend(ax, new_loc, **kws):
    old_legend = ax.legend_
    handles = old_legend.legendHandles
    labels = [t.get_text() for t in old_legend.get_texts()]
    title = "Online Film Platforms"
    ax.legend(handles, labels, loc=new_loc, title=title, **kws)
