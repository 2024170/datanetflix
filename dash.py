import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Netflix Data Dashboard 🎥",
    page_icon="🎬🍿",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_URL = 'https://raw.githubusercontent.com/2024170/datanetflix/main/netflix_titles.csv'
df = pd.read_csv(DATA_URL)

data_load_state = st.text("Loading data...")
data_load_state.text("Done!")  

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(df)

df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')  # Handle non-numeric values in release_year
df['rating'] = df['rating'].fillna('No Rating')  # Handle missing ratings
df['genres'] = df['listed_in'].str.split(",")  # Split genres in 'listed_in' column

df['country'] = df['country'].fillna('')  # Replace NaN with empty string for countries
df['countries'] = df['country'].str.split(",")  # Split countries in 'country' column

#Introduction
st.sidebar.title("🎥 Netflix Genre Dashboard 🎬")
st.sidebar.markdown("""
    You can filter by genre and then you will see the Ratings Distribution, the top Countries, and the Distribution through the years.
""")

genre_filter = st.sidebar.multiselect(
    'Filter by Genre(s):',
    options=df['listed_in'].str.split(',').explode().unique(),
    default=df['listed_in'].str.split(',').explode().unique()[:3]  # Default to top 3 genres
)

if genre_filter:
    filtered_df = df[df['listed_in'].apply(lambda x: any(genre in x for genre in genre_filter))]
else:
    filtered_df = df

st.header("Key Data Insights")

# Titles
st.subheader("Total Titles in the Dataset")
total_titles = len(filtered_df)
st.write(f"Total number of titles: {total_titles}")

# Genres
st.subheader("Total Unique Genres")
total_genres = len(set([genre for sublist in filtered_df['genres'] for genre in sublist]))
st.write(f"Total unique genres: {total_genres}")

# Countries
st.subheader("Total Unique Countries")
total_countries = len(set([country for sublist in filtered_df['countries'] for country in sublist]))
st.write(f"Total unique countries: {total_countries}")

# Ratings Distribution
st.subheader("Ratings Distribution ⭐")
rating_counts = filtered_df['rating'].value_counts()
st.bar_chart(rating_counts)

# Popular Genres
st.subheader("Most Popular Genres")
genre_counts = filtered_df['listed_in'].str.split(',').explode().value_counts().head(10)
st.bar_chart(genre_counts)

# Top 10 Countries by Number of Titles
st.subheader("Top 10 Countries by Number of Titles")
country_counts = filtered_df['countries'].explode().value_counts().head(10)
st.bar_chart(country_counts)

# Release Year Distribution
st.subheader("Distribution of Titles by Release Year 📅")
release_year_counts = filtered_df['release_year'].value_counts().sort_index()

# Plot using Matplotlib
plt.figure(figsize=(10, 6))
sns.lineplot(x=release_year_counts.index, y=release_year_counts.values, marker='o')
plt.title("Distribution of Titles by Release Year")
plt.xlabel("Release Year")
plt.ylabel("Number of Titles")
st.pyplot(plt)
