import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

CURRENT_DIR = os.getcwd()
ALL_SITES_SCORES_PATH = os.path.join(CURRENT_DIR, "data_dir", "all_sites_scores.csv")
FANDANGO_SCRAPE_PATH = os.path.join(CURRENT_DIR, "data_dir", "fandango_scrape.csv")

all_scores_df: "pd.DataFrame" = pd.read_csv(ALL_SITES_SCORES_PATH)
fandango_df: "pd.DataFrame" = pd.read_csv(FANDANGO_SCRAPE_PATH)






