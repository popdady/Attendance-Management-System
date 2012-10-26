# -*- coding: utf-8 -*-
"""
    test cases for amsUser.

    :copyright: (c) 2012 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from datetime import datetime

from django.utils import unittest

from amsUser.models import Time, UserTime

class ModelTest(unittest.TestCase): 
    def setUp(self):
        self.time_obj = Time.objects.create(time_in = datetime.time(datetime.now()), time_out = datetime.time(datetime.now()))

    def test_Time_model_insert(self):
        self.assertEqual(self.time_obj, datetime.time())
