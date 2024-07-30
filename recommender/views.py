import os
from django.shortcuts import render
from .recommender import MovieRecommender

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_file = os.path.join(BASE_DIR, 'data', 'movies_with_images.csv')

movie_recommender = MovieRecommender(data_file)

def index(request):
    if request.method == 'POST':
        title = request.POST['title']
        try:
            recommendations = movie_recommender.recommend(title)
            return render(request, 'index.html', {'title': title, 'recommendations': recommendations})
        except ValueError as e:
            return render(request, 'index.html', {'error': str(e)})
    return render(request, 'index.html')
