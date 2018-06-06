#!/usr/bin/env python2

import pandas as pd
from pd_validator import Schema
from pd_validator import Report
from pandas.testing import assert_frame_equal

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
                       'regex': False}
}

# create test schema and report
test_schema = Schema(rules=test_rules)
actual_report = Report(df=df, schema=test_schema())


def test_report():
    assert assert_frame_equal(expected_report, actual_report())


if __name__ == "__main__":
    test_report()
