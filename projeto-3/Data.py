class Data:
    def __init__(self):
        self.atrib = {}
        self.possible_atrib()
        self.users = self.read_users("data/users.dat")
        self.movies = self.read_movies("data/movies.dat")
        self.ratings = self.read_ratings("data/ratings.dat")
        self.key_atrib = list(self.atrib.keys())


    def possible_atrib(self):
        self.atrib["Gender"] = set(["F","M"])
        self.atrib["Age"] = set([1,18,25,35,45,50,56])
        self.atrib["Occupation"] = set(range(1,21))
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
            new_movie["GenderMovie"] = set(movie_info_splited[2].split("|"))
            new_movie["Year"] = int(movie_info_splited[1].split("(")[-1][:-1])
            self.atrib["Year"].add(new_movie["Year"])
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
    
    def generate_samples(self):
        samples = []
        for rate in self.ratings:
            new_sample = {}
            new_sample["Rating"] = rate["Rating"]
            new_sample["Gender"] = self.users[rate["UserID"]]["Gender"]
            new_sample["Age"] = self.users[rate["UserID"]]["Age"]
            new_sample["Occupation"] = self.users[rate["UserID"]]["Occupation"]
            new_sample["Year"] = self.movies[rate["MovieID"]]["Year"]
            new_sample["GenderMovie"] = self.movies[rate["MovieID"]]["GenderMovie"]
            samples.append(new_sample)
        return samples


if __name__ == "__main__":
    data = Data()
    print(data.atrib["Year"])
    pass