## Introduction

Some modifications to the pretty cool https://github.com/robertoszek/pleroma-bot tool with the primary goal to import a Twitter backup archive into a Pleroma server, preserving the original Tweet time.

## Features 

So basically, it does the following:
* Can parse a Twitter [archive](https://twitter.com/settings/your_twitter_data), moving all your tweets to the Fediverse
  * Preserving the original Tweet time.
* Can use an RSS feed as the source of the tweets to post
* Retrieves latest **tweets** and posts them on the Fediverse account if their timestamp is newer than the last post.
  * Can filter out RTs or not
  * Can filter out replies or not
  * Supports Twitter threads
* Media retrieval and upload of multiple **attachments**. This includes:
  * Video
  * Images
  * Animated GIFs 
  * Polls
* Retrieves **profile info** from Twitter and updates it in on the Fediverse account. This includes:
  * *Display name*
  * *Profile picture*
  * *Banner image*
  * *Bio text*
* Adds some **metadata fields** to the Fediverse account, pointing to the original Twitter account or custom text.

## Installation
### Using Git
```
$ git clone https://github.com/nazimulhaque/pleroma-bot.git
$ cd pleroma-bot/
```
## Test the Installation
Once installed, cd into the ```pleroma-bot``` directory (if not already done):
```
$ cd pleroma-bot/
```
Now test that the package has been correctly installed using the following command:.
```
$ python3 -m pleroma_bot.cli -h


                        `^y6gB@@BBQA{,
                      :fB@@@@@@BBBBBQgU"
                    `f@@@@@@@@BBBBQgg80H~
                    H@@B@BB@BBBB#Qgg&0RNT
                   z@@&B@BBBBBBQgg80RD6HK
                  ;@@@QB@BBBB#Qgg&0RN6WqS
                  q@@@@@BBBBQgg80RN6HAqSo          _             _
                 z@@@@BBBB#Qg8&0RN6WqSUhr         | |           | |
               -H@@@@BBBBQQg80RD6HAqSKh(       ___| |_ ___  _ __| | __
              rB@@@BBBB#6Lm00DN6WqSUhfv       / __| __/ _ \| '__| |/ /
             f@@@@BBBBf= |0RD6HAqSKhfv        \__ \ || (_) | |  |   <
           =g@@@BBBBF=  "RDN6WqSUhff{         |___/\__\___/|_|  |_|\_|
          c@@@@BBgu_   ~WD9HAqSKhfkl`
        _6@@@BBNr     'qN6WqSUhhfXI'     .                           .       .
       rB@@@B0r      `S6HAqSKhfkoCr  ,-. |  ,-. ,-. ,-. ,-,-. ,-.    |-. ,-. |-
     `X@@@BQx       `I6WASShhfXFIy_  | | |  |-' |   | | | | | ,-| -- | | | | |
    _g@@@Q\`        JHAqSKhfXoCwJz_  |-' `' `-' '   `-' ' ' ' `-^    `-' `-' `'
   rB@@#x`         }WASShhfXsIyzuu,  |
 `y@@&|          .IAqSKhfXoCwJzu1lr  '
`D@&|           :KqSUhffXsIyzuu1llc,
ff=            `==:::""",,,,________


usage: cli.py [-h] [-c CONFIG] [-l LOG] [-n] [--forceDate [FORCEDATE]] [-s]
              [-a ARCHIVE] [--verbose] [--version]

Bot for mirroring one or multiple Twitter accounts in Pleroma/Mastodon.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        path of config file (config.yml) to use and parse. If
                        not specified, it will try to find it in the current
                        working directory.
  -d, --daemon          run in daemon mode. By default it will re-run every
                        60min. You can control this with --pollrate
  -p POLLRATE, --pollrate POLLRATE
                        only applies to daemon mode. How often to run the
                        program in the background (in minutes). By default is
                        60min.
  -l LOG, --log LOG     path of log file (error.log) to create. If not
                        specified, it will try to store it at your config file
                        path
  -n, --noProfile       skips Fediverse profile update (no background image,
                        profile image, bio text, etc.)
  --forceDate [FORCEDATE]
                        forces the tweet retrieval to start from a specific
                        date. The twitter_username value (FORCEDATE) can be
                        supplied to only force it for that particular user in
                        the config
  -s, --skipChecks      skips first run checks
  -a ARCHIVE, --archive ARCHIVE
                        path of the Twitter archive file (zip) to use for
                        posting tweets.
  -t THREADS, --threads THREADS
                        number of threads to use when processing tweets
  -L LOCKFILE, --lockfile LOCKFILE
                        path of lock file (pleroma_bot.lock) to prevent
                        collisions with multiple bot instances. By default it
                        will be placed next to your config file.
  --verbose, -v
  --version             show program's version number and exit

```

### Before Running

There are multiple options for using the bot.

You can either choose to use: 

- A Twitter archive
- An RSS feed
- Guest tokens
- [Twitter tokens](https://developer.twitter.com/en/docs/authentication/api-reference/token) with a Developer account 

However, our primary concern is to restore Twitter archive data into a Pleroma social media server.
For this purpose, you'll need to create a configuration file (config.yaml) containing user and database credentials. These credentials are:

* Twitter username
* Pleroma username
* Pleroma user account access token
* Twitter archive zip file location
* Pleroma database credentials
*

Please follow the Configuration section below for details.

In order to obtain the Pleroma access token, please follow https://tools.splat.soy/pleroma-access-token link and generate access token with read write follow scopes.


### Configuration

Create a ```config.yml``` file in the same path where you are calling ```pleroma-bot```.

There's a config example in this repo called ```config.yml.nazim``` that can help you when filling yours out.

Below is what the ```config.yml``` must contain for our use case. Please replace values indicated by square brackets in your specific file.
```yaml
pleroma_base_url: [http://localhost:4000]
max_tweets: 40
users:
- twitter_username: [theNazimul]
  pleroma_username: [nazimul]
  pleroma_token: [m4FsKuHI2FhFN7qzID3WbUdWjXAKD5TIYkOK5t7PNFc]
  signature: true
  archive: [/media/sf_UbuntuVMShared/Twitter Importer/Twitter Archives/Nazim/twitter-2023-03-05-6b5f7d8cd4c2626089d70be4627bf06a0f9ad2b9d934d21cbf00e924b532ccf3.zip]
  original_date: true
  skip_pin: true
  bio_text: "\U0001F916 BEEP BOOP \U0001F916 \n I'm a bot that mirrors {{ twitter_username }} Twitter's account.\n \n "
  fields:
      - name: "\U0001F426 Birdsite"
        value: "{{ twitter_url }}"
      - name: "Status"
        value: "I am completely operational, and all my circuits are functioning perfectly."
      - name: "WWW"
        value: "{{ website }}"
```

### Running the Bot

If you're running the bot for the first time it will ask you for the date you wish to start retrieving tweets from (it will gather all from that date up to the present). 
If you leave it empty and just press enter it will default to the oldest date that Twitter's API allows ('```2010-11-06T00:00:00Z```') for tweet retrieval.

To force this behaviour in future runs you can use the ```--forceDate``` argument (be careful, no validation is performed with the already posted toots/posts by that Fediverse account and you can end up with duplicates posts/toots!).

Additionally, you can provide a ```twitter_username``` if you only want to force the date for one user in your config.


Run the bot using command:
```
$ python3 -m pleroma_bot.cli
```

It might take hours to completely restore all of your tweet, depending on the number of tweets.

## Possible Issues
You might face issues with file upload size limit. In that case, you can increase the file upload size limit in your ```pleroma/config/prod.secret.exs``` or ```pleroma/config/dev.secret.exs``` file:
```
```


## Other Usages
```console
$ pleroma-bot [-c CONFIG] [-l LOG] [--noProfile] [--daemon] [--forceDate [FORCEDATE]] [-a ARCHIVE]
```

```console
Bot for mirroring one or multiple Twitter accounts in Pleroma/Mastodon.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        path of config file (config.yml) to use and parse. If
                        not specified, it will try to find it in the current
                        working directory.
  -d, --daemon          run in daemon mode. By default it will re-run every
                        60min. You can control this with --pollrate
  -p POLLRATE, --pollrate POLLRATE
                        only applies to daemon mode. How often to run the
                        program in the background (in minutes). By default is
                        60min.
  -l LOG, --log LOG     path of log file (error.log) to create. If not
                        specified, it will try to store it at your config file
                        path
  -n, --noProfile       skips Fediverse profile update (no background image,
                        profile image, bio text, etc.)
  --forceDate [FORCEDATE]
                        forces the tweet retrieval to start from a specific
                        date. The twitter_username value (FORCEDATE) can be
                        supplied to only force it for that particular user in
                        the config
  -s, --skipChecks      skips first run checks
  -a ARCHIVE, --archive ARCHIVE
                        path of the Twitter archive file (zip) to use for
                        posting tweets.
  -t THREADS, --threads THREADS
                        number of threads to use when processing tweets
  -L LOCKFILE, --lockfile LOCKFILE
                        path of lock file (pleroma-bot.lock) to prevent
                        collisions with multiple bot instances. By default it
                        will be placed next to your config file.
  --verbose, -v
  --version             show program's version number and exit
```

