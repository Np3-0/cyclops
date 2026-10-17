from ppf.datamatrix import DataMatrix
import pandas as pd
from .get_data import get_dye_data

# creates a data matrix from a link, saves to file to be printed
def gen_matrix(url: str, filename: str = "datamatrix_code.svg"):
    dm = DataMatrix(url)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(dm.svg())

    print("Data Matrix saved successfully!")
    
def gen_all_matrix():
    data = get_dye_data()
    for row in data.itertuples(index=False):
        url = ""
        if type(row.itemId) is not str:
            url = row.dye
        else:
            url = row.itemId
        print(url)
        filename = f"../datamatrix/datamatrix_{url}.svg"
        gen_matrix(url, filename)