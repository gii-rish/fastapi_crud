from pymongo import MongoClient

# client = MongoClient("mongodb://localhost:27017/")
# db = client["cryptodb"]
# collection = db["currency"]

def searializer(obj) -> dict:
    response = {}
    for value in obj:
        if value == "_id":
            response.update({"id": str(obj[value])})
        else:
            response.update({value: obj[value]})
    
    return response