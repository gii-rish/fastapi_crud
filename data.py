import json
import pymongo

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
