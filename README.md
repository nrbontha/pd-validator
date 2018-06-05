# Pandas DataFrame Validator

`pd-validator` is a pandas wrapper library for validating DataFrames against a user-defined schema. 

```
>>> from pd_validator import Schema
>>> from pd_validator import Report

>>> rules = {'col_1': {'dtype': int, 
                       'length': 1,  
                       'range': [0,1], 
                       'required': True, 
                       'codes': False, 
                       'regex': False},
             'col_2': {'dtype': str,
                       'length': 1,
                       'range': False,
                       'required': False,
                       'codes': ['A', 'B', 'C'],
                       'regex': False}
             }

>>> df = pd.read_csv('data.csv')
>>> df
    col_1  col_2  
    A      B      
    1      BC 
    2      D
    NaN    A

>>> schema = Schema(rules=rules)
>>> report = Report(df=df, schema=schema())
>>> report()
    col_1  col_2  inval_line  inval_col  inval_val  error
    A      B      1           col_1      A          Invalid 'dtype': int required
    1      BC     2           col_2      BC         Invalid 'length': 1 required
    2      D      3           col_1      2          Invalid 'range': [0,1] required
    2      D      3           col_2      D          Invalid 'codes': ['A', 'B', 'C'] required
    NaN    A      4           col_1      NaN        Missing value: col_1 required

```
