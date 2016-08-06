from pymongo import MongoClient
client = MongoClient()
db=client.test
col=db.store
result=col.insert_one({"Ankit":"HelloWorld"});
print(result.inserted_id)