#!/usr/bin/env python
from unittest import TestCase
from mock import patch

import json
import test.yahoo_options_data

computedJson = test.yahoo_options_data.contractAsJson("aapl.dat")
expectedJson = open("aapl.json").read()
expectedJson_change = open("aapl_change.json").read()

class StandAloneTests(TestCase):
    @patch('__builtin__.open')
    def test(self, mockOpen):
        mockOpen.return_value.read.return_value = 'aapl.dat'
        self.assertTrue(json.loads(computedJson) == json.loads(expectedJson) or json.loads(computedJson) == json.loads(expectedJson_change))

if json.loads(computedJson) != json.loads(expectedJson) and json.loads(computedJson) != json.loads(expectedJson_change):
  print "Test failed!"
  print "Expected output:", expectedJson
  print "Your output:", computedJson
  assert False
else:
  print "Test passed"
