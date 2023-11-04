from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_cors import CORS
from flask_migrate import Migrate

app = Flask(__name__)
CORS(app) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza_restaurant.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Define models
class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    pizzas = db.relationship('Pizza', secondary='restaurant_pizza', back_populates='restaurants')

class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    ingredients = db.Column(db.String(255), nullable=False)
    restaurants = db.relationship('Restaurant', secondary='restaurant_pizza', back_populates='pizzas')

class RestaurantPizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)

# Define schema for serialization (using Marshmallow)
class RestaurantSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Restaurant

class PizzaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pizza

def create_tables_and_run_app():
    # Create database tables
    db.create_all()

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Routes
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    with app.app_context():
        restaurants = Restaurant.query.all()
        restaurant_schema = RestaurantSchema(many=True)
        result = restaurant_schema.dump(restaurants)
        return jsonify(result)

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    with app.app_context():
        restaurant = Restaurant.query.get(id)
        if restaurant:
            restaurant_schema = RestaurantSchema()
            result = restaurant_schema.dump(restaurant)
            return jsonify(result)
        else:
            return jsonify({'error': 'Restaurant not found'}), 404

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    with app.app_context():
        restaurant = Restaurant.query.get(id)
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            return '', 204
        else:
            return jsonify({'error': 'Restaurant not found'}), 404

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    with app.app_context():
        pizzas = Pizza.query.all()
        pizza_schema = PizzaSchema(many=True)
        result = pizza_schema.dump(pizzas)
        return jsonify(result)

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    with app.app_context():
        data = request.get_json()
        price = data.get('price')
        pizza_id = data.get('pizza_id')
        restaurant_id = data.get('restaurant_id')

        if not (price and pizza_id and restaurant_id):
            return jsonify({'errors': ['Validation errors']}), 400

        pizza = Pizza.query.get(pizza_id)
        restaurant = Restaurant.query.get(restaurant_id)

        if not (pizza and restaurant):
            return jsonify({'errors': ['Validation errors']}), 400

        if not (1 <= price <= 30):
            return jsonify({'errors': ['Validation errors']}), 400

        restaurant_pizza = RestaurantPizza(price=price, pizza=pizza, restaurant=restaurant)
        db.session.add(restaurant_pizza)
        db.session.commit()

        pizza_schema = PizzaSchema()
        result = pizza_schema.dump(pizza)
        return jsonify(result), 201

if __name__ == '__main__':
    with app.app_context():
        create_tables_and_run_app()
    app.run(debug=True)