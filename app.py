import pickle
from flask import Flask, render_template, request

# Initialize the Flask app
app = Flask(__name__)

# Load movies and similarity data
with open('movies.pkl', 'rb') as f:
    movies = pickle.load(f)

with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

# Extract movie titles
movie_titles = movies['title'].tolist()

# Recommendation function
def recommend(title):
    if title not in movie_titles:
        return ["Movie not found."]
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(similarity[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]
    return [movie_titles[i[0]] for i in sim_scores]

# Main route
@app.route('/', methods=['GET', 'POST'])
def home():
    recommendations = []
    if request.method == 'POST':
        selected_movie = request.form.get('movie')
        if selected_movie:
            recommendations = recommend(selected_movie)
    return render_template('index.html', movie_titles=movie_titles, recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)