import urllib
import os.path

class ArchivedTweetEntity:

    # Create a new archived tweet entity
    def __init__(self, rawTweet):

        # Is always false (even when it is indeed a retweet)
        self.retweeted = False

        # Consider tweet as never sensitive (information is not retrieved and is not that important)
        self.possibly_sensitive = False

        # Tweet ID
        self.id = rawTweet.id_str # Dirty fix for int format problem
        self.id_str = rawTweet.id_str

        # Tweet data retrieved from API
        self.created_at = rawTweet.created_at
        self.source = rawTweet.source
        self.favorite_count = rawTweet.favorite_count
        self.retweet_count = rawTweet.retweet_count
        self.favorited = rawTweet.favorited

        # Tweet content
        self.truncated = rawTweet.truncated

        # If tweet is retweeted, full text is available on original tweet only
        if rawTweet.retweeted:
            self.full_text = 'RT @' + self.getUserScreenNameById(list(map(self.formatUserMention, rawTweet.user_mentions)), rawTweet.retweeted_status.user.id) + ': ' + rawTweet.retweeted_status.full_text
        else:
            self.full_text = rawTweet.full_text

        self.lang = rawTweet.lang
        self.display_text_range = [ 0, len(self.full_text) ]

        # Tweet entities
        self.entities = {
            'user_mentions': list(map(self.formatUserMention, rawTweet.user_mentions)),
            'urls': list(map(self.formatURL, rawTweet.urls)),
            'symbols': [], # No data provided by the API for that
            'media': [],
            'hashtags': list(map(self.formatHashtag, rawTweet.hashtags))
        }

        # If tweet has media
        if rawTweet.media != None:
            self.entities['media'] = list(map(self.formatMedia, rawTweet.media))

        # Tweet extended entities
        self.extended_entities = {
            'media': self.entities['media']
        }


    # Format an user mention
    def formatUserMention(self, User):
        return User._json

    # Format an url
    def formatURL(self, URL):
        return URL._json

    # Format a media
    def formatMedia(self, Media):

        # For each supported type
        if Media.type == 'photo':
            return self.formatPhoto(Media)

        if Media.type == 'video':
            return self.formatVideo(Media)

        if Media.type == 'animated_gif':
            return self.formatAnimatedGif(Media)

    # Format a photo type media
    def formatPhoto(self, Photo):
        return Photo._json

    # Format a video type media
    def formatVideo(self, Video):
        videoDict = Video._json

        # Bitrate should be a string
        videoDict['video_info']['variants'] = self.stringifyVariantsBitrates(videoDict['video_info']['variants'])

        return videoDict

    # Format an animated gif type media
    def formatAnimatedGif(self, AnimatedGif):
        animatedGifDict = AnimatedGif._json

        # Bitrate should be a string
        animatedGifDict['video_info']['variants'] = self.stringifyVariantsBitrates(animatedGifDict['video_info']['variants'])

        return animatedGifDict

    # Format a hashtag
    def formatHashtag(self, Hashtag):
        return Hashtag._json

    # Return an user screen name by user id
    def getUserScreenNameById(self, users, userId):
        for user in users:
            if user['id'] == userId:
                return user['screen_name']

        return '<not_found>'

    # Return the entity as a dictionary
    def getDict(self):
        return vars(self)

    # Convert int bitrates into string bitrates for variants
    def stringifyVariantsBitrates(self, variants):

        # Count variants
        variantsCount = len(variants)

        # If there is no variants
        if variantsCount < 1:
            return []

        # For each variant
        for i in range (0, variantsCount):

            # If there is a bitrate
            if 'bitrate' in variants[i]:
                variants[i]['bitrate'] = str(variants[i]['bitrate'])

        return variants


    # Save all media from tweet
    def downloadMedia(self, mediaPath):

        # For each tweet media
        for media in self.extended_entities['media']:

            # Find media URL
            mediaURL = None
            if media['type'] == 'photo':
                mediaURL = media['media_url_https']

            elif media['type'] == 'animated_gif' or media['type'] == 'video':
                mediaBestVariant = self.getBestVariantAvailable('video/mp4', media['video_info']['variants'])

                # Ignore media if there is no variant
                if mediaBestVariant is None:
                    continue

                mediaURL = mediaBestVariant['url']

            # Generate media file name
            mediaFileName = self.id_str + '-' + os.path.basename(urllib.parse.urlsplit(mediaURL).path)

            # Download the media
            print('Downloading media ' + mediaFileName + ' (' + mediaURL + ')')
            urllib.request.urlretrieve(mediaURL, mediaPath + '/' + mediaFileName)

    # Get best available variant of a media by mimetype
    def getBestVariantAvailable(self, mimeType, variants):
        bestVariant = None

        for variant in variants:
            if variant['content_type'] == mimeType and (bestVariant is None or int(bestVariant['bitrate']) < int(variant['bitrate'])):
                bestVariant = variant

        return bestVariant

