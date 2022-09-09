from flask import Flask
from flask_restful import Resource, reqparse
from models.item_model import ItemModel

class Item(Resource):
    parser= reqparse.RequestParser()
    parser.add_argument("price", type= float, required= True, help= "This field cannot be left blank!")
    parser.add_argument("store_id", type= int, required= True, help= "Every item needs a store id")   
    
    def get(self, name):
        item= ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404
    
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with name '{}' already exists.".format(name)}, 400
        
        data= Item.parser.parse_args()
        item_model= ItemModel(name, **data)
        try: 
            item_model.save_to_db()
            return item_model.json(), 201
        except:                                    
            return {"message": "An error occured while inserting item"}, 500
    
    def delete(sele, name):
        item= ItemModel.find_by_name(name)
        if item:
            try:
                ItemModel.delete_from_db(name)
            except :
                return {"message": "Item not deleted."}
        return {"message": "Item deleted."}
    
    def put(self, name):        
        data= Item.parser.parse_args()        
        item= ItemModel.find_by_name(name)
        if item is None:
            item= ItemModel(name, **data)
        else:
            item.price= data["price"]
            item.store_id= data["store_id"]
        
        item.save_to_db()       
        return item.json()


class ItemList(Resource):
    def get(self):
        return {"items":list(map(lambda item: item.json(), ItemModel.query.all()))}
        #return {"items":[item.json() for item in ItemModel.query.all()] }