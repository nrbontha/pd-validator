#!/usr/bin/env python2

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
    def __init__(self, rules={}):
        self._rules = rules

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

            self._rules[col] = {'dtype': dtype,
                                'length': length,
                                'range': range,
                                'required': required,
                                'codes': codes,
                                'regex': regex}

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

            self._rules[col] = {'dtype': dtype,
                                'length': length,
                                'range': range,
                                'required': required,
                                'codes': codes,
                                'regex': regex}

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
