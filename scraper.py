import requests
from bs4 import BeautifulSoup
import pandas as pd

try: 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'

    # res (response) contains HTML source code of the webpage
    res = requests.get(url)
    
    # capturing error if url is not reachable
    res.raise_for_status() 

    # # if it outputs 200, its working (success)
    # print(res.status_code) 
    
    # beautiful soup will take the html content of response using .text, and then parsing it with html.parser
    bs = BeautifulSoup(res.text, 'html.parser') 
    
    # Lists to store the data
    rank = []
    name = []
    year = []
    rating = []
    
    # using class_ because just class is a keyword in python. movies_list contains a list that has 250 tr tag details
    movies_list = bs.find('tbody', class_ = "lister-list").find_all('tr')
    
    for movie in movies_list:
        
        movie_rank = movie.find('td', class_ = "titleColumn").get_text(strip=True).split('.')[0] # getting the first element from the resulting list
        movie_name = movie.find('td', class_ = "titleColumn").a.text
        movie_year = movie.find('td', class_ = "titleColumn").span.text.strip('()')
        movie_rating = movie.find('td', class_ = "ratingColumn imdbRating").strong.text

        rank.append(movie_rank)
        name.append(movie_name)
        year.append(movie_year)
        rating.append(movie_rating)
    
    # Creating dataframe
    df = pd.DataFrame({'Rank':rank,'Name':name,'Year_Released':year,'Rating':rating}) 
    print(df)
    
    # exporting dataframe to csv file
    df.to_csv('top_250_movies_imdb.csv', index=False, encoding='utf-8')
        
except Exception as e:
    print(e)