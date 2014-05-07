import logging

from libBGG.PropertiedObject import PropertiedObject

log = logging.getLogger(__name__)


class CollectionException(Exception):
    '''Exception wrapper for Collection specific exceptions.'''
    pass


class Rating(object):
    __slots__ = ['name', 'bgid', 'userrating', 'usersrated', 'average', 'stddev',
                 'bayesaverage', 'BGGrank', 'median']

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def dump(self):
        log.debug('%s rating' % self.name)
        for a in Rating.__slots__:
            log.debug('\t%s: %s' % (a, getattr(self, a)))


class BoardgameStatus(PropertiedObject):
    __slots__ = ['name', 'bgid', 'own', 'prevown', 'fortrade', 'want', 'wanttoplay',
                 'wanttobuy', 'wishlist', 'wishlistpriority', 'timestamp', 'numplays']

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def dump(self):
        log.debug('%s rating' % self.name)
        for a in BoardgameStatus.__slots__:
            if getattr(self, a, None):
                log.debug('\t%s: %s' % (a, getattr(self, a)))



class Collection(object):
    '''
    Store information about a Collection. The init function takes a list of valid
    proprties defined by Collection.valid_properties. Properties that are lists can
    be given as a single item or as a list.

    The Collection class contains a list of minimally filled out Boardgames as
    well as a rating map for those games. Each rating contains # users rated, 
    average, stddev, median, BGG Boardgame rank, etc as well as the User's rating if given.

    Ratings are mapped by boardgame name.
    '''
    def __init__(self, user):
        self.user = user
        self.games = list()
        self.rating = dict()   # index is BG name
        self.status = dict()   # index is BG name

    def __unicode__(self):
        return '%s collection %d items' % (self.user, len(self.games))

    def __str__(self):
        return self.__unicode__().encode('utf-8').strip()

    def dump(self):
        # note the , at the end of the print statements (no new lines)
        log.debug('%s\'s collection has %s games:' % (self.user, len(self.games)))
        for game in self.games:
            name = game.name
            if self.rating[game.bgid].userrating:
                rating = ' rated: %s' % self.rating[game.bgid].userrating
            else:
                rating = ''
            log.debug('%s (%s)%s,' % (game.name, game.year, rating))

    @property
    def len(self):
        return len(self.games)
