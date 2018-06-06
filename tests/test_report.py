#!/usr/bin/env python2

import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from pd_validator import Schema
from pd_validator import Report

# read in test data and report
df = pd.read_csv('../data/test_data.csv')
expected_report = pd.read_csv('../data/test_report.csv')

# set up test rules dict
test_rules = {'col_1': {
                        'dtype': int, 
                        'length': 1,  
                        'range': [0,1], 
                        'required': True, 
                        'codes': False, 
                        'regex': False
                       },
              'col_2': {
                        'dtype': str,
                        'length': 1,
                        'range': False,
                        'required': False,
                        'codes': ['A', 'B', 'C'],
                        'regex': False
                       }
}


# create test schema and report
test_schema = Schema(rules=rules)
actual_report = Report(df=df, schema=schema())

def test_report():
    assert assert_frame_equal(expected_report, actual_report)

