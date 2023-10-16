import os.path
import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from typing import List
from asisstants import (
    save_graph,
    GRAPHS_FOLDER,
    check_path,
    find_difference,
    create_report,
    move_legend,
)
from data_preparetor import all_scores_df, fandango_df


# identifying relationship between RATING and VOTES from fandango_df
fig1 = plt.figure()
rating_vote = sns.scatterplot(data=fandango_df, x="RATING", y="VOTES")
save_graph(graph_name="fandango_rating_vote.png", sns_plot=rating_vote)

# calculating correlation
fandango_df_cor = fandango_df.drop("FILM", axis=1).corr()
print(f"correlation:\n{fandango_df_cor}")

# making a separate column with year
fandango_df["YEAR"] = (
    fandango_df["FILM"].str.extract(r"\((\d{4})\)", expand=False).astype(int)
)
print("\n", fandango_df.head())

# checking how many films were produced each year
print("\nTABLE OF FILMS PRODUCED BY YEAR\n", fandango_df.value_counts("YEAR"))

# visualizing films produced by year in the countplot
fig2 = plt.figure()
year_plot = sns.countplot(
    data=fandango_df, x="YEAR", order=fandango_df["YEAR"].value_counts().index
)
save_graph(graph_name="fandango_countplot_year.png", sns_plot=rating_vote)

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
sns.kdeplot(
    data=voted_films_df,
    x="STARS",
    clip=[0, 5],
    fill=True,
    label="Stars Displayed",
    color="orange",
)
sns.kdeplot(
    data=voted_films_df,
    x="RATING",
    clip=[0, 5],
    fill=True,
    label="True Rating",
    color="blue",
)
plt.legend(loc=(1.01, 0.5))
if not check_path(os.path.join(GRAPHS_FOLDER, "visualisation_stars_vs_rating.png")):
    plt.savefig(os.path.join(GRAPHS_FOLDER, "visualisation_stars_vs_rating.png"))

# creating a new column to calculate a difference between STARS and RATING
voted_films_df["SCORE_DIFFERENCE"] = np.vectorize(find_difference)(
    voted_films_df["STARS"], voted_films_df["RATING"]
)
print(voted_films_df)

# we need to see which differences are met and how often
fig4 = plt.figure()
difference_score_graph = sns.countplot(
    data=voted_films_df,
    x="SCORE_DIFFERENCE",
    order=voted_films_df["SCORE_DIFFERENCE"].value_counts().index,
)
save_graph(graph_name="difference_in_scores.png", sns_plot=difference_score_graph)

# from the graph we see that there are some films having a difference of 1 full score, let us find it
most_difference_film = voted_films_df[voted_films_df["SCORE_DIFFERENCE"] >= 1]
print(
    f"\nThis film(s) shows large difference between STARS and actual RATING\n{most_difference_film}"
)


# COMPARING FANDANGO WITH OTHER FILM PLATFORMS

# considering Rotten Tomatoes
# building a scatterplot to see relationship between users and critics feedbacks
fig5 = plt.figure()
rotten_tomatoes_scatter = sns.scatterplot(
    data=all_scores_df, x="RottenTomatoes", y="RottenTomatoes_User"
)
save_graph(
    graph_name="rottentomatoes_critic_scatter.png", sns_plot=difference_score_graph
)

# creating a new column to evaluate a difference in votes between professional critics and users
# this way we can see if users agree professional estimation. If the result is close to 0, they do
all_scores_df["ROTTEN_DIFFERENCE"] = np.vectorize(find_difference)(
    all_scores_df["RottenTomatoes"], all_scores_df["RottenTomatoes_User"]
)
print(all_scores_df.info())

# finding an average difference for ROTTEN_DIFFERENCE
avg_rotten_diff: float = all_scores_df["ROTTEN_DIFFERENCE"].apply(abs).mean()
print(f"\naverage difference between users and critics scores is {avg_rotten_diff}")

# difference deviation of the ROTTEN_DIFFERENCE to see differences between professional and users feedbacks
fig6 = plt.figure()
histplot_diff = sns.histplot(
    data=all_scores_df, x="ROTTEN_DIFFERENCE", kde=True, color="darkred"
)
save_graph(graph_name="rottentomatoes_diff_critic_users.png", sns_plot=histplot_diff)

# checking abs difference deviation
fig7 = plt.figure()
histplot_diff_abs = sns.histplot(
    x=all_scores_df["ROTTEN_DIFFERENCE"].apply(abs), kde=True, color="darkred", bins=25
)
save_graph(
    graph_name="rottentomatoes_diff_critic_users_abs.png", sns_plot=histplot_diff_abs
)

# finding out films with the largest difference in votes of users and professional critics
lgst_diff_films_roten = all_scores_df.nsmallest(5, "ROTTEN_DIFFERENCE")[
    ["FILM", "ROTTEN_DIFFERENCE"]
]
print(
    f"\nHere are five films with the largest difference in votes of simple users and professional critics\n{lgst_diff_films_roten}"
)

# finding out films with the largest difference in votes of professional critics and simple users
lgst_diff_films_roten_prof = all_scores_df.nlargest(5, "ROTTEN_DIFFERENCE")[
    ["FILM", "ROTTEN_DIFFERENCE"]
]
print(
    f"\nHere are five films with the largest difference in votes of professional critics and simple users\n{lgst_diff_films_roten_prof}"
)

# let us build first impressions regarding situation with MetaCritic and IMDB
# MetaCritic
fig8 = plt.figure()
metacritic_scatter = sns.scatterplot(
    data=all_scores_df, x="Metacritic", y="Metacritic_User"
)
save_graph(graph_name="metacritic_scatter.png", sns_plot=difference_score_graph)

# let us check differences between votes in MetaCritic and IMDB
fig9 = plt.figure()
metacritic_vs_IMDB_scatter = sns.scatterplot(
    data=all_scores_df, x="Metacritic_user_vote_count", y="IMDB_user_vote_count"
)
save_graph(
    graph_name="metacritic_vs_imdb_scatter.png", sns_plot=metacritic_vs_IMDB_scatter
)

# we see that there is one film where IMDB voted with the highest score while Metacritic only with 500
imdb_highest_vote_film = all_scores_df.sort_values(
    by="IMDB_user_vote_count", ascending=False
).iloc[0]
print(
    f"\nFilm with the highest score by IMDB while with 500 votes only by Metacritic\n{imdb_highest_vote_film}"
)

# Now finding the best voted film in the Metacritic
metacritic_highest_vote_film = all_scores_df.sort_values(
    by="Metacritic_user_vote_count", ascending=False
).iloc[0]
print(
    f"\nFilm with the highest score by Mecacritic while with 500 votes only by Metacritic\n{metacritic_highest_vote_film}"
)

# Comparing Fandango ratings with ratings on other given platforms

# merging two DataFrames
final_df = pd.merge(fandango_df, all_scores_df, on="FILM", how="inner")
print(final_df.info())

# converting all ratings to 1-5 scale
final_df["RT_Norm"] = np.round(final_df["RottenTomatoes"] / 20, 1)
final_df["RTU_Norm"] = np.round(final_df["RottenTomatoes_User"] / 20, 1)
final_df["Meta_Norm"] = np.round(final_df["Metacritic"] / 20, 1)
final_df["Meta_U_Norm"] = np.round(final_df["Metacritic_User"] / 2, 1)
final_df["IMDB_Norm"] = np.round(final_df["IMDB"] / 2, 1)
print(final_df.head())

# customizing final_df with columns we need for further procession
RATING_COLUMNS: List[str] = [
    "FILM",
    "STARS",
    "RATING",
    "RT_Norm",
    "RTU_Norm",
    "Meta_Norm",
    "Meta_U_Norm",
    "IMDB_Norm",
]

final_customized_df = final_df[RATING_COLUMNS]
print(final_customized_df.info())


# calculating mean value of standard deviations for all ratings of all platforms with exception for Fandango
mean_std_dev: float = np.std(
    final_customized_df[
        ["RT_Norm", "RTU_Norm", "Meta_Norm", "Meta_U_Norm", "IMDB_Norm"]
    ],
    axis=0,
).mean(axis=0)
print(
    f"\n\nMEAN VALUE OF STANDARD DEVIATION VALUES FOR ALL RATINGS FROM ALL PLATFORMS WITH EXCEPTION FOR FANDANGO: {mean_std_dev}"
)


# checking the ten worst films by RottenTomatoes in comparison with Fandango and making a csv report
ten_worst_rotten_films = final_customized_df.nsmallest(10, "RT_Norm")[
    ["FILM", "RT_Norm", "RATING", "STARS"]
]
print(ten_worst_rotten_films[["FILM", "RT_Norm", "RATING", "STARS"]])

# now we calculate a difference between RATING from FANDANGO and RottenTomatoes
ten_worst_rotten_films["rating_diff"] = (
    ten_worst_rotten_films["RATING"] - ten_worst_rotten_films["RT_Norm"]
)
print(ten_worst_rotten_films)

# taking decision if rating difference IS healthy (with no evil manipulation) or NOT healthy (manipulation is possible)
ten_worst_rotten_films["RATING_MANIPULATION_POSSIBILITY"] = ten_worst_rotten_films[
    "rating_diff"
].apply(lambda num: "high" if num > mean_std_dev else "low")
create_report(df=ten_worst_rotten_films)
print(
    "\n\nMANIPULATION POSSIBILITY FOR THE WORST RT RATED FILMS BY FANDANGO:\n",
    ten_worst_rotten_films,
)


# building a final graph to show the overall picture of possible manipulations made by Fandango 2015
fig10, ax = plt.subplots(figsize=(15, 6), dpi=150)
final_graph = sns.kdeplot(
    data=final_customized_df.drop("FILM", axis=1),
    clip=[0, 5],
    fill=True,
    palette="Set1",
    ax=ax,
)
move_legend(ax, "upper left")
save_graph(graph_name="final_graph.png", sns_plot=final_graph, figsize=(15, 6), dpi=150)
# plt.show()


# let us have a general impression how films are rated across platforms (added as an optional one)
fig11 = plt.figure()
cluster_map = sns.clustermap(
    data=final_customized_df.set_index("FILM"), cmap="mako", col_cluster=False
)
save_graph(graph_name="cluster_film_map.png", sns_plot=cluster_map)
# plt.show()
