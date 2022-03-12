'''
Testing Mongodb using pymongo
'''

from http import client
import pymongo

if __name__ =="__main__":
    #print("Pymongo for mongodb")
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    #print(client)
    db = client['test']

