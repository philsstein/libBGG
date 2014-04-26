import logging
from libBGG.PropertiedObject import PropertiedObject

log = logging.getLogger(__name__)


class GuildException(Exception):
    '''Exception wrapper for Guild specific exceptions.'''
    pass


class Guild(PropertiedObject):
    '''Store information about a BGG Guild. The init function takes a list of valid
    proprties defined by Guild.valid_properties.'''

    # This should really contain the correct types as well...
    # ... and be put in a common base class.
    valid_properties = [
        'category', 'website', 'manager', 'description', 'members', 'name', 'gid'
    ]

    def __init__(self, **kwargs):
        self.valid_properties = Guild.valid_properties
        super(Guild, self).__init__(**kwargs)

        # force self.members to be a list.
        try:
            if type(self._members) != list:
                self._members = [self._members]
        except AttributeError:
            pass

    def dump(self):
        super(Guild, self).dump('Guild %s' % self.name)

    def __unicode__(self):
        return 'Guild %s (id=%s): %s' % (self.name, self.gid)

    def __str__(self):
        return self.__unicode__().encode('utf-8').strip()
