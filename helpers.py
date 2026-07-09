import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

# Path to your downloaded private key file
cred = credentials.Certificate("service_key.json")

# Initialize the default app
def init():
    firebase_admin.initialize_app(cred)
    
def upload_csv():
    df = pd.read_csv('antibodies.csv')
    db = firestore.client()
    
    for row in df.itertuples(index=False):
        print(row.Name)
        data = {
            "name": row.Name,
            "vendor": row.Vendor,
            "catalog_num": row.Catalog_Number,
            "date_received": row.Date_Received,
            "quantity": row.Quantity,
            "unit": row.Unit,
            "description": row.Description,
            "expiration_date": row.Expiration_Date,
            "lot_number": row.Lot_Number,
            "notes": row.Notes,
            "storage_location_top": row.Storage_Location_Top,
            "storage_location_freezer_box_cells": row.Storage_Location_Freezer_Box_Cells,
            "url": row.URL,
            "id": row.ID,
            "antigen": row.Antigen,
            "clonality": row.Clonality,
            "clone": row.Clone,
            "conjugation": row.Conjugation,
            "primary_or_secondary": row.Primary_Or_Secondary,
            "raised_in": row.Raised_In,
            "recognizes": row.Recognizes
        }
        # Replace NaN values with None for API calls
        data = {k: None if pd.isna(v) else v for k, v in data.items()}
        db.collection("dyes").document(row.ID).set(data)