from pymongo import MongoClient

def serializer(obj) -> dict:
    response = {}
    for value in obj:
        if value == "_id":
            response.update({"id": str(obj[value])})
        else:
            response.update({value: obj[value]})
    
    return response