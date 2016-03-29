import feedparser
import MLStripper


class rssfeedmanager:
    # Korean RSS feed source repository
    feedsources = ["http://www.boannews.com/media/news_rss.xml",
                   "http://www.ahnlab.com/kr/site/rss/ahnlab_securitynews.xml",  # latest security news
                   "http://www.ahnlab.com/kr/site/rss/ahnlab_securityfocus.xml ",  # security issue
                   "http://company.ahnlab.com/company/site/rss/comRss/comRssPressRelease.do"]  # security news on media

    # English RSS feed source repository, this is default
    feedsourceseng = ["http://www.eweek.com/security/rss/",
                      "http://feeds.feedburner.com/Securityweek?format=xml"]

    # feedsourceseng = ["http://krebsonsecurity.com/feed/",
    # 					"https://threatpost.com/feed/",
    # 					"http://www.networkworld.com/category/security/index.rss",
    # 					"http://feeds.feedburner.com/Securityweek?format=xml",
    # 					"http://www.eweek.com/security/rss/"]

    markup_stripper = MLStripper.MLStripper()

    # constructor : load RSS feeds into memory
    def __init__(self):
        # declare instance variable that will store downloaded feed data
        self.feedsdownloaded = []
        self.isfeedsourceeng = True

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
        return ret

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

# usage example
# feedparser = rssfeedmanager()
#
# for data in feedparser.get_keyword_from_articles():
# 	print data
