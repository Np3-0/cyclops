from ppf.datamatrix import DataMatrix

# creates a data matrix from a link, saves to file to be printed
def gen_matrix(url: str):
    dm = DataMatrix(url)

    with open("datamatrix_code.svg", "w", encoding="utf-8") as f:
        f.write(dm.svg())

    print("Data Matrix saved successfully!")