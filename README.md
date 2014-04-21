libBGG
======

A python interface to boardgamegeek.com. Pulls information from BGG and creates appropriate python objects for the data.

It contains three parts:
 * BGGAPI - for retriving information from BGG and parsing it into python objects
 * the boardgame objects: Boardgame, Guild, etc.
 * A caching API for writing local boardgame objects to a local sqlite3 DB.

Example usage:
--------------

```python
api = BGGAPI()

bg = api.fetch_boardgame('yinsh')
print 'Yinsh was created in %s by %s' % (bg.year, ', '.join(bg.designers))

guild = api.fetch('1920')  # BGG only supports fetch by ID.
print 'BGG Guild %s has %d members.' % (guild.name, len(guild.members))
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
