"""
Scripts to access Monroe API
see http://www.monroe.api.com
or
https://github.com/bengwinter/monroe_gem
"""

from urllib2 import urlopen

def articles(first, last):
    "get articles based on MoC's name"

    base = 'http://monroeapi.com/'
    

    url = base + "articles?first_name=" + first + \
            "&last_name=" + last + "&api_key=" + uid

    return(urlopen(url).read())

"""
http://political-sentiment.herokuapp.com/articles?first_name=Ted&last_name=Cruz&api_key=E84890C4458AC893E4E67BD5E16DF2D1
"""
    
