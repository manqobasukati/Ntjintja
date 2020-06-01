from flask import Flask, jsonify, request, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask.ext.admin.contrib.sqla import ModelView

import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config["SECRET_KEY"] = "tHIS IS SCRET"

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(BASE_DIR, 'todo.sqlite')

db = SQLAlchemy(app)

admin = Admin(app)
 
 
class Transact(db.Model):
	__tablename__ = 'transactions'
	id = db.Column(db.Integer, primary_key=True)
	from_number = db.Column(db.Integer)
	to_number = db.Column(db.Integer)
	amount_sent = db.Column(db.Integer)
	charge_amount = db.Column(db.Integer)
	resent_amount =  db.Column(db.Integer)
	recipient_network = db.Column(db.String(30))
	dialled = db.Column(db.Boolean, default=False)
	
	
db.create_all()

class TransactView(ModelView):
	column_display_pk = True
	column_hide_backrefs = False
	column_list = ('id','from_number','to_number','amount_sent','recipient_network','resent_amount','dialled')

admin.add_view(TransactView(Transact, db.session))

@app.route("/transactions/swazi-mobile", methods=["GET"])
def get_swazi_mobile():
	transactions = Transact.query.filter_by(recipient_network='mtn').all()
	output = []
	
	for transaction in transactions:
		transact_data = {}
		transact_data['id'] = transaction.id
		transact_data['from_number']  = transaction.from_number
		transact_data['to_number'] = transaction.to_number
		transact_data['charge_amount'] = transaction.charge_amount
		transact_data['amount_sent'] = transaction.amount_sent
		transact_data['resent_amount'] = transaction.resent_amount
		transact_data['dialled'] = transaction.dialled
		output.append(transact_data)
		
	return jsonify({'output':output})
	
	
	

@app.route("/transactions/swazi-mobile", methods=["POST"])
def create_transaction_swazi():
	data = request.get_json(silent=False)
	charge = 0
	resend_amount = 0
	
	print data
	if int(data["amount_sent"]) <= 20:
		charge = 1
		resend_amount = int(data["amount_sent"]) - charge
	elif int(data["amount_sent"]) >= 21 and int(data["amount_sent"]) <= 30:
		charge = 2
		resend_amount = int(data["amount_sent"]) - charge
	elif int(data["amount_sent"]) >= 31 and int(data["amount_sent"]) <= 40:
		charge = 3
		resend_amount = int(data["amount_sent"]) - charge
	elif int(data["amount_sent"]) >= 41 and int(data["amount_sent"]) <= 50:
		charge = 4
		resend_amount = int(data["amount_sent"]) - charge
	elif int(data["amount_sent"]) >= 51 and int(data["amount_sent"]) <= 100:
		charge = 5
		resend_amount = int(data["amount_sent"]) - charge
		
		
		
	transaction = Transact(from_number=data["from_number"],to_number=data["to_number"], 
					amount_sent=data["amount_sent"], charge_amount=charge, 
					resent_amount=resend_amount, recipient_network=data['recipient_network'])
	
	db.session.add(transaction)
	db.session.commit()
	
	return jsonify({"message":"Transaction sent"})
	


@app.route("/transactions/mtn", methods=["GET"])
def get_swazi_mtn():
	transactions = Transact.query.filter_by(recipient_network='swazi-mobile').all()
	output = []
	
	for transaction in transactions:
		transact_data = {}
		transact_data['id'] = transaction.id
		transact_data['from_number']  = transaction.from_number
		transact_data['to_number'] = transaction.to_number
		transact_data['charge_amount'] = transaction.charge_amount
		transact_data['amount_sent'] = transaction.amount_sent
		transact_data['resent_amount'] = transaction.resent_amount
		transact_data['dialled'] = transaction.dialled
		output.append(transact_data)
		
	return jsonify({'output':output})



@app.route("/transactions/mtn", methods=["POST"])
def create_transaction_mtn():
	data = request.get_json()
	charge = 0
	resend_amount = 0
		
	if int(data["amount_sent"]) <= 20:
		charge = 1
		resend_amount = int(data["amount_sent"]) - charge
	elif int(data["amount_sent"]) >= 21 and int(data["amount_sent"]) <= 30:
		charge = 2
		resend_amount = int(data["amount_sent"]) - charge
	elif int(data["amount_sent"]) >= 31 and int(data["amount_sent"]) <= 40:
		charge = 3
		resend_amount = int(data["amount_sent"]) - charge
	elif int(data["amount_sent"]) >= 41 and int(data["amount_sent"]) <= 50:
		charge = 4
		resend_amount = int(data["amount_sent"]) - charge
	elif int(data["amount_sent"]) >= 51 and int(data["amount_sent"]) <= 100:
		charge = 5
		resend_amount = int(data["amount_sent"]) - charge
	print data
		
	transaction = Transact(from_number=data["from_number"],to_number=data["to_number"], 
					amount_sent=data["amount_sent"], charge_amount=charge, 
					resent_amount=resend_amount, recipient_network=data['recipient_network'])
	
	db.session.add(transaction)
	db.session.commit()
	
	return jsonify({"message":"Transaction sent"})
	

@app.route("/" ,methods=["GET"])
def appp():
	return jsonify({"message":"app"})
	
	
@app.route("/transactions/<transaction_id>", methods=["PUT"])
def update_dialled(transaction_id):
	transaction = Transact.query.filter_by(id=transaction_id).first()
	transaction.dialled = True
	db.session.commit()
	return jsonify({"message":"updated"})
	
@app.route("/sms-transaction/<phone_number>",methods=["PUT"])
def func(phone_number):
	data = request.get_json()
	transaction = Transact.query.filter_by(from_number=phone_number).first()
	
	transaction.real_amount = data["real_amount"]
	if transaction.real_amount >= transaction.amount_sent:
		transaction.sufficient = True
		db.session.commit()
	else:
		transaction.sufficient = False
		db.session.commit()
	
	return jsonify({"message":"real-amount-updated"})
	

		
	
	
if __name__ == '__main__':
	app.run(debug=True,port=8080)




	
	
	

