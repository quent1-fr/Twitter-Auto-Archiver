# Read the settings for this script

import json
import dateparser

class SettingsHelper():

    # Constructor
    def __init__(self):

        # Open the config.json file and load data into memory
        with open('config.json') as settingsFile:
            self.settings = json.load(settingsFile)

    # Get settings
    def getAll(self):
        return self.settings

    # Parse date
    def parseDate(self, date):
        return dateparser.parse(date, settings = {
            'TIMEZONE': 'UTC',
            'RETURN_AS_TIMEZONE_AWARE': True
        })