from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class BookRecommender:

    def __init__(self, books_df):
        self.books = books_df.copy()

        self.books["content"] = (
            self.books["titre"] + " " +
            self.books["genre"] + " " +
            self.books["auteur"] + " " +
            self.books["synopsis"]
        )

        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = self.vectorizer.fit_transform(self.books["content"])

    def recommend(self, book_titles, top_n=3):
        if self.books.empty or not book_titles:
            return []

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
            title = self.books.iloc[idx]["titre"]
            if title not in book_titles:
                recommendations.append(title)
            if len(recommendations) == top_n:
                break

        return recommendations
