#-*- coding: utf-8 -*-#-*- coding: utf-8 -*-

from nltk.corpus import stopwords
from rss.rssfeedmanager import rssfeedmanager

# Get tokens from RSS feeds
feedparser = rssfeedmanager()

word_list = feedparser.get_keyword_from_articles()
filtered_words = [word for word in word_list if word not in stopwords.words('english')]

print(len(word_list))
print(len(filtered_words))

print(word_list)
print(filtered_words)

