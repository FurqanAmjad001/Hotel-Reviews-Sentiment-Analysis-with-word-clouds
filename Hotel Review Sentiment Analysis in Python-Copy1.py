#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.by import By
from selenium import webdriver
import time


# In[2]:


#url = "https://www.viator.com/tours/New-York-City/New-York-in-One-Day-Guided-Sightseeing-Tour/d687-7081NYCDAY"
#This is the website i will be targeting


# In[3]:


def parseHTML(response):
    soup = BeautifulSoup(response,'html.parser')
    content = soup.find('div', class_='reviews__1boD')
    content = soup.find_all('div', class_='review__27Tn')
    for i, text in enumerate(content):
        t = text.find_all('span')[1].text
        allReviews.append(t)
        
        
def printAllReviews(): 
    for review in allReviews:
        print(review)
        
def clickNextReviewPageButton(element):
    partialPath=driver.find_element(By.XPATH, Xpath)
    partialPath=partialPath.find_element(By.XPATH,"//div[contains(@class,'pagination__2znr' )]" )
    partialPath=partialPath.find_element(By.XPATH,"//div[contains(@class,'paginationContainer__3kKy' )]" )
    partialPath=partialPath.find_elements(By.XPATH,"//*[contains(@class,'navigationItem__1x-2' )]")[element].click()
    response = driver.page_source
    time.sleep(1)

    return response

def countReviews():
    return len(allReviews)
        
url = "https://www.viator.com/tours/New-York-City/New-York-in-One-Day-Guided-Sightseeing-Tour/d687-7081NYCDAY"
Xpath = '//*[@id="app"]/div/div/div[3]/div[2]/div[6]/div[2]/div'
allReviews=[]

print("Grabbing Page",1)
driver = webdriver.Chrome(r"C:\Users\zamja\Downloads\chromedriver.exe")
driver.get(url)

response = driver.page_source
parseHTML(response)
clickNextReviewPageButton(0)

for i in range(0,400):
    try:
        print("Grabbing Page",i+2)
        response = clickNextReviewPageButton(1)
        parseHTML(response)
    except:
            print("No More Pages")
            break  
            
print(countReviews())             #total number of reviews scraped
print(printAllReviews())          #shows customer reviews


# In[4]:


from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
for review in allReviews:
    sentiment = analyzer.polarity_scores(review)
    print(sentiment)


# In[12]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
review_sentiments = []
for review in allReviews:
    sentiment = analyzer.polarity_scores(review)
    review_sentiments.append(sentiment)
df = pd.DataFrame(review_sentiments)
df['sentiment'] = ['positive' if score > 0 else 'negative' if score < 0 else 'neutral' for score in df['compound']]

font1 = {'family':'serif','color':'blue','size':20}
font2 = {'family':'serif','color':'darkred','size':15}

sns.countplot(x='sentiment', data=df)
plt.title("Customer Sentiment", fontdict = font1)
plt.xlabel("Sentiment", fontdict = font2)
plt.ylabel("Frequency", fontdict = font2)
plt.show()


# In[7]:


from matplotlib import pyplot as plt

# Initialize the count of each sentiment
positive_count = 0
neutral_count = 0
negative_count = 0

# Iterate through the reviews and count the sentiment of each one
for review in allReviews:
    sentiment = analyzer.polarity_scores(review)
    if sentiment['compound'] > 0:
        positive_count += 1
    elif sentiment['compound'] == 0:
        neutral_count += 1
    else:
        negative_count += 1

# Create a list of the counts
sentiment_counts = [positive_count, neutral_count, negative_count]

# Create a list of the labels for the pie chart
sentiment_labels = ['Positive', 'Neutral', 'Negative']

# Create the pie chart
plt.pie(sentiment_counts, labels=sentiment_labels)

# Show the chart
plt.show()


# In[8]:


from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Prepare the reviews for wordcloud
allreviews_string = " ".join(allReviews)
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words("english"))
words = word_tokenize(allreviews_string)
words = [word for word in words if word.lower() not in stop_words]

# Create the wordcloud
wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white', 
                stopwords = stop_words, 
                min_font_size = 10).generate(" ".join(words))

# Plot the wordcloud
plt.figure(figsize = (8, 8), facecolor = None) 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 
  
plt.show()


# In[9]:


#this is for negative reviews only
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Prepare the reviews for wordcloud
analyzer = SentimentIntensityAnalyzer()
negative_reviews = []
for review in allReviews:
    sentiment = analyzer.polarity_scores(review)
    if sentiment['compound'] < 0:
        negative_reviews.append(review)

negative_reviews_string = " ".join(negative_reviews)
nltk.download('stopwords')
nltk.download('punkt')
more_stopwords = ["got", "hopefully", "try","next","would","want","even"]  #adding more stopwords
stop_words = set(stopwords.words("english") + more_stopwords)
words = word_tokenize(negative_reviews_string)
words = [word for word in words if word.lower() not in stop_words]

# Create the wordcloud
wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='black', 
                stopwords = stop_words, 
                min_font_size = 10).generate(" ".join(words))

# Plot the wordcloud
plt.figure(figsize = (8, 8), facecolor = None) 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 
  
plt.show()


# In[11]:


#this is for Positive reviews only
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Prepare the reviews for wordcloud
analyzer = SentimentIntensityAnalyzer()
negative_reviews = []
for review in allReviews:
    sentiment = analyzer.polarity_scores(review)
    if sentiment['compound'] > 0:
        negative_reviews.append(review)

negative_reviews_string = " ".join(negative_reviews)
nltk.download('stopwords')
nltk.download('punkt')
more_stopwords = ["got", "hopefully", "try","next","would","want","even"]  #adding more stopwords
stop_words = set(stopwords.words("english") + more_stopwords)
words = word_tokenize(negative_reviews_string)
words = [word for word in words if word.lower() not in stop_words]

# Create the wordcloud
wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='black', 
                stopwords = stop_words, 
                min_font_size = 10).generate(" ".join(words))

# Plot the wordcloud
plt.figure(figsize = (8, 8), facecolor = None) 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 
  
plt.show()


# In[ ]:




