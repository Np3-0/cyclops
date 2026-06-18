from firebase_admin import firestore
from fastapi import FastAPI, HTTPException
import helpers

helpers.init()
db = firestore.client()
app = FastAPI()

@app.get("/dyes")
def get_all_dyes():
    try:
        dyes_ref = db.collection("dyes")
        docs = dyes_ref.stream()
        all_users = {doc.id: doc.to_dict() for doc in docs}
        return all_users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dyes/{dye_id}")
def get_dye(dye_id: str):
    try:
        dye_ref = db.collection("dyes").document(dye_id)
        doc = dye_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            raise HTTPException(status_code=404, detail="Dye not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/dyes/{dye_id}")
def update_dye(dye_id: str, dye_data: dict):
    try:
        dye_ref = db.collection("dyes").document(dye_id)
        dye_ref.set(dye_data, merge=True)
        return {"message": "Dye updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))