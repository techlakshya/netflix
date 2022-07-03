from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


class Content:
    def __init__(self):
        self.df = pd.read_csv('data/app.csv', parse_dates=['date_added'], index_col=['date_added'])

        # Splitting Dataset into two parts -

        self.movies_df = self.df[self.df['type'] == 'Movie']
        self.tv_shows_df = self.df[self.df['type'] == 'TV Show']

    # Show latest Movies based on date_added -

    def latest_movies(self, n):
        latest_movies = self.movies_df[:n]
        return latest_movies

    # Show latest TV Shows based on date_added -

    def latest_tv_shows(self, n):
        latest_tv_shows = self.tv_shows_df[:n]
        return latest_tv_shows

    # Recommended movies based on director and cast using python only.

    # def recommended_movies(self, watched_movies, n):
    #     watched_directors = watched_movies.get('director')
    #     watched_casts = watched_movies.get('cast')

    #     director_df = self.movies_df['director']
    #     cast_df = self.movies_df['cast']

    #     recommendations = []

    #     if watched_directors:
    #         movies = self.movies_df[director_df.apply(lambda x: any(director in x for director in watched_directors))]['title'].to_list()
    #         recommendations.extend(movies)

    #     if watched_casts:
    #         movies = self.movies_df[cast_df.apply(lambda x: any(cast in x for cast in watched_casts))]['title'].to_list()
    #         recommendations.extend(movies)

    #     return recommendations[:n]

    # Recommended tv shows based on director and cast using python only.

    # def recommended_tv_shows(self, watched_tv_shows, n):
    #     watched_directors = watched_tv_shows.get('director')
    #     watched_casts = watched_tv_shows.get('cast')

    #     director_df = self.tv_shows_df['director']
    #     cast_df = self.tv_shows_df['cast']

    #     recommendations = []

    #     if watched_directors:
    #         tv_shows = self.tv_shows_df[director_df.apply(lambda x: any(director in x for director in watched_directors))]['title'].to_list()
    #         recommendations.extend(tv_shows)

    #     if watched_casts:
    #         tv_shows = self.tv_shows_df[cast_df.apply(lambda x: any(cast in x for cast in watched_casts))]['title'].to_list()
    #         recommendations.extend(tv_shows)

    #     return recommendations[:n]

    # Recommended tv shows based on director and cast using python only.

    def recommended_movies(self, n):
        recommendations = []

        self.movies_df = self.movies_df.reset_index()
        self.movies_df['combined_features'] = self.movies_df.apply(self.combined_features, axis=1)

        vectorizer = CountVectorizer()
        model = vectorizer.fit_transform(self.movies_df['combined_features'])

        similarity_scores = cosine_similarity(model)
        movie = "MANK"

        movie_index = self.get_movie_index(movie)
        similar_movies = list(enumerate(similarity_scores[movie_index]))

        for i in range(len(similar_movies)):
            if i >= n:
                break

            recommendations.append(self.get_movie_title(similar_movies[i][0]))

        return recommendations

    # Recommended tv shows based on director and cast using sklearn algorithm.

    def recommended_tv_shows(self, n):
        recommendations = []

        self.tv_shows_df = self.tv_shows_df.reset_index()
        self.tv_shows_df['combined_features'] = self.tv_shows_df.apply(self.combined_features, axis=1)

        vectorizer = CountVectorizer()
        model = vectorizer.fit_transform(self.tv_shows_df['combined_features'])

        similarity_scores = cosine_similarity(model)
        tv_show = "The Idhun Chronicles"

        tv_show_index = self.get_tv_show_index(tv_show)
        similar_tv_shows = list(enumerate(similarity_scores[tv_show_index]))

        for i in range(len(similar_tv_shows)):
            if i >= n:
                break

            recommendations.append(self.get_tv_show_title(similar_tv_shows[i][0]))

        return recommendations

    # Helping methods

    def combined_features(self, row):
        return f"{row['director']} {row['cast']}"

    def get_movie_index(self, movie_title):
        return self.movies_df[self.movies_df['title'] == movie_title].index[0]

    def get_movie_title(self, movie_index):
        return self.movies_df[self.movies_df.index == movie_index]["title"].values[0]

    def get_tv_show_index(self, tv_show_title):
        return self.tv_shows_df[self.tv_shows_df['title'] == tv_show_title].index[0]

    def get_tv_show_title(self, tv_show_index):
        return self.tv_shows_df[self.tv_shows_df.index == tv_show_index]["title"].values[0]


if __name__ == '__main__':
    content = Content()

    # watched_movies = {
    #     'director': ['Toshiya Shinohara', 'Hajime Kamegaki'],
    #     'cast': ['Kofi Ghanaba', 'Johny Lever']
    # }

    # watched_tv_shows = {
    #     'director': ['Cecilia Peck', 'Stuart Orme'],
    #     'cast': ['Linor Abargil', 'Linor Abargil']
    # }

    # print('\n\nRecommended Movies -\n\n')
    # print(content.recommended_movies(watched_movies, 10))

    # print('\n\nRecommended TV Shows -\n\n')
    # print(content.recommended_tv_shows(watched_tv_shows, 10))

    print(content.recommended_movies(3))
    print(content.recommended_tv_shows(3))
