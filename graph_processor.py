import re
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from typing import List, Callable
from asisstants import save_graph
from data_preparetor import all_scores_df, fandango_df


# identifying relationship between RATING and VOTES from fandango_df
rating_vote = sns.scatterplot(data=fandango_df, x="RATING", y="VOTES")
save_graph(graph_name="fandango_rating_vote.png", sns_plot=rating_vote)
# plt.show()

# calculating correlation
fandango_df_cor = fandango_df.drop("FILM", axis=1).corr()
print(f"correlation:\n{fandango_df_cor}")

# making a separate column with year
fandango_df["YEAR"] = fandango_df["FILM"].str.extract(r"\((\d{4})\)", expand=False).astype(int)
print("\n", fandango_df.head())

# checking how many films were produced each year
print("\nTABLE OF FILMS PRODUCED BY YEAR\n", fandango_df.value_counts("YEAR"))

# visualizing films produced by year in the countplot
fig2 = plt.figure()
year_plot = sns.countplot(data=fandango_df, x="YEAR", order=fandango_df['YEAR'].value_counts().index)
save_graph(graph_name="fandango_countplot_year.png", sns_plot=rating_vote)
plt.show()

# checking the top ten films rated
top_ten = fandango_df.nlargest(columns=["VOTES"], n=10)
print(f"\nTEN MOST RATED FILMS\n{top_ten}")

# finding films with zero votes
zero_votes_films = fandango_df[fandango_df["VOTES"] == 0]
total_zero_votes = zero_votes_films.shape[0]
print(f"\nFIMLS WITH ZERO VOTES\n{zero_votes_films}\n\nTOTAL: {total_zero_votes}")

# creating df only with films which have votes
voted_films_df = fandango_df[fandango_df["VOTES"] > 0]
print(f"\nDataFrame with voted films\n{voted_films_df}")

# estimating kernel density (KDE) for RATING and STARS (that is built on the RATING)