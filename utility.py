import pymongo

client = pymongo.MongoClient("mongodb://%s:%s@%s:27017/" % ("root", "password", "localhost"))
db = client.iot

# db.drop_collection("polygonscan")
# db.drop_collection("ftmscan")
# db.drop_collection("snowtrace")
# db.drop_collection("bscscan")

# db.create_collection("polygonscan")
# db.create_collection("ftmscan")
# db.create_collection("snowtrace")
# db.create_collection("bscscan")

print(db.list_collection_names())