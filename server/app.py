# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response,jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

@app.route('/earthquakes/<int:id>')
def get_eartquake_by_id(id):
        earthquake = Earthquake.query.get(id)
        if earthquake:
            return make_response(jsonify(earthquake.to_dict(),201))
        else:
            return make_response(jsonify({"message": "Earthquake 9999 not found."}),404)
        
@app.route('/earthquakes/magnitude/<float:magnitude>') 
def get_all(mag):
     earthquakes = Earthquake.query.filter(Earthquake.magnitude >= mag).all()   
     if earthquakes:
          quakes_list = [quake.to_dict() for quake in earthquakes]
          return jsonify({
               "count": len(quakes_list),
                "quakes": quakes_list
          }),200
     else:
        return jsonify({
            "count": 0,
            "quakes": []
        }), 200

       


if __name__ == '__main__':
    app.run(port=5555, debug=True)
