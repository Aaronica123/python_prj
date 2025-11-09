# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os

# Page config
st.set_page_config(page_title="CORD-19 Explorer", layout="wide")

# Title
st.title("CORD-19 Research Papers Explorer")
st.markdown("""
**Explore COVID-19 research trends** from the CORD-19 dataset.  
Filter by year and title length. View publication trends, top journals, and common keywords.
""")

# Load data with caching
@st.cache_data
def load_data():
    df = pd.read_csv("data/metadata_sample.csv")
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['year'] = df['publish_time'].dt.year
    df['month'] = df['publish_time'].dt.month
    df['title_words'] = df['title'].fillna("").str.split().str.len()
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
year_range = st.sidebar.slider(
    "Publication Year Range", 
    int(df['year'].min()), int(df['year'].max()), 
    (2019, 2022)
)
min_words = st.sidebar.slider("Minimum Title Words", 5, 50, 10)

# Filter data
filtered_df = df[
    (df['year'].between(year_range[0], year_range[1])) &
    (df['title_words'] >= min_words)
].copy()

st.sidebar.metric("Papers Shown", len(filtered_df))
st.sidebar.metric("Total in Sample", len(df))

# Main layout
col1, col2 = st.columns(2)

# Plot 1: Publications over time
with col1:
    st.subheader("Publications Over Time")
    yearly = filtered_df['year'].value_counts().sort_index()
    fig, ax = plt.subplots()
    ax.plot(yearly.index, yearly.values, marker='o', color='#ff6b6b', linewidth=2)
    ax.fill_between(yearly.index, yearly.values, alpha=0.3, color='#ff6b6b')
    ax.set_title("Number of Papers by Year", fontsize=14, fontweight='bold')
    ax.set_xlabel("Year")
    ax.set_ylabel("Count")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Plot 2: Top journals
with col2:
    st.subheader("Top 10 Journals")
    top_journals = filtered_df['journal'].value_counts().head(10)
    fig, ax = plt.subplots()
    sns.barplot(x=top_journals.values, y=top_journals.index, palette="viridis", ax=ax)
    ax.set_title("Most Active Publishers", fontsize=14, fontweight='bold')
    ax.set_xlabel("Number of Papers")
    st.pyplot(fig)

# Word Cloud
st.subheader("Most Common Words in Paper Titles")
title_text = " ".join(filtered_df['title'].dropna().astype(str))
if len(title_text) > 100:
    wordcloud = WordCloud(
        width=1000, height=500,
        background_color='white',
        colormap='plasma',
        max_words=100
    ).generate(title_text)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
else:
    st.info("Not enough title text for word cloud.")

# Sample papers
st.subheader("Sample Research Papers")
display_cols = ['title', 'authors', 'journal', 'year', 'source_x']
st.dataframe(filtered_df[display_cols].head(10), use_container_width=True)

# Download filtered data
csv = filtered_df.to_csv(index=False).encode()
st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name="cord19_filtered.csv",
    mime="text/csv"
)

# Footer
st.markdown("---")
st.markdown("**CORD-19 Dataset** • Built with Streamlit • Assignment by [Your Name]")