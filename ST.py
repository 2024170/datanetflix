import streamlit as st
import pandas as pd
import numpy as np

st.title("Netflix Data Dashboard")

DATA_URL = ('https://github.com/2024170/datanetflix/blob/49421723d5101a1f21d8b8a75e4182873e0751a1/netflix_titles.csv')



@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    return data
data_load_state = st.text("Loading data...")
data = load_data(10000)
data_load_state.text("Done!")


if 'release_date' in data.columns:
    st.subheader('Number of Content Added by Year')
    data['release_date'] = pd.to_datetime(data['release_date'], errors='coerce')
    data['year'] = data['release_date'].dt.year
    hist_values = data['year'].value_counts().sort_index()
    st.bar_chart(hist_values)

# Filter by a specific year (replace 'release_date' and adjust slider values as needed)
if 'release_date' in data.columns:
    year_to_filter = st.slider('Filter by Year', int(data['year'].min()), int(data['year'].max()), int(data['year'].min()))
    filtered_data = data[data['year'] == year_to_filter]

    st.subheader(f'Content Released in {year_to_filter}')
    st.write(filtered_data)

# Optional: Add a map visualization if data has geographical info (replace `latitude` and `longitude` with actual columns)
if 'country' in data.columns and 'country' in data.columns:
    st.subheader('Map of Netflix Content Locations')
    st.map(data[['latitude', 'longitude']])
