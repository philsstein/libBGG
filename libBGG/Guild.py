import logging

log = logging.getLogger(__name__)


class GuildException(Exception):
    '''Exception wrapper for Guild specific exceptions.'''
    pass


class Guild(object):
    '''Store information about a BGG Guild. The init function takes a list of valid
    proprties defined by Guild.valid_properties.'''

    # This should really contain the correct types as well...
    # ... and be put in a common base class.
    __slots__ = [
        'category', 'website', 'manager', 'description', 'members', 'name', 'gid'
    ]

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        # force self.members to be a list.
        try:
            if type(self._members) != list:
                self._members = [self._members]
        except AttributeError:
            pass

    def dump(self):
        log.debug('Guild %s:' % self.name)
        for a in Guild.__slots__:
            log.debug('\t%s: %s' % (a, getattr(self, a, None)))

    def __unicode__(self):
        return 'Guild %s (id=%s): %s' % (self.name, self.gid)

    def __str__(self):
        return self.__unicode__().encode('utf-8').strip()
