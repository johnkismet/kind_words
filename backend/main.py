import pymongo
import datetime

# Replace the uri string with your MongoDB deployment's connection string.
conn_str = "mongodb+srv://Kismet:wZ0vNyvkUENVhg2o@kind-words-cluster.l8p7d.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

# set a 5-second connection timeout
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
db = client['kind_words-database']
kw_coll = db['kind-words-collection']
# req_coll = db['requests-collection']
# user_coll = db['users-collection']
post = {"author": "Mike",
         "text": "My first blog post!",
         "tags": ["mongodb", "python", "pymongo"],
         "date": datetime.datetime.utcnow()}
kw_coll.insert_one(post)

try:
    print('connected to mongoDB')
except Exception:
    print("Unable to connect to the server.")