#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries=[]
    for bakery in Bakery.query.all():
        bakery_dict={
            "id":bakery.id,
            "name":bakery.name,
            "created_at":bakery.created_at
        }
        bakeries.append(bakery_dict)
    response=make_response(
            jsonify(bakeries),
            200
        )
    response.headers['content-Type']='application/json'
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery=Bakery.query.filter_by(id=id).first()
    bakery_data={
        "id":bakery.id,
        "name":bakery.name,
        "created_at":bakery.created_at
    }
    response=make_response(
        jsonify(bakery_data),
        200
        )
    response.headers['content-Type']='application/json'
    return response
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods=BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_data=[{
        "id":baked_good.id,
        "name":baked_good.name,
        "price":baked_good.price,
        "created_at":baked_good.created_at
    }
    for baked_good in baked_goods

    ]
    response=make_response(
        jsonify(baked_goods_data),
        200
        )
    response.headers['content-Type']='application/json'
    return response


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_goods=BakedGood.query.order_by(BakedGood.price.desc()).limit(1).all()
    for baked_good in baked_goods:
       baked_goods_data={
        "id":baked_good.id,
        "name":baked_good.name,
        "price":baked_good.price,
        "created_at":baked_good.created_at
     }

    response=make_response(
        jsonify(baked_goods_data),
        200
        )
    response.headers['content-Type']='application/json'
    return response

# @app.route('/add_data')
# def add_data():
# # Creating and adding a bakery
#     bakery = Bakery(name='Example Bakery')
#     db.session.add(bakery)
#     db.session.commit()

#     # Creating and adding a baked good associated with the bakery
#     baked_good = BakedGood(name='Example Good', price=10.99, bakery_id=bakery.id)
#     db.session.add(baked_good)
#     db.session.commit()

#     return 'Data added successfully'

# ...

# @app.route('/seed')
# def seed():
#     seed_data()
#     return 'Data has been seeded to the database.'

if __name__ == '__main__':
     app.run(port=5555, debug=True)