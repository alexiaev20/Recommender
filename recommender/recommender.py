import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class MovieRecommender:
    def __init__(self, data_file):
        # Carregar o dataset e preencher valores ausentes na descrição
        self.movies_df = pd.read_csv(data_file)
        self.movies_df['overview'] = self.movies_df['overview'].fillna('')
        
        # Inicializar o vetor TF-IDF e calcular a matriz de similaridade
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='portuguese')
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.movies_df['overview'])
        self.similarity_matrix = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
        
    def recommend(self, title, top_n=5):
        # Verifica se o título está no DataFrame
        if title not in self.movies_df['title'].values:
            raise ValueError(f"Filme '{title}' não encontrado no dataset.")
        
        # Obtém o índice do filme no DataFrame
        idx = self.movies_df[self.movies_df['title'] == title].index[0]
        
        # Obtém os índices dos filmes similares ordenados pela similaridade
        sim_scores = list(enumerate(self.similarity_matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Obtém os índices dos top_n filmes similares, ignorando o próprio filme
        sim_scores = sim_scores[1:top_n+1]
        movie_indices = [i[0] for i in sim_scores]
        
        # Obtém as informações dos filmes recomendados
        recommendations = self.movies_df.iloc[movie_indices]
        recommendations_list = recommendations[['movieId', 'title', 'poster_path', 'overview']].to_dict(orient='records')
        for rec in recommendations_list:
            rec['image_url'] = f"https://image.tmdb.org/t/p/w500{rec['poster_path']}"
        return recommendations_list
