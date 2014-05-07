#!/usr/bin/env python

# Note: python 2.7
import urllib.request, urllib.error, urllib.parse
from urllib.error import  URLError
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError as ETParseError

import logging

from libBGG.Boardgame import Boardgame
from libBGG.Guild import Guild
from libBGG.User import User
from libBGG.Collection import Collection, Rating, BoardgameStatus

log = logging.getLogger(__name__)


class BGGAPIException(Exception):
    pass


class BGGAPI(object):
    '''
    BGGAPI is a class that knows how to contact BGG for information, parse out relevant details,
    the create a Python BGG object for general use.

    Example:
        api = BGGAPI()

        bg = api.fetch_boardgame('yinsh')
        print 'Yinsh was created in %s by %s' % (bg.year, ', '.join(bg.designers))

        guild = api.fetch('1920')  # BGG only supports fetch by ID.
        print 'BGG Guild %s has %d members.' % (guild.name, len(guild.members))
    '''
    def __init__(self, cache=None):
        self.root_url = 'http://www.boardgamegeek.com/xmlapi2/'
        self.cache = cache

    def _fetch_tree(self, url):
        try:
            tree = ET.parse(urllib.request.urlopen(url))
        except URLError as e:
            log.warn('error getting URL: %s' % url)
            if hasattr(e, 'reason'):
                log.warn('We failed to reach a server. Reason: %s' % e.reason)
            elif hasattr(e, 'code'):
                log.warn('The server couldn\'t fulfill the request. Error code: %d', e.code)
            # raise BGGAPIException(e)
            return None
        except ETParseError as e:
            log.critical('unable to parse BGG response to %s' % url)
            # raise BGGAPIException(e)
            return None

        return tree

    def fetch_boardgame(self, name, bgid=None, forcefetch=False):
        '''Fetch information about a bardgame from BGG by name. If bgid is given,
        it will be used instead. bgid is the ID of the game at BGG. bgid should be type str.

        BGGAPI always caches the first fetch of a game if given a cachedir. If forcefetch == True, 
        fetch_boardgame will fetch or re-fetch from BGG.'''
        if bgid is None:
            # ideally we'd search the cache by name, but that would be
            # difficult. So we just fetch it via BGG.
            log.debug('fetching boardgame by name "%s"' % name)
            url = '%ssearch?query=%s&exact=1' % (self.root_url,
                                                 urllib.parse.quote(name))
            tree = self._fetch_tree(url)
            game = tree.find("./*[@type='boardgame']")
            if game is None:
                log.warn('game not found: %s' % name)
                return None

            bgid = game.attrib['id'] if 'id' in game.attrib else None
            if not bgid:
                log.warning('BGGAPI gave us a game without an id: %s' % name)
                return None

        log.debug('fetching boardgame by BGG ID "%s"' % bgid)
        url = '%sthing?id=%s' % (self.root_url, bgid)
        if forcefetch == True or self.cache is None:
            tree = self._fetch_tree(url)
        else:
            tree = self.cache.get_bg(bgid)
            if tree is None:  # cache miss
                tree = self._fetch_tree(url)

        if tree is None:
            return None

        if self.cache is not None:
            self.cache.cache_bg(tree, bgid)

        root = tree.getroot()

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
        for xpath, bg_arg in value_map.items():
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
        for xpath, bg_arg in value_map.items():
            els = root.findall(xpath)
            if els:
                if len(els) > 0:
                    log.warn('Found multiple entries for %s, ignoring all but first' % xpath)
                kwargs[bg_arg] = els[0].text

        log.debug('creating boardgame with kwargs: %s' % kwargs)
        return Boardgame(**kwargs)

    def fetch_guild(self, gid, forcefetch=False):
        '''Fetch Guild information from BGG and populate a returned Guild object. There is
        currently no way to query BGG by guild name, it must be by ID.

        BGGAPI always caches the first fetch of a game if given a cachedir. If forcefetch == True, 
        fetch_boardgame will overwrite the existing cache if it exists.'''
        url = '%sguild?id=%s&members=1' % (self.root_url, gid)
        if forcefetch == True or self.cache is None:
            tree = self._fetch_tree(url)
        else:
            tree = self.cache.get_guild(gid)
            if tree is None:  # cache miss
                tree = self._fetch_tree(url)

        if tree is None:
            log.warn('Could not get XML for %s' % url)
            return None

        if self.cache is not None:
            self.cache.cache_guild(tree, gid)

        root = tree.getroot()

        if 'name' not in root.attrib:
            log.warn('Guild %s not yet approved. Unable to get info on it.' % gid)
            return None

        kwargs = dict()
        kwargs['name'] = root.attrib['name']
        kwargs['gid'] = gid
        kwargs['members'] = list()

        el = root.find('.//members[@count]')
        count = int(el.attrib['count'])
        total_pages = int(2+(count/25))   # 25 memebers per page according to BGGAPI
        if total_pages >= 10:
            log.warn('Need to fetch %d pages. It could take awhile.' % (total_pages-1))
        for page in range(1,total_pages):
            url = '%sguild?id=%s&members=1&page=%d' % (self.root_url, gid, page)
            if forcefetch == True or self.cache is None:
                tree = self._fetch_tree(url)
            else:
                tree = self.cache.get_guild(gid, page=page)
                if tree is None:  # cache miss
                    tree = self._fetch_tree(url)

            if tree is None:
                log.warn('Could not get XML for %s' % url)
                return None

            if self.cache is not None:
                self.cache.cache_guild(tree, gid, page=page)

            root = tree.getroot()
            log.debug('fetched guild page %d of %d' % (page, total_pages))

            for el in root.findall('.//member'):
                kwargs['members'].append(el.attrib['name'])

            if page == 1:
                # grab initial info from first page
                for tag in ['description', 'category', 'website', 'manager']:
                    el = root.find(tag)
                    if not el is None:
                        kwargs[tag] = el.text

        return Guild(**kwargs)

    def fetch_user(self, name, forcefetch=False):
        url = '%suser?name=%s&hot=1&top=1' % (self.root_url, urllib.parse.quote(name))
        if forcefetch == True or self.cache is None:
            tree = self._fetch_tree(url)
        else:
            tree = self.cache.get_user(name)
            if tree is None:  # cache miss
                tree = self._fetch_tree(url)

        if tree is None:
            log.warn('Could not get XML for %s' % url)
            return None

        if self.cache is not None:
            self.cache.cache_user(tree, name)

        root = tree.getroot()

        kwargs = dict()
        kwargs['name'] = root.attrib['name']
        kwargs['bgid'] = root.attrib['id']

        value_map = {
            './/firstname': 'firstname',
            './/lastname': 'lastname',
            './/yearregistered': 'yearregistered',
            './/stateorprovince': 'stateorprovince',
            './/country': 'country',
            './/traderating': 'traderating',
        }
        # cut and pasted from fetch_boardgame. TODO put this in separate function.
        for xpath, bg_arg in value_map.items():
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
                    log.warn('no "value" found in %s for user %s' % (xpath, name))

        for xpath, prop in {'.//top/item': 'top10', './/hot/item': 'hot10'}.items():
            els = root.findall(xpath)   # do we need to sort these by attrib='rank'? If so, how?
            for el in els:
                if not prop in kwargs:
                    kwargs[prop] = list()
                kwargs[prop].append(el.attrib['name'])

        return User(**kwargs)

    def fetch_collection(self, name, forcefetch=False):
        url = '%scollection?username=%s&stats=1' % (self.root_url, urllib.parse.quote(name))
        if forcefetch == True or self.cache is None:
            tree = self._fetch_tree(url)
        else:
            tree = self.cache.get_collection(name)
            if tree is None:  # cache miss
                tree = self._fetch_tree(url)

        if tree is None:
            log.warn('Could not get XML for %s' % url)
            return None

        if self.cache is not None:
            self.cache.cache_collection(tree, name)

        root = tree.getroot()
        collection = Collection(name)

        # build up the games, status, and rating and add to collection.
        els = root.findall('.//item[@subtype="boardgame"]')
        log.debug('Found %s games in %s\'s collection.' % (len(els), name))
        for el in els:
            stats = el.find('stats')
            rating = stats.find('rating')
            status = el.find('status')

            kwargs = dict()
            bgname = el.find('name').text
            kwargs['names'] = bgname
            bgid = el.attrib['objectid']
            kwargs['bgid'] = bgid
            subel = el.find('yearpublished')
            kwargs['year'] = subel.text if not subel is None else None
            subel = el.find('image')
            kwargs['image'] = subel.text if not subel is None else None
            subel = el.find('thumbnail')
            kwargs['thumbnail'] = subel.text if not subel is None else None

            for attr in ['minplayers', 'maxplayers', 'playingtime']:
                kwargs[attr] = stats.attrib[attr] if attr in stats.attrib else ''
            collection.games.append(Boardgame(**kwargs))
           
            kwargs = dict()
            # this only works as BoardgameStatus.__slots__ matches most of the XML attributes
            # exactly. i.e. this is probably bad idea.
            for prop in BoardgameStatus.__slots__:
                kwargs[prop] = status.attrib[prop] if prop in status.attrib else ''
            kwargs['numplays'] = el.find('numplays').text
            kwargs['name'] = bgname
            kwargs['bgid'] = bgid
            collection.status[bgname] = BoardgameStatus(**kwargs)

            kwargs = dict()
            kwargs['name'] = bgname
            kwargs['bgid'] = bgid
            if 'value' in rating.attrib and rating.attrib['value'] != 'N/A':
                kwargs['userrating'] = rating.attrib['value']
            else:
                kwargs['userrating'] = None

            for prop in Rating.__slots__:
                rate_el = rating.find(prop)
                if not rate_el is None:
                    kwargs[prop] = rate_el.attrib['value'] if 'value' in rate_el.attrib else ''

            kwargs['BGGrank'] = rating.find('ranks/rank[@name="boardgame"]').attrib['value']
            log.debug('%s ranked %s by BGG - rated %s by %s' % (
                bgname, kwargs['BGGrank'], kwargs['userrating'], name))
            log.debug('Creating Rating with: %s' % kwargs)
            collection.rating[bgid] = Rating(**kwargs)

        return collection
