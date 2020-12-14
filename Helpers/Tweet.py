# Common tools for tweet manipulation

import datetime

class TweetHelper:

    # Convert a tweet datetime to a Python datetime
    def tweetDateTimeToPythonDateTime( tweetDateTime):
        return datetime.datetime.strptime(tweetDateTime, '%a %b %d %H:%M:%S %z %Y')
