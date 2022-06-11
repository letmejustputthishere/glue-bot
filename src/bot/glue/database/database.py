from turtle import up
from pymongo.mongo_client import MongoClient
from typing import TypedDict, Literal, Optional


class Canister(TypedDict):
    canister_id: str
    standard: Literal['ext', 'dip721']
    min: int
    max: Optional[int]
    name: str
    users: list[int]


class GlueGuild(TypedDict):
    server_id: int
    canisters: list[Canister]


class Database:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.db
        self.collection = self.db.collection

    def insert(self, document: GlueGuild):
        # if the document already exists, update it
        if self.collection.find_one({"server_id": document['server_id']}):
            self.collection.update_one(
                {"server_id": document['server_id']},
                {"$push":
                    # we have to use the first element of the list, otherwise we have nested lists
                    {"canisters": document['canisters'][0]}
                 })
        else:
            self.collection.insert_one(document)   # type: ignore

    def find(self, query):
        return self.collection.find(query)

    def find_one(self, query):
        return self.collection.find_one(query)

    def update(self, query, update):
        self.collection.update_one(query, update)

    def delete_server(self, query):
        return self.collection.delete_one(query)

    def delete_canister(self, guild_id, canister_id):
        return self.collection.update_one(
            {"server_id": guild_id},
            {"$pull":
             {"canisters":
              {"canister_id": canister_id}
              }
             })
