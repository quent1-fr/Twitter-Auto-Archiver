# Interact with Twitter API

import twitter

from Helpers.Tweet import TweetHelper

class TwitterAPIHelper:

    # Constructor
    def __init__(self, apiKey, apiSecret, consumerKey, consumerSecret):

        # Internal parameters
        self.tweetsPerAPICall = 50
        self.likesPerAPICall = 200

        # Save constructor parameters
        self.settings = {
            'app': {
                'key': apiKey,
                'secret': apiSecret
            },
            'account': {
                'key': consumerKey,
                'secret': consumerSecret
            }
        }

        # Open connection
        self.connect()

    # Establish connection with the API
    def connect(self):
        self.TwitterAPIConnectionInstance = twitter.Api(
            consumer_key=self.settings['app']['key'],
            consumer_secret=self.settings['app']['secret'],
            access_token_key=self.settings['account']['key'],
            access_token_secret=self.settings['account']['secret'],
            tweet_mode='extended'
        )

    # Get complete tweets older than a certain age
    def getTweets(self, notAfterDateTime):
        formattedTweets = []
        maxTweetId = None

        # While there is new tweets to get
        while True:

            # Get some more tweets
            rawTweets = self.TwitterAPIConnectionInstance.GetUserTimeline(max_id = maxTweetId, include_rts = True, exclude_replies = False, count = self.tweetsPerAPICall)

            # If there is no tweets, stop here
            if (maxTweetId is None and len(rawTweets) < 1) or (maxTweetId is not None and len(rawTweets) < 2):
                break

            # Our targeted tweets ids
            targetedTweetsIds = []

            # For each tweet found
            for tweet in rawTweets:

                # Update latest read tweet
                maxTweetId = tweet.id_str

                # If tweet is too new, ignore it
                if TweetHelper.tweetDateTimeToPythonDateTime(tweet.created_at) > notAfterDateTime:
                    continue

                # Save tweet id
                targetedTweetsIds.append(tweet.id_str)

            # Get tweet details
            formattedTweets = formattedTweets + self.getTweetsDetails(targetedTweetsIds)

        return formattedTweets

    # Get details for tweets by ids and feed an existing array
    def getTweetsDetails(self, targetedTweetsIds):

        # If we have tweets to get
        if len(targetedTweetsIds) > 0:
            return self.TwitterAPIConnectionInstance.GetStatuses(targetedTweetsIds, trim_user = True, include_entities = True, map = False)

        return []

    # Delete likes older than a certain age
    # @FIXME max_id don't seem to work here, so we don't loop
    def deleteLikes(self, notAfterDateTime):

        # Get as many likes as possible
        rawLikes = self.TwitterAPIConnectionInstance.GetFavorites(count=self.likesPerAPICall)

        # For each like found
        for like in rawLikes:

            # If like is too young, ignore it
            if TweetHelper.tweetDateTimeToPythonDateTime(like.created_at) > notAfterDateTime:
                continue

            # Delete the like
            self.deleteLike(like.id_str)

    # Delete a tweet
    def deleteTweet(self, tweetId):
        try:
            print('Deleting tweet ' + tweetId)
            return self.TwitterAPIConnectionInstance.DestroyStatus(tweetId)

        except twitter.error.TwitterError:
            print('Cannot delete tweet ' + tweetId)
            return False

    # Delete a like
    def deleteLike(self, likeId):
        try:
            print('Unliking tweet ' + likeId)
            return self.TwitterAPIConnectionInstance.DestroyFavorite(status_id = likeId)

        except twitter.error.TwitterError:
            print('Cannot unlike tweet ' + likeId)
            return False