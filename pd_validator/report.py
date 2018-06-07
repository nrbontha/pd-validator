#!/usr/bin/env python

import re
import numpy as np
import pandas as pd
from pd_validator.validator import *


def _fmt_inval_report(df, col, schema, invals):
    """
    Format report rows for column values that violate
    schema rules.

    Parameters
    ----------
    df : pd.DataFrame
    col : str
        pd.DataFrame column name
    schema : dict
        Validation rules
    invals : dict
        Invalid values by rule violated

    Returns
    -------
    pd.DataFrame
        Report rows for invalid column values

    """
    rows = pd.DataFrame()

    for k, v in invals.items():
        for inval in v: 
            row = df[df[col] == inval]

            # Add report cols
            row['inval_line'] = (row.index+1).astype(int)
            row['inval_col'] = col
            row['inval_val'] = inval
            row['err_msg'] = schema[col][k]['err_msg']

            rows = rows.append(row, ignore_index=True)
    
    return rows


def _fmt_missing_report(col, schema, missing):
    """
    Format report rows for missing required column values.

    Parameters
    ----------
    col : str
        Column name
    schema : dict
        Validation rules
    missing : pd.DataFrame
        Subset missing required column value 

    Returns
    -------
    pd.DataFrame
        Report rows for missing required values

    """
    missing['inval_line'] = (missing.index+1).astype(int)
    missing['inval_col'] = col
    missing['inval_val'] = np.nan
    missing['err_msg'] = schema[col]['required']['err_msg']

    return missing


def _fmt_col_report(col):
    """
    Format report row for missing required column.

    Parameters
    ----------
    df : pd.DataFrame
    col : str
        pd.DataFrame column name
    invals : dict
        Invalid values by rule violated

    Returns
    -------
    dict
        Report row for missing required column

    """
    return {'inval_line': 'All',
            'inval_col': col,
            'inval_val': 'All',
            'error': 'Column %s is missing' % (col)}


class Report(object):
    """
    Formatted validation report for pd.DataFrame objects.

    Attributes
    ----------
    df : pd.DataFrame
    schema : dict
        Validation rules

    Methods
    -------
    __call__
        Get report of invalid and missing values/columns

    >>> schema = Schema(rules=rules)
    >>> report = Report(df=df, schema=schema())
    >>> report()
    col_1  col_2  inval_line  inval_col  inval_val  error
    A      B      1           col_1      A          Invalid 'dtype': int required
    1      BC     2           col_2      BC         Invalid 'length': 1 required 
    
    """
    def __init__(self, df, schema):

        self.df = df
        self.schema = schema

    def __call__(self):

        report = pd.DataFrame()

        for col in self.schema.keys():
            try:
                # get invalid vals in col
                invals = self._get_invals(col,
                                          self.schema[col]['dtype']['rule'],
                                          self.schema[col]['length']['rule'],
                                          self.schema[col]['range']['rule'],
                                          self.schema[col]['codes']['rule'],
                                          self.schema[col]['regex']['rule'])

                # get missing vals in col if required
                rule = self.schema[col]['required']['rule']
                missing = self._get_missing(col, rule)

            except KeyError:
                # add missing col to report
                rows = _fmt_col_report(col)
                report = report.append(rows, ignore_index=True)


            else:
                if invals:
                    # add invalid rows to report
                    rows = _fmt_inval_report(self.df, col, self.schema, invals)
                    report = report.append(rows, ignore_index=True)

                # `get_missing` returns df, else None
                if isinstance(missing, pd.DataFrame):
                    # add missing rows to report
                    rows = _fmt_missing_report(col, self.schema, missing)
                    report = report.append(rows, ignore_index=True) 

        return report


    def _get_invals(self, col, schema_dtype, schema_length=False, 
                    schema_range=False, schema_codes=False, 
                    schema_regex=False):

        invals = {}
   
        if self.df[col].dtype != schema_dtype:
            invals['dtype'] = check_dtype(self.df, col, schema_dtype)
        if schema_length:
            invals['length'] = check_length(self.df, col, schema_length)
        if schema_range:
            invals['range'] = check_range(self.df, col, schema_range)
        if schema_codes:
            invals['codes'] = check_codes(self.df, col, schema_codes)
        if schema_regex:
            invals['regex'] = check_regex(self.df, col, schema_regex)   

        return invals


    def _get_missing(self, col, schema_required=False): 
        if schema_required and self.df[col].isnull().values.any():
            return check_missing(self.df, col)
