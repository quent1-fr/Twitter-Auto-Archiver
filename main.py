import locale

from Helpers.Settings import SettingsHelper
from Helpers.TwitterAPI import TwitterAPIHelper
from Helpers.TwitterArchive import TwitterArchiveHelper

if __name__ == '__main__':

    # Set locale to en_us
    locale.setlocale(locale.LC_ALL, 'en_US')

    # Open settings
    SettingsInstance = SettingsHelper()
    settings = SettingsInstance.getAll()

    # Open Twitter API
    TwitterAPIInstance = TwitterAPIHelper(
        apiKey=settings['app']['api-key'],
        apiSecret=settings['app']['api-secret'],
        consumerKey=settings['account']['access-token'],
        consumerSecret=settings['account']['access-token-secret']
    )

    # Open Twitter Archive
    TwitterArchiveInstance = TwitterArchiveHelper()

    # Get most recent archived tweet ID
    getNewestArchivedTweetID = TwitterArchiveInstance.getNewestArchivedTweetID()

    # Read tweets to archive
    tweetsToArchive = TwitterAPIInstance.getTweets(SettingsInstance.parseDate(settings['tweets']['maximum-age']), getNewestArchivedTweetID)

    # Tweets to delete
    tweetsToDelete = []

    # For each tweet to archive
    for tweetToArchive in tweetsToArchive:

        # Archive the tweet
        ArchivedTweet = TwitterArchiveInstance.archiveTweet(tweetToArchive)

        # Save the ID for deletion
        tweetsToDelete.append(ArchivedTweet.id_str)

    # Save updated Twitter archive
    TwitterArchiveInstance.saveTweetsFile()

    # Once our archive has been saved, start deleting old tweets
    for tweetToDelete in tweetsToDelete:
        TwitterAPIInstance.deleteTweet(tweetToDelete)

    # Delete likes that are too old
    TwitterAPIInstance.deleteLikes(SettingsInstance.parseDate(settings['likes']['maximum-age']))