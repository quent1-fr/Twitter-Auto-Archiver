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

            # Get archived tweets JSON
            archivedTweets = archivedTweets.read().lstrip('window.YTD.tweet.part0 = ')

            # Parse JSON
            self.archivedTweets = json.loads(archivedTweets)

            # Generate a list of archived tweets IDs
            self.archivedTweetsIDs = self.getArchivedTweetsIDs()

    # Open tweets.js from memory
    def saveTweetsFile(self):

        # Before saving new content into file, backup it
        copyfile('tweets-archive/data/tweet.js', 'tweets-archive/data/tweet.js.backup')

        # Save updated content
        with open('tweets-archive/data/tweet.js', 'w', encoding='utf8') as archivedTweetsFile:
            print('Saving updated tweet.js file')
            archivedTweetsFile.write('window.YTD.tweet.part0 = ' + json.dumps(self.archivedTweets))

    # Extract all archived tweets IDs
    def getArchivedTweetsIDs(self):
        archivedTweetsIDs = []

        # For each archived tweet
        for archivedTweet in self.archivedTweets:
            archivedTweetsIDs.append(archivedTweet['tweet']['id_str'])

        return archivedTweetsIDs

    # Check if a tweet is archived
    def checkIfTweetIsArchived(self, tweetID):
        return tweetID in self.archivedTweetsIDs

    # Archive a tweet
    def archiveTweet(self, tweet):

        # Transform a raw tweet into an ArchivedTweet
        ArchivedTweet = ArchivedTweetEntity(tweet)

        # If tweet is already archived, skip it
        if self.checkIfTweetIsArchived(ArchivedTweet.id_str):
            print('Tweet ' + ArchivedTweet.id_str + ' is already archived, skipping it')
            return ArchivedTweet

        # Add tweet to list of archived tweets
        print('Archiving tweet ' + ArchivedTweet.id_str)
        self.archivedTweets.append({ 'tweet': ArchivedTweet.getDict() })
        self.archivedTweetsIDs.append(ArchivedTweet.id_str)

        # Force download of all media
        ArchivedTweet.downloadMedia('tweets-archive/data/tweet_media')

        return ArchivedTweet