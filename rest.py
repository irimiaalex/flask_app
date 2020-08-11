from flask import Flask, request
from flask_restful import Resource, Api,reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
api = Api(app)
app.secret_key = 'alex'

jwt = JWT(app, authenticate, identity) #/auth   --- new endopoint

#no need to return jsonify while using flask restful
items = []

#next() gives us the first item of the filter function
class  Item(Resource):
    def get(self,name):
        item = next(filter(lambda x: x['name'] == name, items), None) #filter() take 2 arg, I) the filter func II) the list we filter)
        return{'item' : item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message' : 'An item with name {} already exisits'.format(name)},400
        data = request.get_json()
        item = {'name': name, 'price' : data['price']}
        items.append(item)
        return item, 201 #status code for created

    def delete(self,name):
        global items
        items = list(filter(lambda x : x['name'] != name,items))
        return {'message' : 'Item deleted'}

    def put(self,name):

        data = request.get_json()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None :
            item = {'name' : name, 'price' : data['price'] }
            items.append(item)
        else :
            item.update(data)
        return item




class ItemList(Resource):
    def get(self):
        return{'items' : items}


api.add_resource(Item, '/item/<string:name>')# http://127.0.0.1:5000/student/Alex
api.add_resource(ItemList, '/items')
app.run(port=5000, debug = True)