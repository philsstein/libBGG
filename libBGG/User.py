import logging


log = logging.getLogger(__name__)


class UserException(Exception):
    '''Exception wrapper for User specific exceptions.'''
    pass


class User(object):
    '''Store information about a BGG User. The init function takes a list of valid
    proprties defined by boardgame.__slots__. Properties that are lists can
    be given as a single item or as a list.'''

    # This should really contain the correct types as well...
    __slots__ = [
        'name', 'hot10', 'top10', 'firstname', 'lastname', 'yearregistered', 'lastlogin',
        'stateorprovince', 'country', 'traderating', 'bgid'
    ]

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        for l in ['top10', 'hot10']:
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
        log.debug('%s' % self.name)
        for a in User.__slots__:
            log.debug('\t%s: %s' % (a, getattr(self, a, 'Unknown')))

    @property
    def fullname(self):
        return ' '.join([self.firstname, self.lastname]).encode('utf-8').strip()
