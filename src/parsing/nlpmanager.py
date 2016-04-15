#-*- coding: utf-8 -*-#-*- coding: utf-8 -*-

from nltk.corpus import stopwords
from rss.rssfeedmanager import rssfeedmanager
from operator import itemgetter
from presenter.browseropener import browseropener


class nlpManager:

    englishStopwords = ['that', 'every', 'made', 'make', 'among', 'oldest', 'common', 'sold', 'type', 'become', 'includes',
                        'recently', 'sure', 'like', 'turns', 'i\'m', 'a', 'off', 'today', 'sixth', 'you\'re', 'old',
                        'can\'t', 'know', 'remember', 'tipped', 'that\'s', 'middle', 'dating', 'know', 'getting', 'one',
                        'other', 'oldest', '6th', 'fixes', 'site\'s', 'including', 'new', 'the', 'read', 'help', 'could']

    koreanStopwords = []

    specialStopwords = ['.', ',', '(', ')', '[', ']', ':', '!', '--']

    # Constructor for NLP(natural language processing) manager
    def __init__(self):

        ################################################################################################

        # Get tokens from RSS feeds
        feedparser = rssfeedmanager()
        word_list = feedparser.get_keyword_from_articles()
        # word_list.append('denial of service')
        # word_list.append('dictionary attack')
        # word_list.append('botnet')
        # word_list = ['ack piggybacking', 'security', 'help', 'apple', 'access list', 'firmware']

        print 'Total words : %d' % len(word_list)
        print('\n')

        # Remove stopwords related with special characters
        filtered_words_special = self.removespecialchar(word_list, self.specialStopwords)

        # Remove blank list
        filtered_words_blank = self.removeblanklist(filtered_words_special)

        # Remove stopwords with nltk library
        filtered_words_rss = [word for word in filtered_words_blank if word not in stopwords.words('english')]
        print 'Removed stopwords : %d' % len(filtered_words_rss)
        print('\n')

        # Remove custom stopwords
        filtered_words_custom = self.removestopwords(filtered_words_rss, 'english')
        print 'Removed custom stopwords : %d' % len(filtered_words_custom)
        print('\n')

        # Count words
        counted_words = self.countwords(filtered_words_custom)
        print 'Counted words : %d' % len(counted_words)
        print('\n')

        # Weighted word count
        weighted_words = self.weightedwords(counted_words, 1000)
        print 'Weighted words : %d' % len(weighted_words)
        print('\n')

        # Search from Google Trend API
        security_keywords = weighted_words[0:5]
        top_keywords = []
        for keywordsDictionary in security_keywords:
            top_keywords.append(keywordsDictionary[0])

        print 'Top 5 Keywords : %s' % top_keywords
        print('\n')

        # Open web browser
        browseropener.opengoogletrendpage(top_keywords)

        iteration = 0
        while iteration < 10:
            print(weighted_words[iteration])
            iteration += 1

        ################################################################################################


    # Removing stopwords depends on language type (English or Korean)
    def removestopwords(self, words, language_type):

        if (language_type == 'english'):
            stopwords = self.englishStopwords
        else:
            stopwords = self.koreanStopwords

        # Remove word if there is exist in the stopwords list
        words_lowercase = map(lambda x:x.lower(), words)
        words_copy = list(words_lowercase)
        filtered_words = list(words_lowercase)

        # Show progress status
        progressIndex = 0
        totalLength = len(words_copy)

        for word in words_copy:
            for removedWord in stopwords:
                if word == removedWord:
                    if removedWord in filtered_words:
                        filtered_words.remove(removedWord)
            progressIndex = progressIndex + 1

            if (progressIndex % 1000) == 0:
                print "Removing custom stopwords : (%d) / (%d)" % (progressIndex, totalLength)

        return filtered_words


    # Removing stopwords regarding on special characters in sentence
    def removespecialchar(self, words, specialcharacters):

        filteredWords = []
        for filteredWord in words:
            for character in specialcharacters:
                filteredWord = filteredWord.replace(character, '')
            filteredWords.append(filteredWord)
        return filteredWords


    # Removing blank list
    def removeblanklist(self, words):

        filteredWords = []
        for filteredWord in words:
            if len(filteredWord) > 1:
                filteredWords.append(filteredWord)
        return filteredWords


    # Count words
    def countwords(self, words):

        # Show progress status
        progressIndex = 0
        totalLength = len(words)

        filteredWords = []
        for word_source in words:
            count = 0
            for word_target in words:
                if word_source == word_target:
                    count += 1
            filteredWords.append([word_source, count])

            progressIndex = progressIndex + 1

            if (progressIndex % 1000) == 0:
                print "Counting words : (%d) / (%d)" % (progressIndex, totalLength)

        filteredWords = sorted(filteredWords, key=itemgetter(1,0), reverse=True)
        deduplicatedWords = [filteredWords[i] for i in range(len(filteredWords)) if i==0 or filteredWords[i] != filteredWords[i-1]]
        return deduplicatedWords


    # Weighted words count
    def weightedwords(self, words, weight):

        filteredWords = []
        securityDictionary = []

        file = open("./security_dictionary", 'r')
        while True:
            line = file.readline()
            if not line: break
            securityDictionary.append(line.strip())
        file.close()

        # Show progress status
        progressIndex = 0
        totalLength = len(words)

        word_count = 0
        for word_source in words:
            for dic_source in securityDictionary:
                if word_source[0] == dic_source:
                    word_count = word_source[1] + weight
                    break
                else:
                    word_count = word_source[1]

            filteredWords.append([word_source[0], word_count])

            progressIndex = progressIndex + 1

            if (progressIndex % 1000) == 0:
                print "Weighting words : (%d) / (%d)" % (progressIndex, totalLength)

        filteredWords = sorted(filteredWords, key=itemgetter(1,0), reverse=True)
        return filteredWords



# Run nlp manager
nlpManager()

