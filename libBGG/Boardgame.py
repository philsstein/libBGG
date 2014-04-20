import logging

log = logging.getLogger(__name__)

class BoardgameException(Exception):
    '''Exception wrapper for Boardgame specific exceptions.'''
    pass


class Boardgame(object):
    '''Store information about a boardgame. The init function takes a list of valid
    proprties defined by boardgame.valid_properties.'''

    # This should really contain the correct types as well...
    valid_properties = [
        'designers', 'artists', 'playingtime', 'thumbnail',
        'image', 'description', 'minplayers', 'maxplayers',
        'categories', 'mechanics', 'families', 'publishers', 
        'website', 'year', 'names', 'bgid'
    ]

    def __init__(self, **kwargs):
        # set all attributes to None
        for vp in Boardgame.valid_properties:
            setattr(self, '_' + vp, '')

        # if we're given a valid property, set it otherwise leave it
        # as None
        for key, value in kwargs.iteritems():
            if key in Boardgame.valid_properties:
                setattr(self, '_' + key, value)    
            else:
                err = 'bad arg given to Boardgame: %s=%s' % (
                    str(key), str(value))
                log.critical(err)
                raise BoardgameException(err)

        # force lists to be lists
        for l in ['designers', 'artists', 'categories', 'mechanics', 'families', 'publishers',
                  'names']:
            try:
                if type(getattr(self, '_' + l)) != list:
                    setattr(self, '_' + l, [getattr(self, '_' + l)])
            except AttributeError:
                pass

    def __unicode__(self):
        return '%s (%s) by %s' % (self.name, self._year, ', '.join(self._designers))

    def __str__(self):
        return self.__unicode__().encode('utf-8').strip()

    def dump(self):
        print '%s:' % self.name
        for p in sorted(Boardgame.valid_properties):
            try:
                attr = getattr(self, '_' + p)
                if len(attr) > 0:
                    if type(attr) == list:
                        print '\t%s: %s' % (p, u', '.join(attr).encode('utf-8').strip())
                    else:
                        print '\t%s: %s' % (p, attr.encode('utf-8').strip())
            except AttributeError:
                pass

    @property
    def name(self):
        return self._names[0]

    @name.setter
    def name(self, value):
        self._names = [value]

    @property
    def names(self):
        return self._names

    @names.setter
    def names(self, value):
        if type(value) == list:
            log.debug('setting names from list')
            self._names = value
        else:
            log.debug('setting names from string')
            self._names = [value]

    @property
    def thumbnail(self):
        return self._thumbnail

    @thumbnail.setter
    def thumbnail(self, value):
        self._thumbnail = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        self._year = year

    @property
    def minplayers(self):
        return self._minplayers

    @minplayers.setter
    def minplayers(self, value):
        self._minplayers = value

    @property
    def maxplayers(self):
        return self._maxplayers

    @maxplayers.setter
    def maxplayers(self, value):
        self._maxplayers = value

    @property
    def categories(self):
        return self._categories

    @categories.setter
    def categories(self, value):
        self._categories = value

    @property
    def mechanics(self):
        return self._mechanics

    @mechanics.setter
    def mechanics(self, value):
        self._mechanics = value

    @property
    def families(self):
        return self._families

    @families.setter
    def families(self, value):
        self._families = value

    @property
    def publishers(self):
        return self._publishers

    @publishers.setter
    def publishers(self, value):
        self._publishers = value

