import logging

from libBGG.PropertiedObject import PropertiedObject

log = logging.getLogger(__name__)


class CollectionException(Exception):
    '''Exception wrapper for Collection specific exceptions.'''
    pass


class Rating(PropertiedObject):
    valid_properties = ['name', 'bgid', 'userrating', 'usersrated', 'average', 'stddev',
                        'bayesaverage', 'BGGrank', 'median']
    def __init__(self, **kwargs):
        self.valid_properties = Rating.valid_properties
        super(Rating, self).__init__(**kwargs)

    def dump(self):
        super(Rating, self).dump('%s rating' % self.name)


class BoardgameStatus(PropertiedObject):
    valid_properties = ['name', 'bgid', 'own', 'prevown', 'fortrade', 'want', 'wanttoplay',
                        'wanttobuy', 'wishlist', 'wishlistpriority', 'timestamp', 'numplays']
    def __init__(self, **kwargs):
        self.valid_properties = BoardgameStatus.valid_properties
        super(BoardgameStatus, self).__init__(**kwargs)

    def dump(self):
        super(Rating, self).dump('%s rating' % self.name)


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
        print('%s\'s collection has %s games:' % (self.user, len(self.games)), end=' ')
        for game in self.games:
            name = game.name
            if self.rating[game.bgid].userrating:
                rating = ' rated: %s' % self.rating[game.bgid].userrating
            else:
                rating = ''
            print('%s (%s)%s,' % (game.name, game.year, rating), end=' ')

        print()


    @property
    def len(self):
        return len(self.games)
