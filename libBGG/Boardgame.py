import logging

from libBGG.PropertiedObject import PropertiedObject

log = logging.getLogger(__name__)


class BoardgameException(Exception):
    '''Exception wrapper for Boardgame specific exceptions.'''
    pass


class Boardgame(PropertiedObject):
    '''Store information about a boardgame. The init function takes a list of valid
    proprties defined by boardgame.valid_properties. Properties that are lists can
    be given as a single item or as a list.'''

    # This should really contain the correct types as well...
    valid_properties = [
        'designers', 'artists', 'playingtime', 'thumbnail',
        'image', 'description', 'minplayers', 'maxplayers',
        'categories', 'mechanics', 'families', 'publishers', 
        'website', 'year', 'names', 'bgid'
    ]

    def __init__(self, **kwargs):
        self.valid_properties = Boardgame.valid_properties
        super(Boardgame, self).__init__(**kwargs)
        # force lists to be lists
        for l in ['designers', 'artists', 'categories', 'mechanics', 'families', 'publishers',
                  'names']:
            try:
                if type(getattr(self, l)) != list:
                    setattr(self, l, [getattr(self, l)])
            except AttributeError:
                pass

    def __unicode__(self):
        return '%s (%s) by %s' % (self.name, self._year, ', '.join(self._designers))

    def __str__(self):
        return self.__unicode__().encode('utf-8').strip()

    def dump(self):
        super(Boardgame, self).dump('%s' % self.name)

    # Litte syntactic sugar for the more usual case of a single name.
    @property
    def name(self):
        return self.names[0]

    @name.setter
    def name(self, value):
        self.names = [value]
