import requests, re, json
import pandas as pd
import pymupdf

def get_dye_data():
    req = requests.get("https://merlin.floot.app/_api/kite/antibodies?databaseId=2")
    data = req.json()
    data.pop('meta', None)
    formatted = data['json']['antibodies']
    return pd.DataFrame(formatted)

def get_dye_from_info(marker: str, dye: str, box: str):
    data = get_dye_data()
    results = data[(data['marker'] == marker) & (data['dye'] == dye) & (data['box'].lower() == box.lower())]
    return results.to_dict(orient='records') 

def get_sequence_data():
    pass

def get_data_from_matrix(data: pd.DataFrame, id):
    match = data[data['itemId'] == id]
    if match.empty:
        match = data[data['dye'] == id]
    if match.empty:
        return None
    
    return match.iloc[0].to_dict()

def get_data_from_pdf(path: str):
    VOL = re.compile(r"^([\d.]+)\s*[µμ]L$")          # micro sign or Greek mu
    STEP_HDR = re.compile(r"^Step (\d+)(?:\s+(.+))?$")  # "Step 1" or "Step 1 Surface Stain C"
    STEP_ROW = re.compile(r"^(\d+)\.\s+(.+)$")
    FOOTER = re.compile(r"^(\d+/\d+/\d+, .*|Flare · Merlin|https?://.*|\d+/\d+)$")
    HEADERS = {"Surface", "Intracellular", "Marker", "Dye", "Box", "Address",
               "Step", "Done"}

    with pymupdf.open(path) as doc:
        text = "\n".join(page.get_text() for page in doc)

    # strip radio-circle glyphs, blank lines, and page headers/footers
    lines = [l.lstrip("○◯ ").strip() for l in text.splitlines()]
    lines = [l for l in lines if l and not FOOTER.match(l)]

    out = {"steps": []}
    step, buf, i = None, [], 0

    while i < len(lines):
        line = lines[i]

        if line.startswith("Database:"):
            out["database"] = line.split(":", 1)[1].strip()
        elif line.startswith("Printed"):
            out["printed"] = line.removeprefix("Printed").strip()
        elif m := re.match(r"Samples: (\d+).*Multiplier: ([\d.]+)", line):
            out["samples"] = int(m[1])
            out["multiplier"] = float(m[2])

        elif m := STEP_HDR.match(line):
            if m[2]:    # name on the same line as "Step N"
                name, type_, skip = m[2], lines[i + 1], 1
            else:       # name and type on their own lines
                name, type_, skip = lines[i + 1], lines[i + 2], 2
            step = {"step": int(m[1]), "name": name, "type": type_,
                    "reagents": [], "totals": {}}
            out["steps"].append(step)
            buf, i = [], i + skip

        elif (step is None or line in HEADERS
              or line.startswith("Optimal Volume")
              or line.startswith("Marker Dye")):
            pass

        elif m := re.match(r"(\d+) antibodies$", line):
            step["antibody_count"] = int(m[1])
            buf = []

        elif m := VOL.match(line):
            if i + 1 < len(lines) and STEP_ROW.match(lines[i + 1]):
                # reagent row: buf holds marker, [IC], dye, [box], [address]
                if buf:
                    marker, rest = buf[0], buf[1:]
                    ic = bool(rest) and rest[0] == "IC"
                    if ic:
                        rest = rest[1:]
                    step["reagents"].append({
                        "marker": marker,
                        "intracellular": ic,
                        "dye": rest[0] if rest else None,
                        "box": rest[1] if len(rest) > 1 else None,
                        "address": rest[2] if len(rest) > 2 else None,
                        "volume_ul": float(m[1]),
                        "step_label": lines[i + 1],
                    })
                i += 1  # skip step label line
            else:
                # summary row: the label is the previous line
                step["totals"][lines[i - 1]] = float(m[1])
            buf = []
        else:
            buf.append(line)

        i += 1
    return out
    
if __name__ == "__main__":
    data = get_data_from_pdf("../data/test_pdf.pdf")
    print(data["multiplier"]) 