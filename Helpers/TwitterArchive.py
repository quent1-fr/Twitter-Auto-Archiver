# Read and write into the Twitter archive

import json

from shutil import copyfile

from Helpers.Tweet import TweetHelper
from Entities.ArchivedTweet import ArchivedTweetEntity

class TwitterArchiveHelper:

    # Constructor
    def __init__(self):

        # Open archives JSON files
        self.openTweetsFile()

    # Open tweets.js into memory
    def openTweetsFile(self):

        with open('tweets-archive/data/tweet.js', encoding='utf8') as archivedTweets:
            print('Opening tweet.js file')
            archivedTweets = archivedTweets.read().lstrip('window.YTD.tweet.part0 = ')
            self.archivedTweets = json.loads(archivedTweets)

    # Open tweets.js from memory
    def saveTweetsFile(self):

        # Before saving new content into file, backup it
        copyfile('tweets-archive/data/tweet.js', 'tweets-archive/data/tweet.js.backup')

        # Save updated content
        with open('tweets-archive/data/tweet.js', 'w', encoding='utf8') as archivedTweetsFile:
            print('Saving updated tweet.js file')
            archivedTweetsFile.write('window.YTD.tweet.part0 = ' + json.dumps(self.archivedTweets))

    # Get newest archived tweet ID
    def getNewestArchivedTweetID(self):
        targetedTweetID = None
        targetedTweetDate = None

        # For each archived tweet
        for archivedTweet in self.archivedTweets:

            # Check if it is more recent than the current one
            archivedTweetDateTime = TweetHelper.tweetDateTimeToPythonDateTime(archivedTweet['tweet']['created_at'])
            if targetedTweetDate == None or archivedTweetDateTime > targetedTweetDate:
                targetedTweetID = archivedTweet['tweet']['id_str']
                targetedTweetDate = archivedTweetDateTime

        return targetedTweetID

    # Archive a tweet
    def archiveTweet(self, tweet):

        # Transform a raw tweet into an ArchivedTweet
        ArchivedTweet = ArchivedTweetEntity(tweet)

        # Add tweet to list of archived tweets
        print('Archiving tweet ' + ArchivedTweet.id_str)
        self.archivedTweets.append({ 'tweet': ArchivedTweet.getDict() })

        # Force download of all media
        ArchivedTweet.downloadMedia('tweets-archive/data/tweet_media')

        return ArchivedTweet