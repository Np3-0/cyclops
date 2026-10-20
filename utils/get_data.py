import requests
import pandas as pd

def get_dye_data():
    req = requests.get("https://merlin.floot.app/_api/kite/antibodies?databaseId=2")
    data = req.json()
    data.pop('meta', None)
    formatted = data['json']['antibodies']
    return pd.DataFrame(formatted)

def get_dye_from_info(marker: str, dye: str):
    data = get_dye_data()
    results = data[(data['marker'] == marker) & (data['dye'] == dye)]
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
