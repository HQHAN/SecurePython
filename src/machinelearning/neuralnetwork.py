import word2vec
from rss.rssfeedmanager import rssfeedmanager

# word2vec.word2phrase('./text8', './text8-phrases', verbose=True)
# word2vec.word2vec('./text8-phrases', './text8.bin', size=100, verbose=True)
# word2vec.word2clusters('./text8', './text8-clusters.txt', 100, verbose=True)

# clusters = word2vec.load_clusters('./text8-clusters.txt')
# clusters['security']
# lists = clusters.get_words_on_cluster(90)[:20]
# print (lists)





# model based filtering

# model = word2vec.load('./text8.bin')

# indexes, metrics = model.cosine('queen')
# indexes, metrics = model.analogy(pos=['king', 'man'], neg=['woman'], n=20)
# result = model.generate_response(indexes, metrics).tolist()

# for item in result:
#     print (item)



# Gethering statements for training data

specialStopwords = ['.', ',', '(', ')', '[', ']', ':', '!', '--', '\"']

feedparser = rssfeedmanager()
word_list = feedparser.get_keyword_from_articles()

filteredWords = []
for filteredWord in word_list:
    for character in specialStopwords:
        filteredWord = filteredWord.replace(character, '')
        lowercase_str = filteredWord.lower()
    filteredWords.append(lowercase_str)


print (filteredWords)

str = ' '.join(filteredWords).encode('utf-8').strip()

f = open('./sample-phrases', 'w')
f.write(str)

# try:
#     word2vec.word2vec('./sample-phrases', './sample.bin', size=100, verbose=True)
#     model = word2vec.load('./sample.bin')
#     indexes, metrics = model.cosine('hacker')
#     result = model.generate_response(indexes, metrics).tolist()
#
#     print('\n')
#
#     for item in result:
#         print (item)
#
# except Exception:
#     print (Exception)