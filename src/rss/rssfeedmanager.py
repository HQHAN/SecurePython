import feedparser
import MLStripper
import ushlex
from presenter.browseropener import browseropener

class rssfeedmanager:
    # Korean RSS feed source repository
    # feedsources = ["http://www.boannews.com/media/news_rss.xml",
    #                "http://www.ahnlab.com/kr/site/rss/ahnlab_securitynews.xml",  # latest security news
    #                "http://www.ahnlab.com/kr/site/rss/ahnlab_securityfocus.xml ",  # security issue
    #                "http://company.ahnlab.com/company/site/rss/comRss/comRssPressRelease.do"]  # security news on media

    # English RSS feed source repository, this is default
    feedsourceseng = ["http://www.eweek.com/security/rss/",
                      "http://feeds.feedburner.com/Securityweek?format=xml"]

    # feedsourceseng = ["http://krebsonsecurity.com/feed/",
    # 					"https://threatpost.com/feed/",
    # 					"http://www.networkworld.com/category/security/index.rss",
    # 					"http://feeds.feedburner.com/Securityweek?format=xml",
    # 					"http://www.eweek.com/security/rss/"]

    # Filter list
    # !! Just add word that starts with unique word !!
    filterList = ["access control",
                  # "access control list",
                  # "access control service",
                  # "access management access",
                  # "access matrix",

                  "account harvesting",
                  "ack piggybacking",
                  "active content",
                  "activity monitors",
                  "Address Resolution Protocol",
                  "advanced encryption standard",

                  "asymmetric cryptography",
                  # "asymmetric warfare",
                  "Two-Factor Authentication",
                  "Simple Attacks",
                  "nuclear regulatory"]

    markup_stripper = MLStripper.MLStripper()

    # constructor : load RSS feeds into memory
    def __init__(self):
        # declare instance variable that will store downloaded feed data
        self.feedsdownloaded = []
        self.filter_dictionary = {}
        self.isfeedsourceeng = True

        # init filter dictinary
        self.__initfilterdictionary(rssfeedmanager.filterList)

        # download the feed datas from the feedsources
        self.__downloadfeeddata()

    # add source RSS feed URL
    # this downloads feed data from new source
    # and return the whole downloaded feed data list
    def addfeedsource(self, newsource):
        self.__getfeedsource().append(newsource)
        self.getcurrentfeeddatalist().append(feedparser.parse(newsource))
        return self.feedsdownloaded

    # get currenlt downloaded feed data
    # data structure consist of "1" channel to "N" item
    # channel can be referenced by listitem.feed and item list can be referenced by listitem.entries
    def getcurrentfeeddatalist(self):
        return self.feedsdownloaded

    # get keyword string from "description" && "title" of feed data
    def get_keyword_from_articles(self):
        ret = []
        for data in self.getcurrentfeeddatalist():
            for entry in data.entries:
                if hasattr(entry, 'description'):
                    rssfeedmanager.markup_stripper.feed(entry.description)
                    ret.extend(rssfeedmanager.markup_stripper.get_data().split())

                if hasattr(entry, 'title'):
                    rssfeedmanager.markup_stripper.feed(entry.title)
                    ret.extend(rssfeedmanager.markup_stripper.get_data().split())

        return self.__reorganizekeywordlist(ret)

    # refresh feed datas
    def refreshfeeddata(self):
        del self.feedsdownloaded[0:len(self.feedsdownloaded)]
        self.__downloadfeeddata()

    # set whether feed source is from eng or not, if false, then it will take the feed from korean source
    def setfeedsourcetoeng(self, eng):
        self.isfeedsourceeng = eng
        self.refreshfeeddata()

    # download feeddata
    def __downloadfeeddata(self):
        # download the feed datas from the feedsources
        for source in self.__getfeedsource():
            print "downloading feed from : %s " % source
            self.feedsdownloaded.append(feedparser.parse(source))

    # return feedsource depending on the language flag
    def __getfeedsource(self):
        if self.isfeedsourceeng:
            return rssfeedmanager.feedsourceseng
        else:
            return rssfeedmanager.feedsource

    # return reorganized keyword list using reference security keyword table,
    def __reorganizekeywordlist(self, sourceStringList):

        result = []
        current_state = "start"
        sourceStringList = list(map(lambda x: x.lower(), sourceStringList))

        for source in sourceStringList:

            if current_state == "start":
                if source in self.filter_dictionary:
                    current_state = "check"
                    start_word = source
                    checking_index = 1
                else:
                    result.append(source)

            elif current_state == "check":
                filterword_list = self.filter_dictionary[start_word]

                if source in filterword_list and filterword_list.index(source) == checking_index:
                    checking_index += 1
                    if checking_index == len(filterword_list):
                        result.append(' '.join(self.filter_dictionary[start_word]))
                        current_state = "start"
                else:
                    current_state = "start"
                    result.append(source)

        return result

    # initialize filter dictionary
    def __initfilterdictionary(self, filterlist):

        # make it lower as python is case-sensitive for string comparison
        filterlist = list(map(lambda x:x.lower(), filterlist))

        self.filter_dictionary.clear()

        for filterword in filterlist:
            filter = ushlex.split(filterword)
            self.filter_dictionary[filter[0]] = filter

# usage example
# feedparser = rssfeedmanager()

# for data in feedparser.get_keyword_from_articles():
#     print data

# print feedparser.get_keyword_from_articles()
browseropener.opengoogletrendpage(['security', 'AES', 'DES', 'encryption', 'hans'])
