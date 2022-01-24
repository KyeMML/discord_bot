# #install pytrends
# !pip install pytrends or conda install -c conda-forge pytrends
#import the libraries
import pandas as pd
from pytrends.request import TrendReq
pytrend = TrendReq()


# Get Google Keyword Suggestions
def keywordSearch(word):
    keywords = pytrend.suggestions(keyword=word)
    df = pd.DataFrame(keywords)
    return df
# Get Google Keyword Suggestions
def textSuggestions(text):
    return pytrend.suggestions(keyword=text)


# Get Google Hot Trends data
def trendingSearchs():
    return pytrend.trending_searches()
