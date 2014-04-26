import os
import os.path
import logging
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError as ETParseError

log = logging.getLogger(__name__)


class BGGCacheException(Exception):
    pass


class BGGCache(object):
    '''Cache and/or retrieve the given XML representations of BGG objects.'''
    def __init__(self, cachedir):
        self.cachedir = cachedir
        self.bgdir = os.path.join(self.cachedir, 'boardgames')
        self.collectiondir = os.path.join(self.cachedir, 'collections')
        self.userdir = os.path.join(self.cachedir, 'users')
        self.guilddir = os.path.join(self.cachedir, 'guilds')

        for d in [self.cachedir, self.guilddir, self.bgdir, self.collectiondir, self.userdir]:
            if not os.path.isdir(d):
                os.mkdir(d)

    def cache_bg(self, tree, bgid):
        self._cache_tree(tree, os.path.join(self.bgdir, '%s.xml' % bgid))

    def get_bg(self, bgid):
        return self._get_tree(os.path.join(self.bgdir, '%s.xml' % bgid))

    def bg_exists(self, bgid):
        return os.path.exists(os.path.join(self.bgdir, '%s.xml' % bgid))

    def cache_guild(self, tree, gid, page=1):
        self._cache_tree(tree, os.path.join(self.guilddir, '%s-%d.xml' % (gid, page)))

    def get_guild(self, gid, page=1):
        return self._get_tree(os.path.join(self.guilddir, '%s-%d.xml' % (gid, page)))

    def guild_exists(self, gid):
        return os.path.exists(os.path.join(self.guilddir, '%s-1.xml' % gid))

    def cache_user(self, tree, name):
        self._cache_tree(tree, os.path.join(self.userdir, '%s.xml' % name))

    def get_user(self, user):
        return self._get_tree(os.path.join(self.userdir, '%s.xml' % user))

    def user_exists(self, name):
        return os.path.exists(os.path.join(self.userdir, '%s.xml' % name))

    def cache_collection(self, tree, user):
        self._cache_tree(tree, os.path.join(self.collectiondir, '%s.xml' % user))

    def get_collection(self, user):
        return self._get_tree(os.path.join(self.collectiondir, '%s.xml' % user))

    def collection_exists(self, user):
        return os.path.exists(os.path.join(self.collectiondir, '%s.xml' % user))

    def _cache_tree(self, tree, filename):
        tree.write(filename)

    def _get_tree(self, path):
        if not os.path.exists(path):
            return None
        try:
            return ET.parse(path)
        except ETParseError:
            log.critical('unable to parse file %s' % path)
            # raise BGGCacheException(e)
            return None

