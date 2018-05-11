#!/usr/bin/env python

import sys
import re
import pandas as pd

# Suppress pandas warning
pd.options.mode.chained_assignment = None  # default='warn'

def get_report(file, schema):

    report = pd.DataFrame()

    def get_invals(name, schema_type, schema_length, schema_codes=False, 
                   schema_regex=False):
        
        # Get unique vals in column 
        vals = [v for v 
                in file[name].unique() 
                if not pd.isnull(v)]
        
        # Store vals that violate schema
        invals = {}

        # Check vals against schema
        if schema_type:
            invals['inval_types'] = [v for v 
                                     in vals 
                                     if not isinstance(v, schema_type)]
        if schema_length:
            invals['inval_lengths'] = [v for v 
                                       in vals 
                                       if len(str((v))) > schema_length]
        
        if schema_codes:
            invals['inval_codes'] = [v for v 
                                     in vals 
                                     if v not in schema_codes]
        if schema_regex:    
            invals['inval_regex'] = [v for v 
                                     in vals 
                                     if re.match(schema_regex, v) is None]
        
        return invals

    def get_missing(name, schema_required=False): 
        if schema_required and file[name].isnull().values.any():
            return file[pd.isnull(file[name])]

    def format_inval_report(invals, col, file, schema):
        for k, v in invals.iteritems():
            for inval in v: 
                # Get rows with invalid values by column
                rows = file[file[col] == inval]
                
                # Add report cols
                rows['Inval_Line'] = rows.index 
                rows.Inval_Line = rows.Inval_Line.astype(int)
                rows['Inval_Col'] = col
                rows['Inval_Val'] = inval

                # Format error message by rule
                if k == 'inval_types':
                    rows['Error'] = 'Invalid type: %s required' \
                                     % (schema[col]['type'])

                elif k == 'inval_lengths':
                    rows['Error'] = 'Invalid length: %s maximum' \
                                     % (schema[col]['length'])

                elif k == 'inval_codes':
                    rows['Error'] = 'Invalid code: %s required' \
                                     % (schema[col]['codes'])

                elif k == 'inval_regex':
                    rows['Error'] = 'Invalid pattern: %s required' \
                                     % (schema[col]['regex'])

                return rows

    def format_missing_report(missing, col):
        
        # Add report cols
        missing['Inval_Line'] = missing.index                
        missing['Inval_Col'] = col
        missing['Inval_Val'] = ''
        missing['Error'] = 'Missing value: %s required' % (col)

        return missing

    def format_col_report(col):
        return {'Inval_Line': 'All',
                'Inval_Col': col,
                'Inval_Val': 'All',
                'Error': 'Column %s is missing' % (col)}

    for col in schema.keys():
        try:
            # Get invalid vals in col
            invals = get_invals(col,
                                schema[col]['type'],
                                schema[col]['length'],
                                schema[col]['codes'],
                                schema[col]['regex'])

            # Get missing vals in col if required
            missing = get_missing(col, schema[col]['required'])

        except KeyError:
            # Add missing col to report
            report = report.append(format_col_report(col), ignore_index=True)

        
        else:
            if invals:
                # Add invalid rows to report
                report = report.append(format_inval_report(invals, 
                                                           col, 
                                                           file, 
                                                           schema),
                                       ignore_index=True)

            # `get_missing` returns df, else None
            if isinstance(missing, pd.DataFrame):
                # Add missing rows to report
                report = report.append(format_missing_report(missing, col), 
                                       ignore_index=True) 

    return report
