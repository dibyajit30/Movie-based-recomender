from movie_data_scraping import ExtractMovieContent as emc
import pandas as pd

filePath  = "MovieList.txt"
movieFile = open(filePath, encoding="utf8")

movies_keywords = {}
movies_name = []
movies_genre = []
i = 1
for movie in movieFile:
    movie = movie.strip()
    movies_name.append(movie)
    genre = emc.getMovieGenre(movie)
    movies_genre.append(genre)
    print("Getting genres for movie " + str(i))
    i += 1

save = pd.DataFrame(movies_genre)
save.insert(0, 'Movie', movies_name)
save.to_csv('movie_genre.csv', index = False)
save.tail()