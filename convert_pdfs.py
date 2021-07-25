''' Convert pdf sales books to csv format

Usage:

python convert_pdfs.py in_dir/ output_dir/

'''

import camelot
import sys
import os
import pandas as pd

def ingest_pdf(pdf_dir, file_name, read_kwargs = {}):
    ''' Convert tables in pdfs into csv format.
    Inputs:
        pdf_dir: The directory where the pdf file is found.
        file_name: The specific file in pdf_dir to convert.
        read_kwargs: Keyword arguments passed to camelot.read_pdf
    Outputs:
        A tuple of (pandas.DataFrame, str) where the first element is the table
        content of file_name, and the second element is file_name.
    '''
    # collect pdf data and return as dfs
    # to do: add link to camelot docs
    tables = camelot.read_pdf(os.path.join(pdf_dir, file_name),
                            **read_kwargs)
    # for each table in the document, yield its contents
    # we do this so we don't end up overlapping and so you can keep cleaning
    # separate from collection
    for each_table in tables:
        yield each_table.df, file_name

def write_pdfs_to_csv(tables, out_file, **kwargs):
    ''' Write pdf content to a csv (out_file).
    Input:
        tables: a pandas.DataFrame object, or any object with a to_csv() method.
        out_file: where to save the csv
        **kwargs: passed to the to_csv() method of tables.
    Outputs:
        Saves to the file specified by out_file.
    '''
    tables.to_csv(out_file, **kwargs)

if __name__ == "__main__":

    # for every file in the target directory
    for file_name in os.listdir(sys.argv[1]):
        cnt = 0 # keep track of tables by giving them a number
        for table, f in ingest_pdf(sys.argv[1], file_name,
                                    read_kwargs = dict(flavor = 'stream',
                                                            pages = '5-end')):
            # for each table in a given file, write to csv
            write_pdfs_to_csv(table, os.path.join(sys.argv[2],
                                file_name + '_{}.csv'.format(cnt)))
            cnt += 1
