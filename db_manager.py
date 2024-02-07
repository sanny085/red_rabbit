from pymongo import MongoClient
from datetime import datetime
import json
from dotenv import load_dotenv
import os 
from bson import ObjectId
load_dotenv()
class db_manager():
    def __init__(self, data,db_name,table_name,logger):
        self.logger = logger
        self.data = data
        os.environ.get("DB_URL")
        os.environ.get("DB_PORT")
        self.client = MongoClient(os.environ.get("DB_URL") + os.environ.get("DB_PORT"),serverSelectionTimeoutMS=10000)
        print("passesd mongo client")
        print(self.client)
        self.db_name = db_name
        print(self.db_name)
        self.table_name= table_name


    def insert_data(self):
        print("db_manager: started pushing record to db")
        db = self.client[self.db_name]
        collection = db[self.table_name]
        target_id = self.data["_id"]             # need to update based on the type of the data ObjectId(self.data["_id"])
        if collection.find_one({"_id": target_id}):
            update_query = {"$set": {"coordinates": self.data["coordinates"]}}
            collection.update_one({"_id": target_id}, update_query)
            print("db_manager: record found : updated the record")
            return "updated the record"
        else:            
            collection.insert_many([self.data])
            print("db_manager: new record found : inserted the record")
            return "inserted the record"
            
    def search_data(self,column_name,search_id):
        db = self.client[self.db_name]
        collection = db[self.table_name]
        print("db_manager: search_data :searching the target record")
        try: #true if the records are avilable and records will get updates
            xy_coords = collection.find_one({column_name :search_id})['coordinates']
            print("db_manager: search_data :fetching xy_coords")
            return xy_coords
        except Exception as err: 
            return "unable to fetch records from db "+ err

        
        
    def get_db_details(self):
        list_of_db = self.client.list_database_names()
        print(list_of_db)

    def clear_db(self):
        table_data = self.collection.delete_many({})
        return table_data.deleted_count, " documents deleted."




