# IMPORTS
import requests
from flask import Flask, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

# APP CONFIG
import UserClient
from producer import publish

app = Flask(__name__)
db = SQLAlchemy(app)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@order_db/order'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#  DB MODELS
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    items = db.relationship('OrderItem', backref='orderItem')
    is_open = db.Column(db.Boolean, default=True)

    def create(self, user_id):
        self.user_id = user_id
        self.is_open = True
        return self

    def to_json(self):
        items = []
        for i in self.items:
            items.append(i.to_json())

        return {
            'items': items,
            'is_open': self.is_open,
            'user_id': self.user_id
        }


class ProductsUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    # will make sure that the usr and produ ids are uniqes and should not duplicate
    # UniqueConstraint('user_id', 'product_id', name='user_product_unique')


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer, default=1)

    def __init__(self, product_id, quantity):
        self.product_id = product_id
        self.quantity = quantity

    def to_json(self):
        return {
            'product': self.product_id,
            'quantity': self.quantity,
        }


# Routes
@app.route('/api/health', methods=['GET'])
def health():
    response = "Healthy"
    return response


@app.route('/api/orders', methods=['GET'])
def orders():
    items = []
    for row in Order.query.all():
        items.append(row.to_json())

    response = jsonify(items)

    return response


@app.route('/api/order/add-item', methods=['POST'])
def order_add_item():
    req = requests.get('http://localhost:8000/django/api/user')
    json = req.json()

    try:

        productUser = ProductsUser(user_id=json['id'], product_id=id)
        db.session.add(productUser)
        db.session.commit()
        publish('Item_added_to _order', id)
    except:
        abort(400, 'already added')

    return jsonify({
        'message': 'success'
    })

    # Find open order
    known_order = Order.query.filter_by(user_id=u_id, is_open=1).first()

    if known_order is None:
        # Create the order
        known_order = Order()
        known_order.is_open = True
        known_order.user_id = u_id

        order_item = OrderItem(p_id, qty)
        known_order.items.append(order_item)

    else:
        found = False
        # Check if we already have an order item with that product
        for item in known_order.items:

            if item.product_id == p_id:
                found = True
                item.quantity += qty

        if found is False:
            order_item = OrderItem(p_id, qty)
            known_order.items.append(order_item)

    db.session.add(known_order)
    db.session.commit()

    response = jsonify({'result': known_order.to_json()})

    return response


#
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
