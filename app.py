from flask import Flask
from flask_restful import Api
from connection import Session, Base, engine
import controllers

app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
Base.metadata.create_all(engine)

api = Api(app)

api.add_resource(controllers.StockListController, '/v1/stocks')
api.add_resource(controllers.StockController, '/v1/stocks/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)