from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app) 

items = [] #contains dictionary for each item

#Every resouce has to be a class
class Item(Resource):
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

	
	def get(self,name):
		item = 	next(filter(lambda x: x['name']==name,items), None)
		return {'item':item}, 200 if item else 404    

	def post(self,name):
		if next(filter(lambda x: x['name']==name,items), None) is not None:
			return {'message':"An item with name'{}'already exists.".format(name)},400 #bad request

		data = request.get_json()
		item = {'name':  name,
				'price': data['price']}
		items.append(item)
		return item,201       #convey to use rthat item is created.
							  #201 code for created


class ItemList(Resource):
	def get(self):
		return {'items':items}

api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')

app.run(port=5000, debug=True)