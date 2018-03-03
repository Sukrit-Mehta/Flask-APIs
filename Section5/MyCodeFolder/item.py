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

		try:				
			self.insert(item)
		except:
			return {"message" : "An error occured while inserting item."}, 500 # internal server error.
		return item,201       #convey to use rthat item is created.
							  #201 code for created


	@classmethod 
	def insert(cls,item):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		insert_query = "INSERT INTO items VALUES(?, ?)"
		cursor.execute(insert_query,(item['name'],item['price']))

		connection.commit()
		connection.close()



	def  delete(self,name):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		delete_query = "DELETE FROM items WHERE name=?"
		cursor.execute(delete_query,(name,))
		connection.commit()
		connection.close()
		return {'message':'Item deleted..!'}


	def put(self,name):
		
		data = Item.parser.parse_args()

		item = self.find_by_name(name)
		updated_item = {'name':name,'price':data['price']}

		if item is None:
			try:
				self.insert(updated_item)
			except:
				return {"message" : "An error occured in inserting the item."}, 500
		else:
			try:
				self.update(updated_item) #dictionaries have update methods
			except:
				return {"message" : "An error occured in updating the item."}, 500
		return updated_item

	@classmethod
	def update(cls,item):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		update_query = "UPDATE items SET price =?  WHERE name=?"
		cursor.execute(update_query,(item['price'],item['name']))
		connection.commit()
		connection.close()


class ItemList(Resource):
	def get(self):
		connection = sqlite3.connect("data.db")
		cursor = connection.cursor()
		fetch_list_query = "SELECT * FROM items"
		result = cursor.execute(fetch_list_query)

		items = []

		for row in result:
			items.append({'name':row[0],'price':row[1]})

		connection.close()

		return {'items':items}