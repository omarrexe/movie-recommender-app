import requests
import pandas as pd
import streamlit as st

API_KEY = "841e24d1799a6d26590a8c291b4b6c21"  # Put API key here or use st.secrets

GENRE_IDS = {
    28: "Action",
    9648: "Mystery",
    35: "Comedy",
    18: "Drama",
    27: "Horror",
    878: "Science Fiction",
    53: "Thriller",
    10749: "Romance"
}

def fetch_movies_by_genre(genre_id, genre_name, min_rating=7.0, year_start=2010, year_end=2025, max_pages=None):
    all_movies = []
    page = 1
    total_pages = 1
   
    # If max_pages is None, fetch all available pages, otherwise limit to max_pages
    while page <= total_pages and (max_pages is None or page <= max_pages):
        params = {
            "api_key": API_KEY,
            "language": "en-US",
            "sort_by": "vote_average.desc",
            "with_genres": str(genre_id),
            "with_original_language": "en",
            "vote_count.gte": 500,
            "vote_average.gte": min_rating,
            "primary_release_date.gte": f"{year_start}-01-01",
            "primary_release_date.lte": f"{year_end}-12-31",
            "page": page
        }
       
        r = requests.get("https://api.themoviedb.org/3/discover/movie", params=params)
        r.raise_for_status()
        data = r.json()
       
        total_pages = data.get("total_pages", 1)  # Get actual total pages from API
        for movie in data.get("results", []):
            title = movie.get("title", "")
            release_date = movie.get("release_date", "")
            release_year = release_date.split("-")[0] if release_date else ""
            movie_id = movie.get("id")
            rating = movie.get("vote_average", 0.0)  # Adding the rating
            vote_count = movie.get("vote_count", 0)  # Adding vote count
            overview = movie.get("overview", "")  # Adding overview description
           
            all_movies.append({
                "id": movie_id,
                "title": title,
                "release_year": release_year,
                "rating": round(rating, 1),  # Round rating to one decimal place
                "vote_count": vote_count,
                "overview": overview,
                "genre": genre_name
            })
       
        page += 1
   
    return all_movies

def fetch_selected_movies(selected_genres, min_rating=7.0, year_start=2010, year_end=2025, max_pages=None):
    all_movies = []
    for genre_id, genre_name in selected_genres.items():
        genre_movies = fetch_movies_by_genre(genre_id, genre_name, min_rating, year_start, year_end, max_pages)
        all_movies.extend(genre_movies)
   
    df = pd.DataFrame(all_movies)
    if len(df) == 0:
        return pd.DataFrame()
   
    if len(selected_genres) > 1:
        df_dedup = df.drop_duplicates(subset=['id'], keep='first')
        duplicate_ids = df[df.duplicated(subset=['id'], keep=False)]['id'].unique()
        for movie_id in duplicate_ids:
            genres = df[df['id'] == movie_id]['genre'].unique()
            combined = ', '.join(genres)
            df_dedup.loc[df_dedup['id'] == movie_id, 'genre'] = combined
        df = df_dedup
   
    # Remove ID from final display
    df = df.drop('id', axis=1)
    
    # Convert release year to numeric
    df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')
    
    # Sort by rating first, then by year
    df = df.sort_values(['rating', 'release_year'], ascending=[False, False])
    
    # Reorder columns for better display
    df = df[['title', 'release_year', 'rating', 'vote_count', 'genre', 'overview']]
    
    return df

# ----------------- Streamlit UI -----------------
st.title("🎬 Movie Recommender")

# Add information about the app
st.markdown("""
**Find highly-rated movies by genre with detailed ratings and vote counts.**
Movies are sorted by rating (highest first) and include vote counts for reliability.
""")

genre_names = list(GENRE_IDS.values())
genre_ids_list = list(GENRE_IDS.keys())

# Improve selection interface
col1, col2 = st.columns(2)

with col1:
    selected = st.multiselect("Select one or more genres:", genre_names)
    min_rating = st.slider("Minimum Rating", 0.0, 10.0, 7.0, 0.1)

with col2:
    year_range = st.slider("Release Year Range", 1980, 2025, (2010, 2025))
    show_overview = st.checkbox("Show movie overviews", value=False)

# Add option to control how much data to fetch
fetch_all_data = st.checkbox("Fetch all available movies (may take longer)", value=False)
max_pages = None if fetch_all_data else 3

if fetch_all_data:
    st.warning("⚠️ Fetching all data may take 30-60 seconds depending on your filters.")

selected_genres = {
    genre_ids_list[genre_names.index(name)]: name for name in selected
}

fetch_clicked = st.button("🔍 Fetch Movies", key="fetch_movies_btn")

if fetch_clicked:
    if not selected_genres:
        st.warning("Please select at least one genre.")
    else:
        with st.spinner("Fetching movies..."):
            df = fetch_selected_movies(selected_genres, min_rating, year_range[0], year_range[1], max_pages)
       
        if len(df) > 0:
            st.success(f"Found {len(df)} unique movies")
            
            # Add quick statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Average Rating", f"{df['rating'].mean():.1f}")
            with col2:
                st.metric("Highest Rating", f"{df['rating'].max():.1f}")
            with col3:
                st.metric("Movies Above 8.0", len(df[df['rating'] >= 8.0]))
            
            # Hide or show overview column based on selection
            display_df = df.copy()
            if not show_overview:
                display_df = display_df.drop('overview', axis=1)
            
            # Display table with better formatting
            st.dataframe(
                display_df.head(20), 
                use_container_width=True,
                column_config={
                    "rating": st.column_config.NumberColumn(
                        "Rating ⭐",
                        help="TMDb rating (0-10)",
                        format="%.1f"
                    ),
                    "vote_count": st.column_config.NumberColumn(
                        "Votes",
                        help="Number of user votes"
                    ),
                    "release_year": st.column_config.NumberColumn(
                        "Year",
                        format="%d"
                    ),
                    "overview": st.column_config.TextColumn(
                        "Overview",
                        width="large"
                    )
                }
            )
           
            # Improve CSV download
            csv = df.to_csv(index=False)
            st.download_button(
                "💾 Download Full Results as CSV", 
                data=csv, 
                file_name=f"movies_{'-'.join(selected).lower().replace(' ', '_')}.csv", 
                mime="text/csv",
                key="download_csv_btn"
            )
            
            # Add additional information
            if not fetch_all_data and len(df) >= 50:  # Adjusted condition
                st.info("💡 Showing limited results (3 pages). Check 'Fetch all available movies' for complete data.")
            elif fetch_all_data:
                st.info(f"✅ Fetched complete dataset from TMDb API.")
                
        else:
            st.error("No movies found. Try changing filters.")