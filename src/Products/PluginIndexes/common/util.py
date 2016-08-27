##############################################################################
#
# Copyright (c) 2002 Zope Foundation and Contributors.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

from zope.deferredimport import deprecated

# BBB ZCatalog 5.0
deprecated(
    'Please import from Products.ZCatalog.query.',
    IndexRequestParseError='Products.ZCatalog.query:IndexQueryParseError',
    parseIndexRequest='Products.ZCatalog.query:IndexQuery',
)

_marker = []


class RequestCache(dict):

    # stats info needed for testing
    _hits = 0
    _misses = 0
    _sets = 0

    def get(self, key, default=None):
        value = super(RequestCache, self).get(key, _marker)

        if value is _marker:
            self._misses += 1
            return default

        self._hits += 1
        return value

    def __getitem__(self, key):
        try:
            value = super(RequestCache, self).__getitem__(key)
        except KeyError as e:
            self._misses += 1
            raise e

        self._hits += 1
        return value

    def __setitem__(self, key, value):
        super(RequestCache, self).__setitem__(key, value)
        self._sets += 1

    def clear(self):
        super(RequestCache, self).clear()
        self._hits = 0
        self._misses = 0
        self._sets = 0

    def stats(self):
        stats = {'hits': self._hits,
                 'misses': self._misses,
                 'sets': self._sets}
        return stats

    def __str__(self):
        return "<RequestCache %s items (hits: %s, misses: %s, sets: %s)>" % \
            (len(self), self._hits, self._misses, self._sets)
