from pymongo import MongoClient
client = MongoClient()   
db=client.test				# test is database name
col=db.store				# store is the collection name in mongo

#Insert Data in Mongo
result=col.insert_one({"Ankit":"HelloWorld"});		# Insert json in mongo
print(result.inserted_id)							# print the _id


# Query data from Mongo
result=col.find_one({"Ankit":"HelloWorld"});		# Query my data to find 
print(result)


# Query multiple data from Mongo
result=col.find({"Ankit":"HelloWorld"});	 		# Return cursor		
for re in result:
	print(re)
