#!/usr/bin/env python2

import sys
import re

class Schema(object):
    
    def __init__(self, rules={}):
        self._rules = rules

    def __repr__(self):
        return 'Schema(rules=%r)' % (self._rules)
    
    def get_rules(self):
        return self._rules

    def get_rule(self, col):
        return self._rules[col]

    def create_rule(self, col, dtype, length=False, in_range=False, 
                    required=False, codes=False, regex=False):

        if col not in self._rules.keys():
            if in_range and dtype not in [int, float]:
                raise TypeError('%s schema dtype must be int or float for \
                                 valid `in_range` rule' % col)

            self._rules[col] = {'dtype': dtype,
                               'length': length,
                               'in_range': in_range,
                               'required': required,
                               'codes': codes,
                               'regex': regex}

        else:
            raise ValueError('rule for %s already exists' % (col)) 

    def update_rule(self, col, dtype, length=False, in_range=False, 
                    required=False, codes=False, regex=False):

        if self._rules[col]:
            if in_range and dtype not in [int, float]:
                raise TypeError('%s schema dtype must be int or float for \
                                 valid `in_range` rule' % col)

            self._rules[col] = {'dtype': dtype,
                               'length': length,
                               'in_range': in_range,
                               'required': required,
                               'codes': codes,
                               'regex': regex}

        else:
            raise KeyError('rule for %s does not exist' % (col))

    def delete_rule(self, col):

        if self._rules[col]:
            self._rules.pop(col)
        
        else:
            raise KeyError('rule for %s does not exist' % (col))
