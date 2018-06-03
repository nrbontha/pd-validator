#!/usr/bin/env python2

import re
import numpy as np
import pandas as pd
from validator import *

class Report(object):
    
    def __init__(self, df, schema):

        self.df = df
        self.schema = schema
        self.report = pd.DataFrame()

    def get_report(self):

        def _fmt_inval_report(df, col, invals):
            
            rows = pd.DataFrame()

            for k, v in invals.iteritems():
                for inval in v: 
                    row = self.df[df[col] == inval]

                    # Add report cols
                    row['Inval_Line'] = (row.index+1).astype(int)
                    row['Inval_Col'] = col
                    row['Inval_Val'] = inval
                    row['Error'] = 'Invalid %r: %r required' \
                                    % (k, self.schema[col][k])
        
                    rows = rows.append(row, ignore_index=True)
            
            return rows

        def _fmt_missing_report(col, missing):
            
            # Add report cols
            missing['Inval_Line'] = (missing.index+1).astype(int)                
            missing['Inval_Col'] = col
            missing['Inval_Val'] = 'NA'
            missing['Error'] = 'Missing value: %s required' % (col)

            return missing

        def _fmt_col_report(col):
            return {'Inval_Line': 'All',
                    'Inval_Col': col,
                    'Inval_Val': 'All',
                    'Error': 'Column %s is missing' % (col)}

        for col in self.schema.keys():
            try:
                # Get invalid vals in col
                invals = self.get_invals(col,
                                         self.schema[col]['dtype'],
                                         self.schema[col]['length'],
                                         self.schema[col]['in_range'],
                                         self.schema[col]['codes'],
                                         self.schema[col]['regex'])

                # Get missing vals in col if required
                missing = self.get_missing(col, self.schema[col]['required'])

            except KeyError:
                # Add missing col to report
                rows = _fmt_col_report(col)
                self.report = self.report.append(rows, ignore_index=True)


            else:
                if invals:
                    # Add invalid rows to report
                    rows = _fmt_inval_report(self.df, col, invals)
                    self.report = self.report.append(rows, ignore_index=True)

                # `get_missing` returns df, else None
                if isinstance(missing, pd.DataFrame):
                    # Add missing rows to report
                    rows = _fmt_missing_report(col, missing)
                    self.report = self.report.append(rows, ignore_index=True) 

        return self.report


    def get_invals(self, col, schema_dtype, schema_length, schema_range=False, 
                   schema_codes=False, schema_regex=False):

        # Catch invalid col vals
        invals = {}
   
        if self.df[col].dtype != schema_dtype:
            invals['dtype'] = check_dtype(self.df, col, schema_dtype)
        if schema_length:
            invals['length'] = check_length(self.df, col, schema_length)
        if schema_range:
            invals['in_range'] = check_range(self.df, col, schema_range)
        if schema_codes:
            invals['codes'] = check_codes(self.df, col, schema_codes)
        if schema_regex:
            invals['regex'] = check_regex(self.df, col, schema_regex)   

        return invals


    def get_missing(self, col, schema_required=False): 
        if schema_required and self.df[col].isnull().values.any():
            return check_missing(self.df, col)
