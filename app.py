from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from db import db
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList # Implementation of store List

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)
# We dont need to do jsonify with Flask-RESTful because it already does for us.
# items = [] # in-memory database



api.add_resource(Item, '/item/<string:name>') 
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
# we dont want to run the app when its imported by any other file.
# we always want to run the file because its the starting point of our app.
# if we are importing app we likely don't want to run the app.
if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
