import webbrowser
import urllib

class browseropener:

    # maximum no of query param is 5 ( google trend limit )
    @staticmethod
    def opengoogletrendpage(list):
        url = "https://www.google.com/trends/explore#q="

        for param in list:
            param = urllib.pathname2url(param)
            url += param + "%2C%20" # hex code for comma(,) and space delimeter

        webbrowser.open(url)