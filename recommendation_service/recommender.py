from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class BookRecommender:

    def __init__(self, books_df):
        self.books = books_df.copy()

        # Créer un champ "content" pour le TF-IDF
        self.books["content"] = (
                self.books["titre"].astype(str) + " " +
                self.books["genre"].astype(str) + " " +
                self.books["auteur"].astype(str) + " " +
                self.books["synopsis"].astype(str)
        )

        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = self.vectorizer.fit_transform(self.books["content"])

    def recommend(self, book_titles, top_n=3):
        """
        Retourne la liste complète des livres recommandés sous forme de dictionnaires.
        """
        if self.books.empty or not book_titles:
            return []

        # indices des livres empruntés
        indices = self.books[self.books["titre"].isin(book_titles)].index
        if len(indices) == 0:
            return []

        similarity = cosine_similarity(
            self.tfidf_matrix[indices],
            self.tfidf_matrix
        )

        mean_similarity = similarity.mean(axis=0)
        recommended_indices = mean_similarity.argsort()[::-1]

        recommendations = []
        for idx in recommended_indices:
            book = self.books.iloc[idx]
            if book["titre"] not in book_titles:
                # Renvoie toutes les colonnes du livre
                recommendations.append(book.to_dict())
            if len(recommendations) == top_n:
                break

        return recommendations