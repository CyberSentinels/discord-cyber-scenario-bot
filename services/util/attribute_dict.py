# this class enables dictionaries that behavior similarily to js objects (can access field via period ".")
class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

