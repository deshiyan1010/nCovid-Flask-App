import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd 
import nltk
import numpy as np

def news_mod():
    print("in")
    page = requests.get('https://timesofindia.indiatimes.com/home/headlines') 
    soup = BeautifulSoup(page.content, 'html.parser')

    weblinks = soup.find_all('a')

    word_bag = ["Covid-19","Covid","covid-19","covid","Corona","Coronavirus","corona","coronavirus"]


    pagelinks = []
    header = []

    for link in weblinks[2:]:  
        try:
            inter = set.intersection(set(word_bag),set(nltk.word_tokenize(link.text)))
            if str(inter) != "set()":
                pagelinks.append("https://www.timesofindia.indiatimes.com"+link.attrs['href'])
                header.append(link.text)

        except Exception as e:
            pass

    zipped_news = pd.DataFrame(list(zip(header,pagelinks))).to_numpy()

    return zipped_news

if __name__=="__main__":
    
    df = pd.DataFrame(news())

    df.to_csv("news.csv")
    
    
    #print(time)
 