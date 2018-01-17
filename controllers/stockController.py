from flask import request
from flask_restful import Resource, reqparse
from connection import Session
from models import Stock, GenericError
from utils import validationUtil

class StockListController(Resource):

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		
		self.reqparse.add_argument('name', type = str, 
			help='No stock name provided', required = True, location = 'json')
			
		self.reqparse.add_argument('description', type = str, required = True,
            help = 'No stock description provided', location = 'json')
			
		super(StockListController, self).__init__()

	def get(self):
		session = Session()
		stocks = session.query(Stock).all()
		
		res = []
		for s in stocks:
			res.append(s._asdict())
			
		return res
    
	def post(self):
		status = 200;
		
		if validationUtil.is_json(request.data):
			args = self.reqparse.parse_args(strict=True, custom=True)
			if args['error']:
				genericError = GenericError(0, list(args['body'].values()))
				res = genericError.__dict__
			else:
				
				name = request.json['name']
				description = request.json['description']
				
				errors = []
				if not name:
					errors.append('Name is empty')
					
				if not description:
					errors.append('Description is empty')
				
				if len(errors) <= 0:
					session = Session()
					
					newStock = Stock(request.json['name'], request.json['description'])
					session.add(newStock)
					session.flush()
					
					res = newStock._asdict()
					
					session.commit()
					session.close()
				else:
					genericError = GenericError(0, errors)
					res = genericError.__dict__
					status = 400
		else:
			errors.append('Not a valid JSON format')
			res = GenericError(0, errors).__dict__
			status = 400
			
		return res, status
		
class StockController(Resource):

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
			
		self.reqparse.add_argument('name', type = str, 
			help='No stock name provided', required = True, location = 'json')
		
		self.reqparse.add_argument('name', type = str, 
			help='No stock name provided', required = True, location = 'json')
			
		self.reqparse.add_argument('description', type = str, required = True,
            help = 'No stock description provided', location = 'json')
			
		super(StockController, self).__init__()

	def put(self, id):
		status = 200
		
		if(validationUtil.is_json(request.data)):
			args = self.reqparse.parse_args(strict=True, custom=True)
			if args['error']:
				genericError = GenericError(0, list(args['body'].values()))
				res = genericError.__dict__
			else:
				name = request.json['name']
				description = request.json['description']
				
				errors = []
				if not name:
					errors.append('Name is empty')
					
				if not description:
					errors.append('Description is empty')
					
				if len(errors) <= 0:
					session = Session()
			
					updatedStock = session.query(Stock).filter_by(id = id).first()
					
					if updatedStock: #if stock exists, update it
						name = request.json['name']
						description = request.json['description']
						
						updatedStock.name = name
						updatedStock.description = description
						
						res = updatedStock._asdict()
						
						session.flush()
						session.commit()
						session.close()
					else:
						errors.append('Stock not found')
						status = 400
						res = GenericError(0, errors).__dict__
				else:
					genericError = GenericError(0, errors)
					res = genericError.__dict__
					status = 400
				
		else:
			errors.append('Not a valid JSON format')
			res = GenericError(0, errors).__dict__
			status = 400
		
		return res, status
		
	def delete(self, id):
		status = 200
		
		session = Session()
		deleteStock = session.query(Stock).filter_by(id = id).first()
		
		if deleteStock:
			session.delete(deleteStock)
			res = deleteStock._asdict()
			
			session.flush()
			session.commit()
			session.close()
		else:
			errors = []
			errors.append('Stock not found')
			status = 400
			res = GenericError(0, errors).__dict__
		
		return res, status