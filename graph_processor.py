import os.path
import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from typing import List, Callable
from asisstants import save_graph, GRAPHS_FOLDER, check_path, find_difference
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
# plt.show()

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
fig3 = plt.figure()
sns.kdeplot(data=voted_films_df, x="STARS", clip=[0, 5], fill=True, label="Stars Displayed", color="orange")
sns.kdeplot(data=voted_films_df, x="RATING", clip=[0, 5], fill=True, label="True Rating", color="blue")
plt.legend(loc=(1.01, 0.5))
if not check_path(os.path.join(GRAPHS_FOLDER, "visualisation_stars_vs_rating.png")):
    plt.savefig(os.path.join(GRAPHS_FOLDER, "visualisation_stars_vs_rating.png"))
# plt.show()

# creating a new column to calculate a difference between STARS and RATING
voted_films_df["SCORE_DIFFERENCE"] = np.vectorize(find_difference)(voted_films_df["STARS"], voted_films_df["RATING"])
print(voted_films_df)

# we need to see which differences are met and how often
fig4 = plt.figure()
difference_score_graph = sns.countplot(data=voted_films_df, x="SCORE_DIFFERENCE", order=voted_films_df["SCORE_DIFFERENCE"].value_counts().index)
save_graph(graph_name="difference_in_scores.png", sns_plot=difference_score_graph)
# plt.show()

# from the graph we see that there are some films having a difference of 1 full score, let us find it
most_difference_film = voted_films_df[voted_films_df["SCORE_DIFFERENCE"] >= 1]
print(f"\nThis film(s) shows large difference between STARS and actual RATING\n{most_difference_film}")


# COMPARING FANDANGO WITH OTHER FILM PLATFORMS

# considering Rotten Tomatoes
# building a scatterplot to see relationship between users and critics feedbacks
fig5 = plt.figure()
rotten_tomatoes_scatter = sns.scatterplot(data=all_scores_df, x="RottenTomatoes", y="RottenTomatoes_User")
save_graph(graph_name="rottentomatoes_critic_scatter.png", sns_plot=difference_score_graph)
# plt.show()

# creating a new column to evaluate a difference in votes between professional critics and users
# this way we can see if users agree professional estimation. If the result is close to 0, they do
all_scores_df["ROTTEN_DIFFERENCE"] = np.vectorize(find_difference)(all_scores_df["RottenTomatoes"], all_scores_df["RottenTomatoes_User"])
print(all_scores_df.info())

# finding an average difference for ROTTEN_DIFFERENCE
avg_rotten_diff: float = all_scores_df["ROTTEN_DIFFERENCE"].apply(abs).mean()
print(f"\naverage difference between users and critics scores is {avg_rotten_diff}")

