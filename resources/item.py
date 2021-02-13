import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price', type=float, 
        required=True, 
        help="This field cannot be left blank")
    parser.add_argument(
        'store_id', type=int,
        required=True,
        help="Every item needs a store_id"
    )
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
    
        return {"message": "Item not found"}, 400
    
    def post(self, name):
        
        data = Item.parser.parse_args()
        if ItemModel.find_by_name(name):
            return {"message": "An item with this name already exists"}, 400
        
        item = ItemModel(name, data['price'], data['store_id'])
        # item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occured while inserting the item."}, 500
            # 500 for internal server error.


        return item.json(), 201 
        # Remember to always return an json and not an object data.
        # For the application to know that the item is created.
        # 201 CREATED
        # 202 ACCEPTED 
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'}
        else:
            return {'message': 'Item not found'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'])
        else:
            item.price = data['price']
        
        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()] }
        # return { 'items': list(map(lambda x: x.json, ItemModel.query.all()))}