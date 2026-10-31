from ppf.datamatrix import DataMatrix
from pathlib import Path
from .get_data import get_dye_data

OUT_DIR = Path(__file__).resolve().parent.parent / "datamatrix"

# creates a data matrix from a link, saves to file to be printed
def gen_matrix(data: str, filename):
    dm = DataMatrix(data)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(dm.svg())

def gen_all_matrix():
    OUT_DIR.mkdir(exist_ok=True)
    for row in get_dye_data().itertuples(index=False):
        code = row.itemId if isinstance(row.itemId, str) else str(row.id)
        print(code)
        gen_matrix(code, OUT_DIR / f"datamatrix_{code}.svg")

if __name__ == "__main__":
    gen_all_matrix()