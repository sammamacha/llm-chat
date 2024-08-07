import pymongo

class Memory:
    _DEFAULT_UNCONSCIOUS = "Nothing yet. It's moldable. Talk about whatever you want and BE whatever you want."
    def __init__(self, db, ip = "mongodb://localhost:27017/"):
        self.client = pymongo.MongoClient(ip)
        self.memory = self.client[db]
        names = self.memory.list_collection_names()

        if "messages" not in names: 
            self.memory.create_collection("messages")
        
        if "unconscious" not in names:
            self.memory.create_collection("unconscious")

    def set_unconscious(self, user : str, info : str): 
        self.memory["unconscious"].update_one({"name" : user}, { "$set" : {"info" : info}})

    def get_unconscious(self, user : str): 
        result = self.memory["unconscious"].find_one({"name" : user})

        if result == None:
            self.memory["unconscious"].insert_one({"name" : user, "info" : self._DEFAULT_UNCONSCIOUS})
            return self._DEFAULT_UNCONSCIOUS
        return result["info"]


    def push_message(self, user : str, message : str):
        self.memory["messages"].insert_one({"user" : user, "content" : message})

    def get_recent_messages(self, max = 32, max_chars = 8192): 
        messages = self.memory["messages"].\
            find().\
            sort('_id', -1).\
            limit(max)
    
        bucket = [] 
        messages = list(messages)
        
        chars = 0 
        for message in messages: 
            if len(message) + chars > max_chars: 
                break 

            bucket.append(message)

        bucket.reverse()

        return bucket

