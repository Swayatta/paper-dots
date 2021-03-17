from pymongo import MongoClient

class MongoUtils():
    def __init__(self, db):
        client = MongoClient("mongodb://harshit158:Hs%40123021@cluster0-shard-00-00-iyydw.mongodb.net:27017,cluster0-shard-00-01-iyydw.mongodb.net:27017,cluster0-shard-00-02-iyydw.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
        self.db = client[db]

    def push(self, coll, doc):
        self.db[coll].insert_one(doc)

    def fetch_applicant(self, coll, query):
        return self.db[coll].find_one(query)

    def get_count(self, coll):
        return self.db.coll.count_documents({})

    def get_recent(self, coll):
        '''Fetches last added record from the collection'''
        records = list(self.db[coll].find().sort("_id", -1).limit(1))
        return records[0]