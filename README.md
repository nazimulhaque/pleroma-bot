## Introduction

Some modifications to the pretty cool https://github.com/robertoszek/pleroma-bot tool in order to basically import a Twitter archive into a Pleroma server, preserving the original Tweet time.

## Features 

So basically, it does the following:
* Can parse a Twitter [archive](https://twitter.com/settings/your_twitter_data), moving all your tweets to the Fediverse
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


## Usage
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
### Before running

There are multiple options for using the bot.

You can either choose to use: 

- A Twitter archive
- An RSS feed
- Guest tokens
- [Twitter tokens](https://developer.twitter.com/en/docs/authentication/api-reference/token) with a Developer account 

You'll need to create a configuration file and obtain the [Fediverse tokens](https://tinysubversions.com/notes/mastodon-bot/) for your accounts no matter what you choose to use.

If you plan on retrieving tweets from an account which has their tweets **protected**, you'll also need the following:
* Consumer Key and Secret. You'll find them on your project app keys and tokens section at [Twitter's Developer Portal](https://developer.twitter.com/en/portal/dashboard)
* Access Token Key and Secret.  You'll also find them on your project app keys and tokens section at [Twitter's Developer Portal](https://developer.twitter.com/en/portal/dashboard). 
Alternatively, you can obtain the Access Token and Secret by running [this](https://github.com/joestump/python-oauth2/wiki/Twitter-Three-legged-OAuth-Python-3.0) locally, while being logged in with a Twitter account which follows or is the owner of the protected account

You'll may also need Elevated access in your Twitter's API project in order for the bot to function properly.

Refer to the docs [for more info about this](https://robertoszek.github.io/pleroma-bot/gettingstarted/beforerunning/#before-running).

### Configuration

Create a ```config.yml``` file in the same path where you are calling ```pleroma-bot``` (or use the `--config` argument to specify a different path). 

There's a config example in this repo called ```config.yml.sample``` that can help you when filling yours out.

For more information you can refer to the ["Configuration" page](https://robertoszek.github.io/pleroma-bot/gettingstarted/configuration/) on the docs.

Here's what a minimal config looks like:
```yaml
# Change this to your target Fediverse instance
pleroma_base_url: https://pleroma.instance
# How many tweets to gather per-user in every execution
# Twitter's API hard limit is 3,200
max_tweets: 40
# Twitter bearer token
twitter_token: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
users:
- twitter_username: User1
  pleroma_username: MyPleromaUser1
  # Mastodon/Pleroma bearer token
  pleroma_token: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### Running

If you're running the bot for the first time it will ask you for the date you wish to start retrieving tweets from (it will gather all from that date up to the present). 
If you leave it empty and just press enter it will default to the oldest date that Twitter's API allows ('```2010-11-06T00:00:00Z```') for tweet retrieval.

To force this behaviour in future runs you can use the ```--forceDate``` argument (be careful, no validation is performed with the already posted toots/posts by that Fediverse account and you can end up with duplicates posts/toots!).

Additionally, you can provide a ```twitter_username``` if you only want to force the date for one user in your config.

For example:

```console
$ pleroma-bot --forceDate WoolieWoolz
```

If the `--noProfile` argument is passed, the profile picture, banner, display name and bio will **not** be updated on the Fediverse account. However, it will still gather and post the tweets following your config's parameters.

NOTE: An ```error.log``` file will be created at the path from which ```pleroma-bot``` is being called.

### crontab entry example 
**(everyday at 6:15 AM)** update profile and **(every 10 min.)** post new tweets:
```bash
# Post tweets every 10 min
*/10 * * * * cd /home/robertoszek/myvenv/ && . bin/activate && pleroma-bot noProfile

# Update pleroma profile with Twitter info every day at 6:15 AM
15 6 * * * cd /home/robertoszek/myvenv/ && . bin/activate && pleroma-bot
```
NOTE: If you have issues with cron running the bot you may have to specify the full path of your Python executable

```*/10 * * * * /usr/bin/python /usr/local/bin/pleroma-bot```
