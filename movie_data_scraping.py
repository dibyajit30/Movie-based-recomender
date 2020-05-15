from bs4 import BeautifulSoup
import requests

class ExtractMovieContent:
    def ExtractMovieContent(self):
        pass
    
    def getMovieContent(movieName):
        movieName = movieName.replace(' ', '_', -1)
        url = "https://en.wikipedia.org/wiki/" + movieName + "_(film)"
        get_result = requests.get(url)
        soup = BeautifulSoup(get_result.content, "lxml")
        content = soup.select("#mw-content-text .mw-parser-output p")
        words = {}
        for con in content:
            line = con.get_text().split()
            for word in line:
                if word in words.keys():
                    words[word] += 1
                else:
                    words[word] = 1
        return words
    
    def getMovieGenre(movieName):
        movieName = movieName.replace(' ', '_', -1)
        url = "https://www.rottentomatoes.com/m/" + movieName
        get_result = requests.get(url)
        soup = BeautifulSoup(get_result.content, "lxml")
        content = soup.select("#mainColumn .movie_info .content_body .content-meta.info .clearfix:nth-child(2) .meta-value a")
        words = []
        for con in content:
            line = con.get_text().split('&')
            for word in line:
                words.append(word.strip())
        return words