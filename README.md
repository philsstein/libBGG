libBGG
======

A python interface to boardgamegeek.com. Pulls information from BGG and creates appropriate python objects for the data.
libBGG is a python module that used teh boardgamegeek API to retrieve boardgame information from BGG and create python objects out of it. 

It contains three parts:
 * BGGAPI - for retriving information from BGG and parsing it into python objects
 * the boardgame objects: Boardgame, Guild, etc.
 * A caching API for writing local boardgame objects to a local sqlite3 DB.


