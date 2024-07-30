from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Similarity:
    def __init__(self, movies):
        self.movies = movies
        self._calculate_similarity()

    def _calculate_similarity(self):
        self.titles = [movie['title'] for movie in self.movies]
        descriptions = [f"{movie['genre']} {movie['director']} {movie['actors']}" for movie in self.movies]
        count_vectorizer = CountVectorizer()
        count_matrix = count_vectorizer.fit_transform(descriptions)
        self.similarity_matrix = cosine_similarity(count_matrix)

    def get_similar_movies(self, title, top_n=5):
        if title not in self.titles:
            raise ValueError(f"Title '{title}' not found in movie list.")
        idx = self.titles.index(title)
        similarity_scores = list(enumerate(self.similarity_matrix[idx]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        similar_movies = [self.titles[i[0]] for i in similarity_scores[1:top_n+1]]
        return similar_movies
