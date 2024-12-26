import streamlit as st
import pickle
import pandas as pd

st.set_page_config(
    page_title="Movie Recommender System",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f5f5;
        font-family: 'Arial', sans-serif;
    }
    .title {
        color: #2c3e50;
        text-align: center;
    }
    .recommendation-header {
        color: #e74c3c;
        margin-top: 20px;
    }
    .movie-info {
        color: #34495e;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎥 Movie Recommender System 🍿")

# Load data
df = pd.read_csv("C:\\Users\\Asus\\Downloads\\Recommendation system\\movie\\tmdb_5000_movies.csv")  
movies_dict = pickle.load(open("movies_d.pkl", "rb"))
data = pd.DataFrame(movies_dict) 
similarity = pickle.load(open("sim.pkl", "rb"))

# Recommendation function
def recommend(movie):
    """Recommend movies based on similarity."""
    index = data[data["title"] == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1]
    )[1:6]

    rec_movies = []
    for i in movie_list:
        rec_movies.append(data.iloc[i[0]])
    return rec_movies


## Process genre
import ast

def convertor(obj):
    """Convert a JSON-like string of genres into a readable format."""
    try:
        genres = ast.literal_eval(obj)  
        return ", ".join(genre["name"] for genre in genres) 
    except (ValueError, SyntaxError, KeyError):
        return "Unknown"



df['genres']=df['genres'].apply(convertor)

# Select movie
movie_name = st.selectbox("🎬 Pick a Movie:", data["title"].values)

if st.button("💡 Recommend"):
    recommendations = recommend(movie_name)
    st.markdown("<h2 class='recommendation-header'>🎉 Recommended Movies</h2>", unsafe_allow_html=True)

    # Display recommendations with details from `df`
    for movie in recommendations:
        movie_title = movie['title']
        movie_details = df[df['title'] == movie_title].iloc[0]  # Fetch details from df
        
        st.markdown(f"### {movie_title}")  # Movie title
        st.write(f"**Genre:** {movie_details.get('genres', 'N/A')}")  # Genre
        st.write(f"**Release Date:** {movie_details.get('release_date', 'Unknown')}")  # Release year
        st.write(f"**Description:** {movie_details.get('overview', 'No description available.')}")  # Description
        st.markdown("---")
