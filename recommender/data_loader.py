import pandas as pd

class DataLoader:
    def __init__(self, movies_file):
        self.movies_file = movies_file

    def load_data(self):
        movies_df = pd.read_csv(self.movies_file)
        movies = []
        for _, row in movies_df.iterrows():
            movie = {
                'title': row['title'],
                'genre': row['genres'],
                'director': '',  # Diretor não está disponível no MovieLens
                'actors': ''     # Atores não estão disponíveis no MovieLens
            }
            movies.append(movie)
        return movies
