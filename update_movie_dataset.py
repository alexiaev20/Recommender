import requests
import pandas as pd
import os

# Define o caminho para o arquivo CSV
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(BASE_DIR, 'movies.csv')
output_file = os.path.join(BASE_DIR, 'movies_with_images.csv')

# Chave da API da TMDb
API_KEY = ''
API_URL = 'https://api.themoviedb.org/3/movie/'

# Lê o arquivo CSV com os IDs dos filmes
movies_df = pd.read_csv(input_file)

# Lista para armazenar os dados dos filmes
movies_with_images = []

# Função para buscar dados do filme
def fetch_movie_data(movie_id):
    url = f'{API_URL}{movie_id}?api_key={API_KEY}&language=pt-BR'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error fetching data for movie ID {movie_id}: {response.status_code} {response.reason}')
        return None

# Processa cada ID de filme
for _, row in movies_df.iterrows():
    movie_id = row['movieId']
    movie_data = fetch_movie_data(movie_id)
    if movie_data:
        movie_info = {
            'movieId': movie_data.get('id'),
            'title': movie_data.get('title'),
            'poster_path': movie_data.get('poster_path'),
            'description': movie_data.get('overview')
        }
        movies_with_images.append(movie_info)

# Cria um DataFrame e salva em CSV
movies_with_images_df = pd.DataFrame(movies_with_images)
movies_with_images_df.to_csv(output_file, index=False)
print(f'Dataset atualizado salvo em {output_file}')
