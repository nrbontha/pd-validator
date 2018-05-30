#!/usr/bin/env python2

import re

class RuleError(Exception):
    pass


#TODO: init with dict
class Schema(object):
    def __init__(self):

        self.rules = {}

    def get_rule(self, col):
        return self.rules[col]

    def create_rule(self, col, dtype, length, in_range=False, 
                    required=False, codes=False, regex=False):
        
        if col not in self.rules.keys():
            self.rules[col] = {'dtype': dtype,
                               'length': length,
                               'in_range': in_range,
                               'required': required,
                               'codes': codes,
                               'regex': regex}
            
            if in_range and dtype not in [int, float]:
                raise RuleError('%s schema dtype must be int or float for \
                                 valid `in_range` rule' % col)

            return "New rule created: %s" % (self.rules[col])

        else:
            raise RuleError('rule for %s already exists' % (col)) 

    def update_rule(self, col, dtype, length=MAX_LEN, in_range=False, 
                    required=False, codes=False, regex=False):
        
        if self.rules[col]:
            self.rules[col] = {'dtype': dtype,
                               'length': length,
                               'in_range': in_range,
                               'required': required,
                               'codes': codes,
                               'regex': regex}
            
            if in_range and dtype not in [int, float]:
                raise RuleError('%s schema dtype must be int or float for \
                                 valid `in_range` rule' % col)

            return "Existing rule updated: %s" % (self.rules[col])

        else:
            raise RuleError('rule for %s does not exist' % (col))

    def delete_rule(self, col):
        
        if self.rules[col]:
            self.rules.pop(col)

            return "Existing rule deleted: %s" % (col)
        
        else:
            raise RuleError('rule for %s does not exist' % (col))

