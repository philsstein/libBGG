libBGG
======

A python interface to boardgamegeek.com. Pulls information from BGG and creates appropriate python objects for the data.

It contains three parts:
 * BGGAPI - for retriving information from BGG and parsing it into python objects
 * the boardgame objects: Boardgame, Guild, etc.
 * A caching API for writing local boardgame objects to a local sqlite3 DB.

Example usage:
--------------
api = BGGAPI()

bg = api.fetch_boardgame('yinch')
bg.dump()
print 'Yinch was created in %s by %s' % (bg.year, ', '.join(bg.designers)

guild = api.fetch('1920')  # BGG only supports fetch by ID.
guild.dump()

