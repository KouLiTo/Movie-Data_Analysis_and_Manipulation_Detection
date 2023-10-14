import os

import matplotlib.pyplot as plt

from data_preparetor import CURRENT_DIR

"""Functions to assist"""

GRAPHS_FOLDER = os.path.join(CURRENT_DIR, "saved_graphs")


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

