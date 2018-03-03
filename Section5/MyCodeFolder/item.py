import sqlite3

from flask_restful import Resource,reqparse
from flask_jwt import jwt_required

class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('price',
			type=float,
			required=True,
			help="This field cannot be left blank !"
			)

	@jwt_required()
	def get(self,name):
		   item = self.find_by_name(name)
		   if item:
		   		return item
		   return {"message":"Item not found"}, 404

	def find_by_name(self,name):
		   connection = sqlite3.connect('data.db')
		   cursor = connection.cursor()

		   query = "SELECT * FROM items WHERE name =?"
		   result = cursor.execute(query,(name,))
		   row = result.fetchone()
		   connection.close()

		   if row:
		   	  return {"item": {"name":row[0],"price":row[1]}}		


	def post(self,name):
		if self.find_by_name(name):
			return {'message':"An item with name'{}'already exists.".format(name)},400 #bad request

		data = Item.parser.parse_args()
		item = {'name':  name,
				'price': data['price']}
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		insert_query = "INSERT INTO items VALUES(?, ?)"
		cursor.execute(insert_query,(item['name'],item['price']))

		connection.commit()
		connection.close()

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
		connection = sqlite3.connect("data.db")
		cursor = connection.cursor()
		fetch_list_query = "SELECT * FROM items"
		result = cursor.execute(fetch_list_query)
		for row in result:
			print(row)
		return {'items':result}