#!/usr/bin/env python

import argparse
import logging

from libBGG.Boardgame import Boardgame
from libBGG.BGGAPI import BGGAPI

logging.basicConfig(level=logging.CRITICAL)
log = logging.getLogger(__name__)

if __name__ == '__main__':
    desc = 'Query BGG for boardgames and related information.'
    ap = argparse.ArgumentParser(description=desc)
    ap.add_argument('-g', '--game', dest='game', action='append', 
                    help='Name of game. May be given multiple times.')
    args = ap.parse_args()

    bgg = BGGAPI()
    for name in args.game:
        game = bgg.fetch_boardgame(name)
        if game is None:
            print '%s: not found.' % name
            continue

        game.dump()

        
