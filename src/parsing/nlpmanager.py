#-*- coding: utf-8 -*-#-*- coding: utf-8 -*-

from nltk.corpus import stopwords
from rss.rssfeedmanager import rssfeedmanager
from operator import itemgetter


class nlpManager:

    englishStopwords = ['that', 'every', 'made', 'among', 'oldest', 'common', 'sold', 'type', 'become', 'includes',
                        'recently', 'sure', 'like', 'turns', 'i\'m', 'a', 'off', 'today', 'sixth', 'you\'re', 'old',
                        'can\'t', 'know', 'remember', 'tipped', 'that\'s', 'middle', 'dating', 'know', 'getting', 'one',
                        'other', 'oldest', '6th', 'fixes', 'site\'s', 'including', 'new']

    koreanStopwords = []

    specialStopwords = ['.', ',', '(', ')', '[', ']', ':', '!', '--']

    # Constructor for NLP(natural language processing) manager
    def __init__(self):

        ################################################################################################

        # Get tokens from RSS feeds
        feedparser = rssfeedmanager()
        word_list = feedparser.get_keyword_from_articles()

        print('Total words : %', len(word_list))

        # Remove stopwords related with special characters
        filtered_words_special = self.removespecialchar(word_list, self.specialStopwords)

        # Remove blank list
        filtered_words_blank = self.removeblanklist(filtered_words_special)

        # Remove stopwords with nltk library
        filtered_words_rss = [word for word in filtered_words_blank if word not in stopwords.words('english')]
        print('Removed stopwords : %', len(filtered_words_rss))

        # Remove custom stopwords
        filtered_words_custom = self.removestopwords(filtered_words_rss, 'english')
        print('Removed custom stopwords : %', len(filtered_words_custom))

        # Count words
        counted_words = self.countwords(filtered_words_custom)
        print('Counted words : %', len(counted_words))
        print("\n")

        iteration = 0
        while iteration < 100:
            print(counted_words[iteration])
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
        for word in words_copy:
            for removedWord in stopwords:
                if word == removedWord:
                    if removedWord in filtered_words:
                        filtered_words.remove(removedWord)

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

        filteredWords = []
        for word_source in words:
            count = 0
            for word_target in words:
                if word_source == word_target:
                    count += 1
            filteredWords.append([word_source, count])

        filteredWords = sorted(filteredWords, key=itemgetter(1,0), reverse=True)
        deduplicatedWords = [filteredWords[i] for i in range(len(filteredWords)) if i==0 or filteredWords[i] != filteredWords[i-1]]
        return deduplicatedWords




# Run nlp manager
nlpManager()

