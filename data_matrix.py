from ppf.datamatrix import DataMatrix
import pandas as pd

# creates a data matrix from a link, saves to file to be printed
def gen_matrix(url: str, filename: str = "datamatrix_code.svg"):
    dm = DataMatrix(url)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(dm.svg())

    print("Data Matrix saved successfully!")
    
def gen_all_matrix():
    df = pd.read_csv('antibodies.csv')
    for row in df.itertuples(index=False):
        url = row.ID
        filename = f"datamatrix/datamatrix_{row.ID}.svg"
        gen_matrix(url, filename)