#!/usr/bin/env python

# Note: python 2.7
import urllib2
import xml.etree.ElementTree as ET
import logging

from libBGG.Boardgame import Boardgame

log = logging.getLogger(__name__)

class BGGAPI(object):

    def __init__(self):
        self.root_url = 'http://www.boardgamegeek.com/xmlapi2/'

    def fetch_boardgame(self, name):
        log.info('fetching boardgame %s' % name)
        url = '%ssearch?query=%s&exact=1' % (self.root_url,
                                              urllib2.quote(name))
        tree = ET.parse(urllib2.urlopen(url))
        game = tree.find("./*[@type='boardgame']")
        if game is None:
            log.warn('game not found: %s' % name)
            return None

        bgid = game.attrib['id'] if 'id' in game.attrib else None
        if not bgid:
            log.warning('BGGAPI gave us a game without an id: %s' % name)
            return None

        url = '%sthing?id=%s' % (self.root_url, bgid)
        tree = ET.parse(urllib2.urlopen(url))
        root = tree.getroot()
        game = tree.find("./*[@id='%s']" % bgid)

        kwargs = dict()
        kwargs['bgid'] = bgid
        # entries that use attrib['value']. 
        value_map = {
            './/yearpublished': 'year',
            './/minplayers': 'minplayers',
            './/maxplayers': 'maxplayers',
            './/playingtime': 'playingtime',
            './/name': 'names',
            ".//link[@type='boardgamefamily']": 'families',
            ".//link[@type='boardgamecategory']": 'categories',
            ".//link[@type='boardgamemechanic']": 'mechanics',
            ".//link[@type='boardgamedesigner']": 'designers',
            ".//link[@type='boardgameartist']": 'artists',
            ".//link[@type='boardgamepublisher']": 'publishers',
            ".//link[@type='boardgamecategory']": 'categories',
        }
        for xpath, bg_arg in value_map.iteritems():
            els = root.findall(xpath)
            for el in els:
                if 'value' in el.attrib:
                    if bg_arg in kwargs:
                        # multiple entries, make this arg a list.
                        if type(kwargs[bg_arg]) != list:
                            kwargs[bg_arg] = [kwargs[bg_arg]]
                        kwargs[bg_arg].append(el.attrib['value'])
                    else:
                        kwargs[bg_arg] = el.attrib['value']
                else:
                    log.warn('no "value" found in %s for game %s' % (xpath, name))

        # entries that use text instead of attrib['value']
        value_map = {
            './thumbnail': 'thumbnail',
            './image': 'image',
            './description': 'description'
        }
        for xpath, bg_arg in value_map.iteritems():
            els = root.findall(xpath)
            if els:
                if len(els) > 0:
                    log.warn('Found multiple entries for %s, ignoring all but first' % xpath)
                kwargs[bg_arg] = els[0].text

        log.debug('creating boardgame with kwargs: %s' % kwargs)
        return Boardgame(**kwargs)

if __name__ == '__main__':
    # test.
    from sys import exit, argv
    logging.basicConfig(level=logging.DEBUG)
    api = BGGAPI()
    name = 'yinsh' if len(argv) <= 1 else argv[1]
    bg = api.fetch_boardgame(name)
    if bg is None:
        log.critical('%s: not found' % name)
        exit(1)

    print bg
    exit(0)
