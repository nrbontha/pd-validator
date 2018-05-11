#!/usr/bin/env python

import validator
import pandas as pd 
from validator import get_report
from schema import Schema
from schema import RuleError

if __name__ == "__main__":

    test_file = pd.read_csv('data/test_data.csv')

    test_schema = Schema()
    test_schema.create_rule(name='x', type=str, length=3, required=True, regex='[979]')
    test_schema.create_rule(name='y', type=str, length=10, required=True)

    report = get_report(test_file, test_schema.rules)

    print report




