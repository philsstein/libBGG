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
    __slots__ = [
        'designers', 'artists', 'playingtime', 'thumbnail',
        'image', 'description', 'minplayers', 'maxplayers',
        'categories', 'mechanics', 'families', 'publishers',
        'website', 'year', 'names', 'bgid'
    ]

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
       
        self._list_slots = ['designers', 'artists', 'categories', 'mechanics', 'families',
                            'publishers', 'names']
        # force these to be lists.
        for l in self._list_slots:
            try:
                if type(getattr(self, l)) != list:
                    setattr(self, l, [getattr(self, l)])
            except AttributeError:
                pass

    def dump(self):
        log.debug('%s:' % self.name)
        for a in Boardgame.__slots__:
            if getattr(self, a, None):
                if a in self._list_slots:
                    log.debug('\t%s: %s' % (a, ', '.join(getattr(self, a))))
                else:
                    log.debug('\t%s: %s' % (a, getattr(self, a)))

    def __unicode__(self):
        return '%s (%s) by %s' % (self.name, self.year, ', '.join(self.designers))

    def __str__(self):
        return self.__unicode__().encode('utf-8').strip()

    # Litte syntactic sugar for the more usual case of a single name.
    @property
    def name(self):
        if getattr(self, 'names', None):
            return self.names[0]
        return None

    @name.setter
    def name(self, value):
        self.names = [value]
