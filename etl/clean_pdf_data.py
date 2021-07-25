''' Clean the data from pdfs.

python3 clean_pdf_data.py [in_dir] [out_dir] [number of rows before data] \
    [column names]

python3 clean_pdf_data.py in_dir/ out_dir/ 4 \
    'idx,address,roll_no,sale_yr,sale_mth,sale_price,adj_sale_price'



'''

import pandas as pd
from sys import argv
import os

def main(argv):
    target_dir, out_dir, skip_rows, cols = argv
    cols = cols.split(",")

    for i in os.listdir(target_dir):
        try:
            fpath = os.path.join(target_dir, i)
            df = pd.read_csv(fpath, skiprows = int(skip_rows),
                            names = cols)

            # done and write
            df.to_csv(os.path.join(out_dir, i), index = False)
        except Exception as e:
            print("Failed conversion: {}".format(i), e)


if __name__ == "__main__":

    main(argv[1:])
