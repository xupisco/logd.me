# coding: utf-8
from __future__ import unicode_literals

from fnmatch import fnmatch


class globlist(list):
    def __contains__(self, key):
        for pat in self:
            if fnmatch(key, pat):
                return True
        return False
