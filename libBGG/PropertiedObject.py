import logging

log = logging.getLogger(__name__)


class PropertiedObjectException(Exception):
    pass


class PropertiedObject(object):
    '''This class defines its properties at init time. Query __dict__ or valid_properties
    to access properties exported by the class.'''
    def __init__(self, **kwargs):
        try:
            props = getattr(self, 'valid_properties')
        except AttributeError as e:
            raise PropertiedObjectException('valid_properties not defined.')

        # set all attributes to None
        for p in props:
            setattr(self, p, '')

        # if we're given a valid property, set it otherwise leave it
        # as None
        for key, value in kwargs.iteritems():
            if key in props:
                setattr(self, key, value)    
            else:
                err = 'bad arg given to a PropertiedObject: %s=%s' % (
                    str(key), str(value))
                log.critical(err)
                raise PropertiedObjectException(err)

    def dump(self, label):
        print '%s:' % label
        try:
            props = getattr(self, 'valid_properties')
        except AttributeError as e:
            raise PropertiedObjectException('valid_properties not defined.')

        for p in sorted(props):
            try:
                attr = getattr(self, p)
                if len(attr) > 0:
                    if type(attr) == list:
                        print '\t%s: %s' % (p, u', '.join(attr).encode('utf-8').strip())
                    else:
                        print '\t%s: %s' % (p, attr.encode('utf-8').strip())
            except AttributeError:
                pass
