# from pydantic import BaseModel
from bson import ObjectId
import json
import pymongo

from fastapi import FastAPI
import uvicorn
from serialization.serializer import serializer
from models.models import CryptoCurrency
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


app = FastAPI()

db = "cryptodb"
collection = "currency"

#get all the available crypto currencies.
@app.get("/", response_description="Get all the currencies")
async def get_currencies():
    currency_list = []
    
    with pymongo.MongoClient("mongodb://root:rootpassword@host.docker.internal:27017/") as client:
        currency_collection = client[db][collection]
        currencies = currency_collection.find()
        
        for i in currencies:
            currency_list.append(serializer(i))        
    return JSONResponse(status_code=200, content=currency_list)


#get a particular crypto, provided the id.
@app.get("/{id}", response_description="Get a single currency", response_model=CryptoCurrency)
async def get_currency(id: str):
    
    with pymongo.MongoClient("mongodb://root:rootpassword@host.docker.internal:27017/") as client:
        currency_collection = client[db][collection]
        
        if (currency := currency_collection.find_one({"_id": ObjectId(id)})) is not None:            
            return JSONResponse(status_code=200, content=serializer(currency))

    raise HTTPException(status_code=404, detail=f"Currency with id - {id} not found")


#add a brand new set of crypto.
@app.post("/", response_description="Add new Crypto", response_model=CryptoCurrency)
async def add_crypto(request: CryptoCurrency):
    currency = jsonable_encoder(request)
    
    with pymongo.MongoClient("mongodb://root:rootpassword@host.docker.internal:27017/") as client:
        currency_collection = client[db][collection]
        new_entry = currency_collection.insert_one(currency)
        created_currency = currency_collection.find_one({"_id": new_entry.inserted_id})
        return JSONResponse(status_code=201, content=serializer(created_currency))
    
    raise HTTPException(status_code=500, detail="Internal server error")


#update any crypto, provided the id.
@app.put("/{id}", response_description="Update Crypto", response_model=CryptoCurrency)
async def update_currency(id: str, request: CryptoCurrency):
    currency = {k: v for k, v in request.dict().items()}        

    if currency:
        with pymongo.MongoClient("mongodb://root:rootpassword@host.docker.internal:27017/") as client:
            currency_collection = client[db][collection]
            update_result = currency_collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": currency})              

            if update_result:
                if (updated_currency := currency_collection.find_one({"_id": ObjectId(id)})) is not None:
                    return JSONResponse(status_code=201, content=serializer(updated_currency))
                
            raise HTTPException(status_code=500, detail="Internal server error")

    raise HTTPException(status_code=404, detail=f"Currency with id - {id} not found")


#delete a currency for the given id
@app.delete("/{id}", response_description="Delete a currency")
async def delete_currency(id: str):
    with pymongo.MongoClient("mongodb://root:rootpassword@host.docker.internal:27017/") as client:
        currency_collection = client[db][collection]
        delete_result = currency_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=204)

    raise HTTPException(status_code=404, detail=f"Currency with id - {id} not found")


if __name__ == "__main__":
    
    try:
        client = pymongo.MongoClient("mongodb://root:rootpassword@host.docker.internal:27017/")
        print("Connected")
    except Exception as e:
        print(e)
        
    db = client["cryptodb"]
    collection = db["currency"]

    with open('fetchTickers.json', 'r') as f:
        data = json.loads(f.read())        
        
        for i in data.keys():        
            collection.insert_one(data[i])
            
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)