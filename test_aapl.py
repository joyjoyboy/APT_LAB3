#!/usr/bin/env python
from unittest import TestCase
from mock import patch

import json
import yahoo_options_data

class Test(TestCase):
    @patch('__builtin__.open')
    def test(self, mockOpen):
        mockOpen.return_value.read.return_value = 'aapl.dat'
        self.assertTrue(json.loads(computedJson) == json.loads(expectedJson) or json.loads(computedJson) == json.loads(expectedJson_change))

computedJson = yahoo_options_data.contractAsJson("aapl.dat")
expectedJson = open("aapl.json").read()
expectedJson_change = open("aapl_change.json").read()

if json.loads(computedJson) != json.loads(expectedJson) and json.loads(computedJson) != json.loads(expectedJson_change):
  print "Test failed!"
  print "Expected output:", expectedJson
  print "Your output:", computedJson
  assert False
else:
  print "Test passed"
