import feedparser

class rssfeedmanager:

	# Korean RSS feed source repository 
	feedsources = ["http://www.boannews.com/media/news_rss.xml", 
					"http://www.ahnlab.com/kr/site/rss/ahnlab_securitynews.xml", # latest security news
					"http://www.ahnlab.com/kr/site/rss/ahnlab_securityfocus.xml ", # security issue
					"http://company.ahnlab.com/company/site/rss/comRss/comRssPressRelease.do"] # security news on media

	# English RSS feed source repository, this is default
	feedsourceseng = ["http://krebsonsecurity.com/feed/",
						"https://threatpost.com/feed/",
						"http://www.networkworld.com/category/security/index.rss"]

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

	# get article strings parsed like "description" && "title" from feed data 
	def getarticles(self):
		ret = []
		for data in feedparser.getcurrentfeeddatalist():
			for entry in data.entries:
				if hasattr(entry, 'description'):
					ret.append(entry.description)

				if hasattr(entry, 'title'):
					ret.append(entry.title)
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
feedparser = rssfeedmanager()

for data in feedparser.getarticles():
	print data








	 






