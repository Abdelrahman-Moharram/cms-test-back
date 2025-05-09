from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
from  os import getenv

class MongoDB:
    connection      = getenv('MONGODB')

    
    def select(self, collection_name, query):
        collection  = self.connection[collection_name]
        
        return collection.find_one(query)
    

    def get_page_by_id(self, id):
        return self.select('page', {'_id': id})


    def get_page_data_by_id(self, id):
        content = self.select('content', {'page': id})









        

    def create_collection(self, name, schema):
        try:
            self.connection.create_collection(
                name,
                validator={'$jsonSchema': schema},
                validationLevel='strict',
                validationAction='error'
            )
            print("Collection created with schema validation.")
        except Exception as e:
            print(f"Collection creation failed or already exists: {e}")
    
    

