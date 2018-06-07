#!/usr/bin/env python

import re
import numpy as np
import pandas as pd


# suppress pandas warning
pd.options.mode.chained_assignment = None  #default='warn'


def _get_vals(df, col):
    """
    Get unique values in column.

    Parameters
    ----------
    df : pd.DataFrame
    col : str
        pd.DataFrame column name

    Returns
    -------
    array_like
        Unique values in column
    
    >>> vals = _get_vals(df, col)
    ['hello', 1, 1.0, True]

    """
    return [v for v in df[col].unique() if not pd.isnull(v)]

def check_dtype(df, col, schema_dtype):
    """
    Get invalid dtype values.

    Parameters
    ----------
    df : pd.DataFrame
    col : str
        pd.DataFrame column name
    schema_dtype : data type
        Required col dtype

    Returns
    -------
    array_like
        Invalid values

    >>> inval_dtype = check_dtype(df, col, int)
    ['hello', 1.0, True]

    """
    invals = []

    if df[col].dtype == object and schema_dtype == int:
        for v in _get_vals(df, col):
            try:
                if type(pd.to_numeric(v)) != np.dtype(np.int):
                    invals.append(v)
            except ValueError:
                invals.append(v)

    elif df[col].dtype == object and schema_dtype == float:
        for v in _get_vals(df, col):
            try:
                if type(pd.to_numeric(v)) != np.dtype(np.float):
                    invals.append(v)
            except ValueError:
                invals.append(v)

    else:
        invals = [v for v in _get_vals(df, col) if type(v) != schema_dtype]

    return invals


def check_length(df, col, schema_length):
    """
    Get values that are greater than max allowed length.

    Parameters
    ----------
    df : pd.DataFrame
    col : str
        pd.DataFrame column name
    schema_length : int
        Max string length

    Returns
    -------
    array_like
        Invalid values

    >>> inval_length = check_dtype(df, col, 1)
    ['hello', 'world']

    """
    return [v for v in _get_vals(df, col) if len(str((v))) > schema_length]


def check_range(df, col, schema_range):
    """
    Get out of range values.

    Parameters
    ----------
    df : pd.DataFrame
    col : str
        pd.DataFrame column name
    schema_range : array_like
        Min value, max value

    Returns
    -------
    array_like
        Invalid values

    >>> inval_range = check_range(df, col, [0,1])
    [2, 3, 4]

    """
    invals = []

    if df[col].dtype not in [int, float]:
        for v in _get_vals(df, col):
            try:
                v_num = pd.to_numeric(v)
                if v_num < schema_range[0] or v_num > schema_range[1]:
                    invals.append(v)
            except ValueError:
                invals.append(v)

    else:
        invals = [v for v in _get_vals(df, col) 
                  if v < schema_range[0] 
                  or v > schema_range[1]]

    return invals

def check_codes(df, col, schema_codes):
    """
    Get values not in list of codes.

    Parameters
    ----------
    df : pd.DataFrame
    col : str
        pd.DataFrame column name
    schema_codes : array_like
        List of allowed values

    Returns
    -------
    array_like
        Invalid values

    >>> inval_codes = check_range(df, col, ['hello', 1, 1.0, True])
    ['world', 2, 2.0, False]

    """
    return [v for v in _get_vals(df, col) if v not in schema_codes]


def check_regex(df, col, schema_regex):
    """
    Get values that violate regex pattern.

    Parameters
    ----------
    df : pd.DataFrame
    col : str
        pd.DataFrame column name
    schema_regex : str 
        Regex pattern

    Returns
    -------
    array_like
        Invalid values

    >>> inval_regex = check_regex(df, col, r'(\d+/\d+/\d+)')
    ['Jan 1st 2018', '1-1-2018']

    """
    p = re.compile(schema_regex)
    return [v for v in _get_vals(df, col) if not p.match(str(v))]


def check_missing(df, col):
    """
    Get missing values in column.

    Parameters
    ----------
    df : pd.DataFrame
    col : str
        pd.DataFrame column name

    Returns
    -------
    pd.DataFrame
        df rows missing col value

    """
    return df[pd.isnull(df[col])]
