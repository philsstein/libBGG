libBGG
======

A python interface to boardgamegeek.com. Pulls information from BGG and creates appropriate python objects for the data.

Supports Python 3

It contains three two parts:
 * BGGAPI - for retriving information from BGG and parsing it into python objects
 * the boardgame objects: Boardgame, Guild, etc.
 * A caching API for writing local boardgame objects to a filesystem.

Example usage:
--------------

```python
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
```

```
usage: bgg_query [-h] [-g GAME] [-G GUILD] [-u USER]
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
  -l {none,all,debug,info,warning,error,critical}, --loglevel {none,all,debug,info,warning,error,critical}
                        The level at which to log. Must be one of none, debug,
                        info, warning, error, or critical. Default is none.
                        (This is mostly used for debugging.)
```

```
glawler@Willow:~/src/libBGG> ./bin/bgg_query.py --game yinsh --guild 1291
Guild r/boardgames:
    bggid: 1291
    members: caitlinsquared, DistinctlyBenign, jdclewis, magdalencox, Schnubby, zetaceti
    name: r/boardgames
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
glawler@Willow:~/src/libBGG>
```

Now, with collections. (Yes, there is a BGG user named "yinsh". 

```
glawler@glory:~/src/libBGG]$ ./bin/bgg_query --user yinsh --collection yinsh --game yinsh
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
```

Version history
---------------
0.1.2 - bin/top_rated works. added local filesystem caching.
0.1.1 - data caching added
0.1.0 - inital checkin
