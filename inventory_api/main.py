from firebase_admin import firestore
from fastapi import FastAPI, Depends, HTTPException, Header
from pyrate_limiter import Duration, Limiter, Rate
from fastapi_limiter.depends import RateLimiter
import helpers as helpers

helpers.init()
db = firestore.client()
app = FastAPI()

# get all dyes, 1 req per 10 secs
@app.get(
    "/dyes", 
    dependencies=[Depends(RateLimiter(limiter=Limiter(Rate(1, Duration.SECOND * 10))))]
)
async def get_all_dyes():
    try:
        dyes_ref = db.collection("dyes")
        docs = dyes_ref.stream()
        all_users = {doc.id: doc.to_dict() for doc in docs}
        return all_users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# get a single dye via ID, 2 req per 5 secs
@app.get(
    "/dyes/{dye_id}",
    dependencies=[Depends(RateLimiter(limiter=Limiter(Rate(2, Duration.SECOND * 5))))]
)
async def get_dye(dye_id: str):
    try:
        dye_ref = db.collection("dyes").document(dye_id)
        doc = dye_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# update dye info via ID, 2 req per 5 secs
@app.patch("/dyes/update/{dye_id}")
async def update_dye(dye_id: str, dye_data: dict):
    try:
        dye_ref = db.collection("dyes").document(dye_id)
        dye_ref.set(dye_data, merge=True)
        return {"message": "Dye updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# delete dye info via ID, 2 req per 5 secs - be careful with
@app.delete("/dyes/delete/{dye_id}")
async def delete_dye(dye_id: str):
    try:
        dye_ref = db.collection("dyes").document(dye_id)
        dye_ref.delete()
        return {"message": "Dye deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))