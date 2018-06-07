#!/usr/bin/env python

import pandas as pd
from pd_validator.validator import *
from pd_validator.schema import Schema
from pd_validator.report import Report
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

# create sort list for equality test
sort = ['inval_line', 'inval_col', 'inval_val', 'err_msg']

def test_report():
    assert_frame_equal(expected_report.sort_values(by=sort) \
                                      .reset_index(drop=True), 
                       actual_report().sort_values(by=sort) \
                                      .reset_index(drop=True))


if __name__ == "__main__":
    test_report()
