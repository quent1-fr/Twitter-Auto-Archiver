# Twitter Auto Archiver

A Python 3 script that allows you to : 

1. Find your tweets older than a certain age (within the limit of the 3,200 most recent ones)
2. Archive them, by placing them correctly in your Twitter archive
3. Delete them forever

It also takes care of deleting old likes, without archiving them.

## Installation

    pip -r requirements.txt

## Configuration

All the configuration is done in the `config.json` file at the root of the project (see `config.json.sample` for more information).

You have to create a new Twitter application [here](https://developer.twitter.com/en/portal/dashboard).

## Usage

Add your unzipped [Twitter archive](https://twitter.com/settings/your_twitter_data) to the root of the project, renaming it `tweets-archive`.

Run the script :

    python main.py 

# Questions

## Is it 100% reliable?

Nope, just a dirty hack done on my free time that does the bare minimum to fetch tweets then archive them in a format that seems to be readable by the native Twitter tools (without completely mimic it).

I don't even really learned Python. You'll be warned. 

## Is anyone using it on a daily basis?

Yep, me (at least).

## Does it save media content?

Yes, at least for photos, videos and animated GIFs. 

## I found a bug, what can I do?

Open a new Github issue with as many details as you can. 