import logging

from libBGG.PropertiedObject import PropertiedObject

log = logging.getLogger(__name__)


class UserException(Exception):
    '''Exception wrapper for User specific exceptions.'''
    pass


class User(PropertiedObject):
    '''Store information about a BGG User. The init function takes a list of valid
    proprties defined by boardgame.valid_properties. Properties that are lists can
    be given as a single item or as a list.'''

    # This should really contain the correct types as well...
    valid_properties = [
        'name', 'hot10', 'top10', 'firstname', 'lastname', 'yearregistered', 'lastlogin',
        'stateorprovince', 'country', 'traderating', 'bggid'
    ]

    def __init__(self, **kwargs):
        self.valid_properties = User.valid_properties
        super(User, self).__init__(**kwargs)
        # force lists to be lists
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
        super(User, self).dump('%s' % self.name)

    @property
    def fullname(self):
        return ' '.join([self.firstname, self.lastname]).encode('utf-8').strip() 
