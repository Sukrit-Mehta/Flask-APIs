from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate,identity

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app) 

jwt = JWT(app, authenticate, identity) #JWT creates a new endpoint->  /auth

items = [] #contains dictionary for each item
 
#Every resouce has to be a class
#class Item(Resource):
	# def get(self, name):
	# 	for item in items:
	# 		if(item['name']==name):
	# 			return item
	# 	return {'name': None},404  
# Python methods return None by default		return None

#	def post(self,name):
#		request_data = request.get_json(force=True)  
#force=True means even if the sent data is not in Json format 
#then it will reformat the data on its own, and hence will not throw any errors.
#Header not required if this is used.

#OR use silent=True   ->it returns None on getting error

class Item(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('price',
			type=float,
			required=True,
			help="This field cannot be left blank !"
			)

	@jwt_required()
	def get(self,name):
		item = 	next(filter(lambda x: x['name']==name,items), None)
		return {'item':item}, 200 if item else 404    

	def post(self,name):
		if next(filter(lambda x: x['name']==name,items), None) is not None:
			return {'message':"An item with name'{}'already exists.".format(name)},400 #bad request

#		data = request.get_json()
		data = Item.parser.parse_args()
		item = {'name':  name,
				'price': data['price']}
		items.append(item)
		return item,201       #convey to use rthat item is created.
							  #201 code for created

	def  delete(self,name):
		global items
		items = list(filter(lambda x: x['name'] !=name, items))
		return {'message':'Item deleted..!'}


	def put(self,name):
		
		data = Item.parser.parse_args()
		item = next(filter(lambda x: x['name'] == name,items),None)
		if item is None:
			item = {'name':name,
			'price':data['price']}
			items.append(item)
		else:
			item.update(data) #dictionaries have update methods
		return item


class ItemList(Resource):
	def get(self):
		return {'items':items}

api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')

app.run(port=5000, debug=True)