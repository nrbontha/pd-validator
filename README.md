# Pandas DataFrame Validator

`pd-validator` is a pandas wrapper library for validating DataFrames against a user-defined schema. 

```
>>> import pandas as pd
>>> from pd_validator.schema import Schema
>>> from pd_validator.report import Report

>>> df = pd.read_csv('data.csv')
>>> df
    col_1  col_2  
    A      B      
    1      BC 
    2      D
    NaN    A

>>> rules = {
        'col_1': {
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
            'regex': False
        }
    }

>>> schema = Schema(rules=rules)

>>> rpt = Report(df=df, schema=schema())
>>> rpt()
    col_1  col_2  inval_line  inval_col  inval_val  err_msg
    1      BC     2           col_2      BC         Invalid length: 1 char max
    1      BC     2           col_2      BC         Invalid code: ['A', 'B', 'C'] required
    2      D      3           col_2      D          Invalid code: ['A', 'B', 'C'] required
    A      B      1           col_1      A          Invalid dtype: int required
    A      B      1           col_1      A          Invalid range: [0, 1] required
    2      D      3           col_1      2          Invalid range: [0, 1] required
    NaN    A      4           col_1      NaN        Missing value: col_1 required

```
