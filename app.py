import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


# st.header('Movie Recommender System Using Machine Learning')
movies = pickle.load(open('artifacts/movie_list.pkl','rb'))
similarity = pickle.load(open('artifacts/similarity.pkl','rb'))

# movie_list = movies['title'].values
# selected_movie = st.selectbox(
#     "Type or select a movie from the dropdown",
#     movie_list
# )

# if st.button('Show Recommendation'):
#     recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
#     col1, col2, col3, col4, col5 = st.columns(5)
#     with col1:
#         st.text(recommended_movie_names[0])
#         st.image(recommended_movie_posters[0])
#     with col2:
#         st.text(recommended_movie_names[1])
#         st.image(recommended_movie_posters[1])

#     with col3:
#         st.text(recommended_movie_names[2])
#         st.image(recommended_movie_posters[2])
#     with col4:
#         st.text(recommended_movie_names[3])
#         st.image(recommended_movie_posters[3])
#     with col5:
#         st.text(recommended_movie_names[4])
#         st.image(recommended_movie_posters[4])



# Page configuration
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# Custom CSS for white theme
st.markdown(
    """
    <style>
    .stApp {
        background-color: #ffffff;
    }
    .title {
        font-size: 32px;
        font-weight: bold;
        color: #333333;
        text-align: center;
    }
    .subtitle {
        font-size: 18px;
        color: #555555;
        text-align: center;
    }
    .paragraph {
        font-size: 14px;
        color: #555555;
        text-align: center;
    }
    .movie-card {
        text-align: center;
        margin: 10px;
        padding: 10px;
        border: 1px solid #eaeaea;
        border-radius: 10px;
        background-color: #f9f9f9;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .movie-title {
        font-size: 16px;
        font-weight: bold;
        color: #444444;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header section
st.markdown("<h1 class='title'>CPSC 8740: AI-Receptive Software Engineering - Movie Recommender System 🎥</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='subtitle'>Find movies similar to your favorite ones!</h3>", unsafe_allow_html=True)
st.markdown("<p class='paragraph'>by Sai Sriharsha Griddaluru</p>", unsafe_allow_html=True)

# Movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list,
    key="movie_selector",
)

# Recommendations
if st.button('Show Recommendations'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    # Display recommendations in a row
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.markdown(
                f"""
                <div class="movie-card">
                    <img src="{recommended_movie_posters[i]}" alt="{recommended_movie_names[i]}" width="100%" style="border-radius:10px;"/>
                    <p class="movie-title">{recommended_movie_names[i]}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )