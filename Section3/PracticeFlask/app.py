from flask import Flask, jsonify, request, render_template  #Flask : Class ; flask : package

app = Flask(__name__) #gives each file a unique name

#tell the app which requests we'll send

#decorator


# POST - used to receive data
# GET - used to send data back only

 
#@app.route('/') #end point .... #home page of site : 'http:www.google.com/'
#def home():
#	return "Hello world..!"


stores = [
	{
		'name' : 'My Wonderful Store',
		'items': [
			{
			'name':'My Item',
			'price':24.22
			}
		]
	}
]


@app.route('/')
def home():
	return render_template('index.html')

# POST /store data: {name:}
@app.route('/store', methods=['POST']) #fetching data from web
def create_store():
	request_data = request.get_json()
	new_store = {
		'name' : request_data['name'],
		'items': []
	}
	stores.append(new_store)
	return jsonify(new_store)

# GET /store/<string:name>
@app.route('/store/<string:name>')
def get_store(name):
	# iterate over stores
	# if the store name matches, return it
	# if none match, return an error message
	for store in stores:
		if store['name'] == name:
			return jsonify(store)
	return jsonify({'message':'store not found'})

# GET /store
@app.route('/store')
def get_stores():
	return jsonify({'stores':stores}) #dictionary

# POST /store/<string:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
	request_data = request.get_json()
	for store in stores:
		if store['name'] == name:
				new_item = {
				'name' : request_data['name'],
				'price' : request_data['price'] 
				}
				store['items'].append(new_item)
				return jsonify(new_item)
	return jsonify({'message':'store not found'})

# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
	for store in stores:
		if store['name'] == name:
			return jsonify({'items': store['items']})
	return jsonify({'message':'store not found'})

app.run(port=5000)  #port no.