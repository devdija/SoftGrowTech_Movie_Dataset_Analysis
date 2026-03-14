import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast

st.set_page_config(page_title="Movie Data Analysis Dashboard", layout="wide")

st.title("🎬 Movie Data Analysis Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv("tmdb_5000_movies.csv")

    # Data cleaning
    df = df.drop(columns=["homepage","tagline"])

    df['overview'] = df['overview'].fillna("No overview available")
    df = df.dropna(subset=['release_date'])

    df['release_date'] = pd.to_datetime(df['release_date'])
    df['release_year'] = df['release_date'].dt.year

    df['runtime'] = df['runtime'].fillna(df['runtime'].median())

    def get_genre(x):
        genres = ast.literal_eval(x)
        return [i['name'] for i in genres]

    df['genres'] = df['genres'].apply(get_genre)

    return df

df = load_data()

genres_df = df.explode('genres')

st.sidebar.header("Filters")

selected_year = st.sidebar.slider(
    "Select Release Year",
    int(df['release_year'].min()),
    int(df['release_year'].max()),
    int(df['release_year'].max())
)

filtered_df = df[df['release_year'] <= selected_year]

tab1, tab2, tab3, tab4 = st.tabs([
    "Genre Analysis",
    "Ratings & Popularity",
    "Revenue Analysis",
    "Movie Trends"
])

# GENRE ANALYSIS
with tab1:

    st.subheader("Most Common Movie Genres")

    genre_counts = genres_df['genres'].value_counts()

    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(x=genre_counts.values[:10], y=genre_counts.index[:10])
    plt.xlabel("Number of Movies")
    plt.ylabel("Genre")

    st.pyplot(fig)


    st.subheader("Highest Rated Genres")

    genre_ratings = genres_df.groupby('genres')['vote_average'].mean().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(10,6))
    genre_ratings.head(10).plot(kind='bar')
    plt.ylabel("Average Rating")

    st.pyplot(fig)


# RATINGS & POPULARITY
with tab2:

    st.subheader("Popularity vs Ratings")

    fig, ax = plt.subplots()
    sns.scatterplot(x='popularity', y='vote_average', data=filtered_df)
    plt.xlabel("Popularity")
    plt.ylabel("Average Rating")

    st.pyplot(fig)


    st.subheader("Vote Count vs Popularity")

    fig, ax = plt.subplots()
    sns.scatterplot(x='popularity', y='vote_count', data=filtered_df)

    st.pyplot(fig)


    st.subheader("Distribution of Movie Ratings")

    fig, ax = plt.subplots()
    sns.histplot(filtered_df['vote_average'], bins=20)

    st.pyplot(fig)


# REVENUE ANALYSIS
with tab3:

    st.subheader("Top 10 Highest Revenue Movies")

    top_revenue = filtered_df.sort_values('revenue', ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(x='revenue', y='title', data=top_revenue)

    st.pyplot(fig)


    st.subheader("Budget vs Revenue")

    fig, ax = plt.subplots()
    sns.scatterplot(x='budget', y='revenue', data=filtered_df)

    st.pyplot(fig)


# MOVIE TRENDS
with tab4:

    st.subheader("Movies Released Per Year")

    movies_per_year = filtered_df['release_year'].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(10,6))
    movies_per_year.plot()

    plt.xlabel("Year")
    plt.ylabel("Number of Movies")

    st.pyplot(fig)


    st.subheader("Runtime Distribution")

    fig, ax = plt.subplots()
    sns.histplot(filtered_df['runtime'])

    st.pyplot(fig)


st.subheader("Top Rated Movies")

top_rated = filtered_df.sort_values('vote_average', ascending=False)[['title','vote_average']].head(10)

st.dataframe(top_rated)
