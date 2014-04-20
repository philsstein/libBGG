#!/usr/bin/env python

import argparse
import logging
from sys import exit

from libBGG.Boardgame import Boardgame
from libBGG.BGGAPI import BGGAPI

log = logging.getLogger(__name__)

if __name__ == '__main__':
    desc = 'Query BGG for boardgames and related information.'
    ap = argparse.ArgumentParser(description=desc)
    ap.add_argument('-g', '--game', dest='game', action='append', 
                    help='Name of game. May be given multiple times.')
    ap.add_argument('-G', '--guild', dest='guild', action='append', 
                    help='ID of guild. (BGG does not support guild by name search.) '
                    ' May be given multiple times.')
    ap.add_argument("-l", "--loglevel", dest="loglevel",
                    help="The level at which to log. Must be one of "
                    "none, debug, info, warning, error, or critical. Default is info.",
                    default='none', choices=['none', 'all', 'debug', 'info', 'warning',
                                             'error', 'critical'])
    args = ap.parse_args()

    if args.game is None and args.guild is None:
        print ap.print_help()
        exit(1)

    logLevels = {
        'none': 100,
        'all': 0,
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }
    log_format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    log_datefmt = '%m-%d %H:%M:%S'
    logging.basicConfig(format=log_format, datefmt=log_datefmt,
                        level=logLevels[args.loglevel])

    bgg = BGGAPI()
    query_map = { bgg.fetch_boardgame: args.game, bgg.fetch_guild: args.guild }
    for func, queries in query_map.iteritems():
        if queries:
            for query in queries:
                item = func(query)
                if item is None:
                    print '%s: not found.' % query
                    continue

                item.dump()

        
