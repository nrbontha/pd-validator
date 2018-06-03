#!/usr/bin/env python2

import re
import numpy as np
import pandas as pd

# Suppress pandas warning
pd.options.mode.chained_assignment = None  #default='warn'

def _get_vals(df, col):
    return [v for v in df[col].unique() if not pd.isnull(v)]

def check_dtype(df, col, schema_dtype):
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
    return [v for v in _get_vals(df, col) if len(str((v))) > schema_length]


def check_range(df, col, schema_range):
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
    return [v for v in _get_vals(df, col) if v not in schema_codes]


def check_regex(df, col, schema_regex):
    p = re.compile(schema_regex)
    return [v for v in _get_vals(df, col) if not p.match(str(v))]


def check_missing(df, col):
    return df[pd.isnull(df[col])]
