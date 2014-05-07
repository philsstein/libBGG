libBGG
======

A python interface to boardgamegeek.com. Pulls information from BGG and
creates appropriate python objects for the data.

Supports Python 3

It contains three parts:
 * BGGAPI - for retriving information from BGG and parsing it into python objects
 * the boardgame objects: Boardgame, Guild, etc.
 * A caching API for writing retrieved XML queries to the local filesystem.

Example python usage:
--------------------------------
> from libBGG.BGGAPI import BGGAPI
> api = BGGAPI()

> bg = api.fetch_boardgame('YINSH')
> print 'Yinsh was created in %s by %s' % (bg.year, ', '.join(bg.designers))
Yinsh was created in 2003 by Kris Burm

> guild = api.fetch_guild('1920')  # BGG only supports guild fetch by ID.
> print 'BGG Guild %s has %d members.' % (guild.name, len(guild.members))
BGG Guild "Paradox" has 2 members.

> collection = api.fetch_collection('philsstein')
> print 'philsstein rated yinsh: %s out of 10' % collection.rating['YINSH'].userrating
philsstein rated yinsh: 8 out of 10
---------------------------------

There are a few example scripts included that use libBGG: "bgg_query", which queries BGG
and dumps the information it finds and "top_rated", which takes a Guild ID 
and dumps the top rated games and ratings of members of the guild. 

Usage:
--------------------------------
$ ./bin/top_rated --help
usage: top_rated [-h] [-g GUILD] [-n NUMBER] [-C CACHE] [-f] [-H HTMLOUT]
                 [-w WIKIOUT]
                 [-l {none,all,debug,info,warning,error,critical}]

Show top ratings for a given guild.

optional arguments:
  -h, --help            show this help message and exit
  -g GUILD, --guild GUILD
                        ID of guild. (bgg does not support guild by name
                        search.
  -n NUMBER, --number NUMBER
                        How many games to show. (Default=100)
  -C CACHE, --cache CACHE
                        Path to cache. If given look in cache first, then
                        fetch from BGG. Otherwise always fetch from BGG.
                        collection. If --forcefetch is given, force a fetch
                        into the cache.
  -f, --forcefetch      If given, force a refetch of any data. This argument
                        does nothing if a cache is not given.
  -H HTMLOUT, --htmlout HTMLOUT
                        If given, write an HTML table of the data to the given
                        file.
  -w WIKIOUT, --wikiout WIKIOUT
                        If given, write a wiki formatted version of the data
                        to the given file.
  -l {none,all,debug,info,warning,error,critical}, --loglevel {none,all,debug,info,warning,error,critical}
                        The level at which to log. Must be one of none, debug,
                        info, warning, error, or critical. Default is none.
                        (This is mostly used for debugging.)

$ ./bin/bgg_query --help
usage: bgg_query [-h] [-g GAME] [-G GUILD] [-u USER] [-c COLLECTION]
                 [-C CACHE] [-f]
                 [-l {none,all,debug,info,warning,error,critical}]

Query BGG for boardgames and related information. All arguments may be given
and given multiple times.

optional arguments:
  -h, --help            show this help message and exit
  -g GAME, --game GAME  Name of game.
  -G GUILD, --guild GUILD
                        ID of guild. (bgg does not support guild by name
                        search.
  -u USER, --user USER  Name of BGG user.
  -c COLLECTION, --collection COLLECTION
                        User's collection
  -C CACHE, --cache CACHE
                        Path to cache. If given look in cache first, then
                        fetch from BGG. Otherwise always fetch from BGG.
                        collection. If --forcefetch is given, force a fetch
                        into the cache.
  -f, --forcefetch      If given, force a refetch of any data. This argument
                        does nothing if a cache is not given.
  -l {none,all,debug,info,warning,error,critical}, --loglevel {none,all,debug,info,warning,error,critical}
                        The level at which to log. Must be one of none, debug,
                        info, warning, error, or critical. Default is none.
                        (This is mostly used for debugging.)

Script sample runs:
-------------------------
# Yes, there is a "yinsh" user at BGG. 
$ ./bin/bgg_query --user yinsh --collection yinsh --game yinsh
yinsh's collection has 2 games: Monopoly: Deluxe Edition (1995) rated: 5, Scrabble (1948) rated: 6,
yinsh:
    bggid: 83873
    country: Malaysia
    firstname: Yin
    hot10: 
    lastname: Swee Heng
    name: yinsh
    top10: 
    traderating: 0
    yearregistered: 2006
YINSH:
    artists: lu'cifer
    bgid: 7854
    categories: Abstract Strategy
    designers: Kris Burm
    families: Mensa Select, Project GIPF
    maxplayers: 2
    mechanics: Grid Movement, Pattern Building
    minplayers: 2
    names: YINSH
    playingtime: 30
    publishers: Don & Co., Rio Grande Games, Smart Toys and Games, Inc.
    year: 2003

$ ./bin/bgg_query.py --guild 1291
Guild r/boardgames:
    bggid: 1291
    members: caitlinsquared, DistinctlyBenign, jdclewis, magdalencox, Schnubby, zetaceti
    name: r/boardgames

$ ./bin/bgg_query -g qwirkle -g notexists -g "Prêt-à-Porter"
Qwirkle:
    artists: b''
    bgid: b'25669'
    categories: b'Abstract Strategy'
    designers: b'Susan McKinley Ross'
    families: b'Mensa Select, Qwirkle'
    maxplayers: b'4'
    mechanics: b'Hand Management, Pattern Building, Tile Placement'
    minplayers: b'2'
    names: b'Qwirkle, Qwirkle \xc3\xa9dition voyage, Qwirkle Travel, \xed\x81\x90\xec\x9c\x84\xed\x81\xb4'
    playingtime: b'45'
    publishers: b'MindWare, 999 Games, ADC Blackfire Entertainment, Compaya.hu - Gamer Caf\xc3\xa9 Kft., Competo / Marektoy, Corfix, cutia.ro, \xc3\x89veil & Jeux, G3, Green Board Game Co., IELLO, Outset Media, Productief BV, Schmidt Spiele'
    year: b'2006'
notexists: not found. No connection or not in cache if given.
Prêt-à-Porter:
    artists: b'Mariusz Gandzel, Tomasz Jedruszek, Micha\xc5\x82 Oracz, Darek Zabrocki'
    bgid: b'87890'
    categories: b'Economic, Industry / Manufacturing'
    designers: b'Piotr Haraszczak, Ignacy Trzewiczek'
    families: b''
    maxplayers: b'4'
    mechanics: b'Card Drafting, Set Collection, Worker Placement'
    minplayers: b'2'
    names: b'Pr\xc3\xaat-\xc3\xa0-Porter'
    playingtime: b'90'
    publishers: b'Portal Games'
    year: b'2010'

$ ./bin/top_rated -C ~/bgg_cache -g 1291 -n 15
Fetched member information for guild "r/boardgames"
Fetching 6 member collections.......Fetched 6 collections totalling 1083 games and 1062 ratings.
Computing ratings...

Ratings for guild r/boardgames:
===============================
Rank Rating Rated Stddev Name
---- ------ ----- ------ ----
  1.  10.00     1   0.00 Kemet
  2.  10.00     1   0.00 Dune
  3.  10.00     1   0.00 Survive: Escape from Atlantis!
  4.  10.00     1   0.00 Galaxy Trucker: Anniversary Edition
  5.  10.00     1   0.00 Rex: Final Days of an Empire
  6.  10.00     1   0.00 Discworld: Ankh-Morpork
  7.  10.00     1   0.00 The Great Zimbabwe
  8.  10.00     1   0.00 Theseus: The Dark Orbit
  9.  10.00     1   0.00 Dice Town
 10.   9.50     1   0.00 Chicago Express
 11.   9.00     1   0.00 Glory to Rome
 12.   9.00     1   0.00 Terra Mystica
 13.   9.00     1   0.00 Coloretto
 14.   9.00     1   0.00 Hansa Teutonica
 15.   9.00     1   0.00 London
Computed at: Mon Apr 28 17:45:22 2014
Using 1062 ratings from 6 guild members.


Version history
---------------
0.1.3 - Reduced memory footprint. 
0.1.2 - bin/top_rated works. added local filesystem caching.
0.1.1 - data caching added
0.1.0 - inital checkin
