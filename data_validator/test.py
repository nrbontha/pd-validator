#!/usr/bin/env python

import validator
import pandas as pd 
from validator import get_report
from schema import Schema
from schema import RuleError

if __name__ == "__main__":

    test_file = pd.read_csv('data/test_data.csv')

    test_schema = Schema()
    test_schema.create_rule(name='team', type=str, length=3, required=True)
    test_schema.create_rule(name='first_name', type=str, length=30, required=True)
    test_schema.create_rule(name='last_name', type=str, length=30, required=True)
    test_schema.create_rule(name='age', type=int, length=2, required=True)

    rules = test_schema.rules

    report = get_report(test_file, rules)

    print report
