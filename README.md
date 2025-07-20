# Deploy Movie Recommender to GitHub & Streamlit Cloud

## Step 1: Prepare Your Files

Create these files in your project folder:

### 1. `app.py` (your main application)
Use the corrected code from the previous response.

### 2. `requirements.txt`
```txt
streamlit==1.28.0
pandas==2.1.0
requests==2.31.0
```

### 3. `.gitignore`
```txt
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt
.DS_Store
*.log
.streamlit/secrets.toml
```

### 4. `README.md`
```markdown
# 🎬 Movie Recommender App

A Streamlit application that helps you discover highly-rated movies by genre using The Movie Database (TMDb) API.

## Features
- Filter movies by genre, rating, and release year
- View detailed movie information including ratings and vote counts
- Download results as CSV
- Responsive and user-friendly interface

## How to Run Locally
1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Add your TMDb API key to the code
4. Run: `streamlit run app.py`

## Live Demo
[Your Streamlit Cloud URL will go here]

## API Key Setup
Get your free API key from [The Movie Database](https://www.themoviedb.org/settings/api)
```

## Step 2: Upload to GitHub

### Option A: Using GitHub Desktop (Easiest)
1. Download and install [GitHub Desktop](https://desktop.github.com/)
2. Create a GitHub account at [github.com](https://github.com)
3. Click "Create a New Repository on your hard drive"
4. Choose your project folder
5. Name your repository: `movie-recommender-app`
6. Add description: "Streamlit app for movie recommendations"
7. Click "Publish repository"
8. Make sure "Keep this code private" is unchecked (for free Streamlit deployment)

### Option B: Using Command Line
```bash
# Navigate to your project folder
cd path/to/your/project

# Initialize Git repository
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit: Movie recommender app"

# Create repository on GitHub first, then:
git remote add origin https://github.com/yourusername/movie-recommender-app.git
git branch -M main
git push -u origin main
```

### Option C: Using GitHub Web Interface
1. Go to [github.com](https://github.com) and sign in
2. Click "New repository"
3. Name: `movie-recommender-app`
4. Description: "Streamlit app for movie recommendations"
5. Make it Public
6. Click "Create repository"
7. Upload your files using the web interface

## Step 3: Deploy on Streamlit Cloud

### 1. Access Streamlit Cloud
- Go to [share.streamlit.io](https://share.streamlit.io)
- Sign in with your GitHub account

### 2. Deploy Your App
1. Click "New app"
2. Select your GitHub repository: `movie-recommender-app`
3. Branch: `main`
4. Main file path: `app.py`
5. App URL (optional): `movie-recommender` or your preferred name
6. Click "Deploy!"

### 3. Configure Secrets (Recommended)
For security, store your API key as a secret:

1. In Streamlit Cloud, go to your app settings
2. Click "Secrets"
3. Add this content:
```toml
[general]
TMDB_API_KEY = "841e24d1799a6d26590a8c291b4b6c21"
```

4. Update your `app.py` to use secrets:
```python
# Replace the API_KEY line with:
API_KEY = st.secrets.general.TMDB_API_KEY
```

## Step 4: Share Your App

Once deployed, you'll get a URL like:
`https://your-app-name.streamlit.app`

Share this URL with others to let them use your movie recommender!

## Troubleshooting

### Common Issues:

1. **Deployment fails**: Check that all files are committed to GitHub
2. **Import errors**: Verify `requirements.txt` has all dependencies
3. **API errors**: Ensure your TMDb API key is valid
4. **App doesn't update**: Push changes to GitHub, Streamlit Cloud will auto-redeploy

### Making Updates:
1. Edit your code locally
2. Commit and push changes to GitHub
3. Streamlit Cloud automatically redeploys your app

## Best Practices

- Use descriptive commit messages
- Test locally before pushing to GitHub  
- Keep your API keys secure using Streamlit secrets
- Add error handling for API failures
- Consider adding caching for better performance

## Next Steps

- Add more movie filters (actors, directors, etc.)
- Implement user favorites functionality
- Add movie poster images
- Create recommendation algorithms
- Add data visualization features
