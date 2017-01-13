# -*- coding: utf-8 -*-

import pydiff

import utils


class TestWord(utils.TestBase):

    def setUp(self):
        self.differ = pydiff.WordDiff()

    def test_diff_words_whitespaces(self):
        self.check_xml('New Value', 'New  ValueMoreData',
                       'New  <del>Value</del><ins>ValueMoreData</ins>')

        self.check_xml('New Value  ', 'New  ValueMoreData ',
                       'New  <del>Value</del><ins>ValueMoreData</ins> ')

    def test_diff_words_boundaries(self):
        self.check_xml('New :Value:Test', 'New  ValueMoreData ',
                       'New  <del>:Value:Test</del><ins>ValueMoreData </ins>')

        self.check_xml('New Value:Test', 'New  Value:MoreData ',
                       'New  Value:<del>Test</del><ins>MoreData </ins>')

        self.check_xml('New Value-Test', 'New  Value:MoreData ',
                       'New  Value<del>-Test</del><ins>:MoreData </ins>')

        self.check_xml('New Value', 'New  Value:MoreData ',
                       'New  Value<ins>:MoreData </ins>')

    def test_diff_words_no_changes(self):
        self.check_xml('New Value', 'New Value', 'New Value')

        self.check_xml('', '', '')

        self.check_xml('New Value', 'New  Value', 'New  Value')

    def test_diff_words_empty(self):
        self.check_xml('New Value', '',
                       '<del>New Value</del>')

        self.check_xml('', 'New Value',
                       '<ins>New Value</ins>')

    def test_diff_words_no_anchor(self):
        self.check_xml('New Value New Value', 'Value Value New New',
                       '<del>New</del><ins>Value</ins> Value New <del>Value</del><ins>New</ins>')

    def test_tokenize_unicode(self):
        self.assertEqual([u'jurídica'],
                         self.differ.tokenize(u'jurídica'))

        self.assertEqual([u'wir', u' ', u'üben'],
                         self.differ.tokenize(u'wir üben'))

    def test_diff_words_count_identity(self):
        self.check_changes('foo', 'foo',
                           [{'value': 'foo', 'count': 1}])

        self.check_changes('foo bar', 'foo bar',
                           [{'value': 'foo bar', 'count': 3}])

    def test_diff_words_count_empty(self):
        self.check_changes('foo', '',
                           [{'value': 'foo', 'count': 1, 'added': None, 'removed': True}])

        self.check_changes('foo bar', '',
                           [{'value': 'foo bar', 'count': 3, 'added': None, 'removed': True}])

        self.check_changes('', 'foo',
                           [{'value': 'foo', 'count': 1, 'added': True, 'removed': None}])

        self.check_changes('', 'foo bar',
                           [{'value': 'foo bar', 'count': 3, 'added': True, 'removed': None}])

    def test_diff_words_ignore_whitespaces(self):
        self.check_changes('hase igel fuchs', 'hase igel fuchs',
                           [{'count': 5, 'value': 'hase igel fuchs'}])

        self.check_changes('hase igel fuchs', 'hase igel fuchs\n',
                           [{'count': 5, 'value': 'hase igel fuchs\n'}])

        self.check_changes('hase igel fuchs\n', 'hase igel fuchs',
                           [{'count': 5, 'value': 'hase igel fuchs\n'}])

        self.check_changes('hase igel fuchs', 'hase igel\nfuchs',
                           [{'count': 5, 'value': 'hase igel\nfuchs'}])

        self.check_changes('hase igel\nfuchs', 'hase igel fuchs',
                           [{'count': 5, 'value': 'hase igel fuchs'}])

    def test_diff_words_only_whitespaces(self):
        self.check_xml('', ' ', '<ins> </ins>')

        self.check_xml(' ', '', '<del> </del>')
