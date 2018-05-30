#!/usr/bin/env python2

import sys
import re
import numpy as np
import pandas as pd


# Suppress pandas warning
pd.options.mode.chained_assignment = None  # default='warn'


class Report(object):
    def __init__(self, file, schema):

        self.file = file
        self.schema = schema

    def get_report(self):

        report = pd.DataFrame()

        def format_inval_report(file, col, invals):
            
            rows = pd.DataFrame()

            for k, v in invals.iteritems():
                for inval in v: 
                    # Get rows with invalid values by column
                    row = self.file[file[col] == inval]

                    # Add report cols
                    row['Inval_Line'] = row.index+1
                    row.Inval_Line = row.Inval_Line.astype(int)
                    row['Inval_Col'] = col
                    row['Inval_Val'] = inval

                    # Format error message by rule
                    if k == 'inval_dtypes':
                        row['Error'] = 'Invalid dtype: %s required' \
                                        % (self.schema[col]['dtype'])

                    elif k == 'inval_lengths':
                        row['Error'] = 'Invalid length: %s maximum' \
                                        % (self.schema[col]['length'])

                    elif k == 'inval_range':
                        row['Error'] = 'Invalid number: %s required' \
                                        % (self.schema[col]['in_range'])

                    elif k == 'inval_codes':
                        row['Error'] = 'Invalid code: %s required' \
                                        % (self.schema[col]['codes'])

                    elif k == 'inval_regex':
                        row['Error'] = 'Invalid pattern: %s required' \
                                        % (self.schema[col]['regex'])

                    rows = rows.append(row, ignore_index=True)
            
            return rows

        def format_missing_report(col, missing):
            
            # Add report cols
            missing['Inval_Line'] = missing.index                
            missing['Inval_Col'] = col
            missing['Inval_Val'] = 'NaN'
            missing['Error'] = 'Missing value: %s required' % (col)

            return missing

        def format_col_report(col):
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
                report = report.append(format_col_report(col), ignore_index=True)


            else:
                if invals:
                    # Add invalid rows to report
                    report = report.append(format_inval_report(self.file, col, invals),
                                           ignore_index=True)

                # `get_missing` returns df, else None
                if isinstance(missing, pd.DataFrame):
                    # Add missing rows to report
                    report = report.append(format_missing_report(col, missing), 
                                           ignore_index=True) 

        return report


    def get_invals(self, col, schema_dtype, schema_length, schema_range=False, 
                   schema_codes=False, schema_regex=False):
        

        vals = [v for v 
                in self.file[col].unique() 
                if not pd.isnull(v)]

        invals = {}
   
        if self.file[col].dtype != schema_dtype:
            if self.file[col].dtype == object and schema_dtype == int:
                inval_dtypes = []
                for v in vals:
                    try:
                        if type(pd.to_numeric(v)) != np.dtype(np.int):
                            inval_dtypes.append(v)
                    except ValueError:
                        inval_dtypes.append(v)
                invals['inval_dtypes'] = inval_dtypes

            elif self.file[col].dtype == object and schema_dtype == float:
                inval_dtypes = []
                for v in vals:
                    try:
                        if type(pd.to_numeric(v)) != np.dtype(np.float):
                            inval_dtypes.append(v)
                    except ValueError:
                        inval_dtypes.append(v)
                invals['inval_dtypes'] = inval_dtypes

            else:  
                invals['inval_dtypes'] = [v for v
                                          in vals
                                          if type(v) != schema_dtype]
 
        if max(len(str(v)) for v in vals) > schema_length:
            invals['inval_lengths'] = [v for v 
                                       in vals 
                                       if len(str((v))) > schema_length]

        if schema_range:
            if self.file[col].dtype not in [int, float]:
                inval_range = []
                for v in vals:
                    try:
                        v_num = pd.to_numeric(v)
                        if v_num < schema_range[0] or v_num > schema_range[1]:
                            inval_range.append(v)
                    except ValueError:
                        inval_range.append(v)
                invals['inval_range'] = inval_range

            else:
                invals['inval_range'] = [v for v
                                         in vals
                                         if v < schema_range[0] or
                                            v > schema_range[1]]


        if schema_codes:
            invals['inval_codes'] = [v for v 
                                     in vals 
                                     if v not in schema_codes]

        if schema_regex:   
            pattern = re.compile(schema_regex)
            invals['inval_regex'] = [v for v 
                                     in vals 
                                     if not pattern.match(str(v))]

        return invals


    def get_missing(self, col, schema_required=False): 
        if schema_required and self.file[col].isnull().values.any():
            return self.file[pd.isnull(self.file[col])]

