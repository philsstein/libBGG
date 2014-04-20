
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
    valid_properties = [
        'category', 'website', 'manager', 'description', 'members', 'name', 'bggid'
    ]

    def __init__(self, **kwargs):
        for vp in Guild.valid_properties:
            setattr(self, '_' + vp, '')

        # if we're given a valid property, set it otherwise leave it
        # as None
        for key, value in kwargs.iteritems():
            if key in Guild.valid_properties:
                setattr(self, '_' + key, value)    
            else:
                err = 'bad arg given to Boardgame: %s=%s' % (
                    str(key), str(value))
                log.critical(err)
                raise GuildException(err)
        try:
            if type(self._members) != list:
                self._members = [self._members]
        except AttributeError:
            pass

    def __unicode__(self):
        return 'Guild %s (id=%s): %s' % (self.name, self.bggid)

    def __str__(self):
        return self.__unicode__().encode('utf-8').strip()

    def dump(self):
        print 'Guild %s:' % self.name
        for p in sorted(Guild.valid_properties):
            try:
                attr = getattr(self, '_' + p)
                if attr != '':
                    if type(attr) == list:
                        print '\t%s: %s' % (p, u', '.join(attr).encode('utf-8').strip())
                    else:
                        print '\t%s: %s' % (p, attr.encode('utf-8').strip())
            except AttributeError:
                pass

    @property
    def name(self):
        return self._name

    @name.setter
    def category(self, value):
        self._name = value

    @property
    def bggid(self):
        return self._bggid

    @bggid.setter
    def bggid(self, value):
        self._bggid = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    @property
    def website(self):
        return self._website

    @website.setter
    def website(self, value):
        self._website = value

    @property
    def manager(self):
        return self._manager

    @manager.setter
    def manager(self, value):
        self._manager = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def members(self):
        return self._members

    @members.setter
    def members(self, value):
        self._members = members
