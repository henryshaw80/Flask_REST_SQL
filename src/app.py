__author__ = 'Timur'

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from src.security import authenticate, identity

#__name__ is unique name of the file that runs app
app = Flask(__name__)
app.secret_key = 'timur'
api = Api(app)

# JWT creates a new end point '/auth'
# when it reach '/auth', app will send username and password
# jwt token can be send to next request since it has been
# authenticated and validated.
jwt = JWT(app, authenticate, identity)

# internal memory
items = []

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    # only price that can be parsed, any other argument will be ignored
    # To require a value be passed for an argument, just add required=True

    @jwt_required()  # decorator with argument to authenticate
    def get(self, name):
        #for item in items:
        #    if item['name'] == name:
        #        return item
        # instead using for loop, one can use filter function
        # and next function to return the first item in the filter
        # next can raise error and break code if they cannot find item
        # thus, one set default value to be None.
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item is not None else 404

    def post(self, name):
        # deal with errors with filter function
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            # there is already an item matching the name
            return {'message': "An item with name '{}' already exist".format(name)}, 400

        # parse argument that comes through json payload
        # will put valid data in data
        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items #identify this variable belongs to outer of this block
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self,name):
        data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
        else:
            # using Flask reqparse to update
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return{'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)