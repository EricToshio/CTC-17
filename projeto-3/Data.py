class Data:
    def __init__(self):
        self.atrib = {}
        self.expanded_movies = {}
        self.possible_atrib()
        self.users = self.read_users("data/users.dat")
        self.movies = self.read_movies("data/movies.dat")
        self.ratings = self.read_ratings("data/ratings.dat")
        self.key_atrib = list(self.atrib.keys())

    def possible_atrib(self):
        # self.atrib["Gender"] = set(["F","M"])
        self.atrib["Age"] = set([1,18,25,35,45,50,56])
        # self.atrib["Occupation"] = set(range(0,21))
        self.atrib["GenderMovie"] = set(['Action', 'Adventure', 'Animation', "Children's", 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'])
        # Adicionado durante a analise
        self.atrib["Year"] = set()

    def read_users(self, path):
        file_user  = open(path, "r")
        users = {}

        for user_info in file_user:
            new_user = {}
            user_info_splited = user_info.split("::")
            user_ID = int(user_info_splited[0])
            new_user["Gender"] = user_info_splited[1]
            new_user["Age"] = int(user_info_splited[2])
            new_user["Occupation"] = int(user_info_splited[3])
            new_user["Zip-code"] = user_info_splited[4]
            users[user_ID] = new_user
        file_user.close()
        return users
    
    def read_movies(self, path):
        file_movie  = open(path, "r")
        movies = {}
        for movie_info in file_movie:
            new_movie = {}
            movie_info_splited = movie_info.split("::")
            movie_ID = int(movie_info_splited[0])
            new_movie["Title"] = movie_info_splited[1]
            new_movie["Year"] = int(movie_info_splited[1].split("(")[-1][:-1])
            self.atrib["Year"].add(new_movie["Year"])
            genres_splited = list(movie_info_splited[2].split("|"))
            genres_splited[-1] = genres_splited[-1][:-1] # remove o \n
            if len(genres_splited) > 1:
                for genre in genres_splited:
                    n = {}
                    n["Year"] = new_movie["Year"]
                    n["GenderMovie"] = genre
                    if self.expanded_movies.get(movie_ID):
                        self.expanded_movies[movie_ID].append(n)
                    else:
                        self.expanded_movies[movie_ID] = [n]
            new_movie["GenderMovie"] = genres_splited[0]
            movies[movie_ID] = new_movie
        file_movie.close()
        return movies

    def read_ratings(self,path):
        file_rating = open(path, "r")
        ratings = []
        for rating_info in file_rating:
            new_rating = {}
            rating_info_splited = rating_info.split("::")
            new_rating["UserID"] = int(rating_info_splited[0])
            new_rating["MovieID"] = int(rating_info_splited[1])
            new_rating["Rating"] = int(rating_info_splited[2])
            new_rating["Timestamp"] = int(rating_info_splited[3])
            ratings.append(new_rating)
        file_rating.close()
        return ratings
    
    def generate_samples(self, percentage=30):
        samples = []
        for rate in self.ratings:
            movie_id = rate["MovieID"]
            if self.expanded_movies.get(movie_id):
                for movie in self.expanded_movies[movie_id]:
                    new_sample = {}
                    new_sample["Rating"] = rate["Rating"]
                    new_sample["Gender"] = self.users[rate["UserID"]]["Gender"]
                    new_sample["Age"] = self.users[rate["UserID"]]["Age"]
                    new_sample["Occupation"] = self.users[rate["UserID"]]["Occupation"]
                    new_sample["Year"] = movie["Year"]
                    new_sample["GenderMovie"] = movie["GenderMovie"]
                    samples.append(new_sample)
            else:
                new_sample = {}
                new_sample["Rating"] = rate["Rating"]
                new_sample["Gender"] = self.users[rate["UserID"]]["Gender"]
                new_sample["Age"] = self.users[rate["UserID"]]["Age"]
                new_sample["Occupation"] = self.users[rate["UserID"]]["Occupation"]
                new_sample["Year"] = self.movies[movie_id]["Year"]
                new_sample["GenderMovie"] = self.movies[movie_id]["GenderMovie"]
                samples.append(new_sample)
        number_of_samples = len(samples)
        size_test_set = int(percentage/100 * number_of_samples)
        return samples[:-size_test_set], samples[-size_test_set:]


if __name__ == "__main__":
    data = Data()
    # print(data.atrib["Year"])
    pass