#!/usr/bin/env python

import sys
import re

class Schema(object):
    """
    Formatted validation rules for pd.DataFrame objects.

    Attributes
    ----------
    rules : dict, optional
        Validation rules

    Methods
    -------
    __call__
        Get validation rules

    """    
    def __init__(self, rules=None):
        self._rules = {}

        if rules:
            for col in rules:
                self.create_rule(col=col, 
                                 dtype=rules[col]['dtype'],
                                 length=rules[col]['length'],
                                 range=rules[col]['range'],
                                 required=rules[col]['required'],
                                 codes=rules[col]['codes'],
                                 regex=rules[col]['regex'])

    def __repr__(self):
        return 'Schema(rules=%r)' % (self._rules)
    
    def __call__(self):
        return self._rules

    def get_rule(self, col):
        return self._rules[col]

    def create_rule(self, col, dtype, length=False, range=False, 
                    required=False, codes=False, regex=False):
        """
        Add rule to schema.

        Parameters
        ----------
        col : str
            Column name
        dtype : str
            Data type name (str, int, float, bool)
        length : int
            Maximum allowed character length
        range : array_like
            Min value, max value for numeric column
        required : bool
            Missing values constraint
        codes : array_like
            Allowed values
        regex : str
            Regular expression pattern

        Raises
        -------
        TypeError
            When range is set on non-numeric column
        ValueError
            When rule already exists for column name

        """
        if col not in self._rules.keys():
            if range and dtype not in [int, float]:
                raise TypeError('%s schema dtype must be int or float for \
                                 valid `range` rule' % col)

            self._rules[col] = {'dtype': {
                                    'rule': dtype, 
                                    'err_msg': 'Invalid dtype: %s required' \
                                                % dtype.__name__ 
                                    },
                                'length': {
                                    'rule': length,
                                    'err_msg': 'Invalid length: %s char max' \
                                                % length 
                                    },
                                'range': {
                                    'rule': range,
                                    'err_msg': 'Invalid range: %s required' \
                                                % range 
                                    },
                                'required': {
                                    'rule': required,
                                    'err_msg': 'Missing value: %s required' \
                                                % col 
                                    },
                                'codes': {
                                    'rule': codes,
                                    'err_msg': 'Invalid code: %s required' \
                                                % codes 
                                    },
                                'regex': {'rule': regex,
                                         'err_msg': 'Invalid regex: %s required' \
                                                     % regex
                                    }
                                }

        else:
            raise ValueError('rule for %s already exists' % (col)) 

    def update_rule(self, col, dtype, length=False, range=False, 
                    required=False, codes=False, regex=False):

        """
        Update rule in schema.

        See `create_rule` for parameter info.

        Raises
        -------
        TypeError
            When range is set on non-numeric column
        KeyError
            When rule for column name does not already exist

        """
        if self._rules[col]:
            if range and dtype not in [int, float]:
                raise TypeError('%s schema dtype must be int or float for \
                                 valid `range` rule' % col)

            self._rules[col] = {'dtype': {
                                    'rule': dtype, 
                                    'err_msg': 'Invalid dtype: %s required' \
                                                % dtype.__name__ 
                                    },
                                'length': {
                                    'rule': length,
                                    'err_msg': 'Invalid length: %s char max' \
                                                % length 
                                    },
                                'range': {
                                    'rule': range,
                                    'err_msg': 'Invalid range: %s required' \
                                                % range 
                                    },
                                'required': {
                                    'rule': required,
                                    'err_msg': 'Missing value: %s required' \
                                                % col 
                                    },
                                'codes': {
                                    'rule': codes,
                                    'err_msg': 'Invalid code: %s required' \
                                                % codes 
                                    },
                                'regex': {'rule': regex,
                                         'err_msg': 'Invalid regex: %s required' \
                                                     % regex
                                    }
                                }

        else:
            raise KeyError('rule for %s does not exist' % (col))

    def delete_rule(self, col):
        """
        Delete rule from schema.

        Parameters
        ----------
        col : str
            Column name

        Raises
        -------
        KeyError
            When rule for column name does not already exist

        """
        if self._rules[col]:
            self._rules.pop(col)
        
        else:
            raise KeyError('rule for %s does not exist' % (col))
