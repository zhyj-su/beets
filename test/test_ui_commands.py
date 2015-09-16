# -*- coding: utf8 -*-
# This file is part of beets.
# Copyright 2015, Adrian Sampson.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

"""Your description
"""
import os
import shutil

from test import _common
from test._common import unittest

from beets import library
from beets import ui
from beets.ui import commands


class QueryTest(_common.TestCase):
    def setUp(self):
        super(QueryTest, self).setUp()

        self.io.install()

        self.libdir = os.path.join(self.temp_dir, 'testlibdir')
        os.mkdir(self.libdir)

        # Add a file to the library but don't copy it in yet.
        self.lib = library.Library(':memory:', self.libdir)

        # Alternate destination directory.
        self.otherdir = os.path.join(self.temp_dir, 'testotherdir')

    def add_Item(self, filename='srcfile', templatefile='full.mp3'):
        itempath = os.path.join(self.libdir, filename)
        shutil.copy(os.path.join(_common.RSRC, templatefile), itempath)
        item = library.Item.from_path(itempath)
        self.lib.add(item)
        return item, itempath

    def add_album(self, items):
        album = self.lib.add_album(items)
        return album

    def test_query_empty(self):
        try:
            items, albums = commands._do_query(self.lib, (), False)
            raise Exception("A UserError should have been raised")
        except ui.UserError:
            pass

    def test_query_empty_album(self):
        try:
            items, albums = commands._do_query(self.lib, (), True)
            raise Exception("A UserError should have been raised")
        except ui.UserError:
            pass

    def test_query_item(self):
        self.i, self.itempath = self.add_Item()
        items, albums = commands._do_query(self.lib, (), False)
        self.assertEqual(len(albums), 0)
        self.assertEqual(len(items), 1)

        self.i, self.itempath = self.add_Item()
        items, albums = commands._do_query(self.lib, (), False)
        self.assertEqual(len(albums), 0)
        self.assertEqual(len(items), 2)

    def test_query_album(self):
        self.i, self.itempath = self.add_Item()
        self.album = self.add_album([self.i])
#        raise Exception(self.album)
        items, albums = commands._do_query(self.lib, (), True)
        self.assertEqual(len(items), 1)
        self.assertEqual(len(albums), 1)
        items, albums = commands._do_query(
            self.lib, (), True, also_items=False)
        self.assertEqual(len(items), 0)
        self.assertEqual(len(albums), 1)

        self.i, self.itempath = self.add_Item()
        self.i2, self.itempath = self.add_Item()
        self.album = self.add_album([self.i, self.i2])
        items, albums = commands._do_query(self.lib, (), True)
        self.assertEqual(len(items), 3)
        self.assertEqual(len(albums), 2)
        items, albums = commands._do_query(
            self.lib, (), True, also_items=False)
        self.assertEqual(len(items), 0)
        self.assertEqual(len(albums), 2)


def suite():
    return unittest.TestLoader().loadTestsFromName(__name__)

if __name__ == b'__main__':
    unittest.main(defaultTest='suite')
