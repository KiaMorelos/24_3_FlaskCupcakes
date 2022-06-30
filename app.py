"""Flask app for Cupcakes"""

from flask import Flask, render_template, request, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SECRET_KEY'] = "its_a_secret_to_everybody"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

def serialize_cupcake(cupcake):
    """Serialize a cupcake SQLAlchemy obj to dictionary."""
   
    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image,
    }

@app.route('/')
def root_route():
    """Home Page View Route"""

    return render_template('index.html')

@app.route('/api/cupcakes')
def list_all_cupcakes():
    """Return JSON list of all cupcakes in database"""
    
    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(cupcake) for cupcake in cupcakes]

    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes/q=<search>')
def search_cupcakes(search):
    """Search for cupcakes query, return JSON result"""
    cupcakes = Cupcake.query.filter(Cupcake.flavor.ilike(f'%{search}%')).all()
    if cupcakes:
        serialized = [serialize_cupcake(cupcake) for cupcake in cupcakes]
        return jsonify(cupcakes=serialized)
    else:
        return (jsonify({"message": "No Results"}))


@app.route('/api/cupcakes/<int:cupcake_id>')
def get_a_cupcake(cupcake_id):
    """Return JSON Data for Single Cupcake"""
    
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = serialize_cupcake(cupcake)
   
    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create a new cupcake in database, return JSON of new cupcake"""
    
    flavor = request.json['flavor']
    rating = request.json['rating']
    size = request.json['size']
    image = request.json['image']

    new_cupcake = Cupcake(flavor=flavor, rating=rating, size=size, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize_cupcake(new_cupcake)
    
    return (jsonify(cupcake= serialized), 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """Update Cupcake and return JSONIFY'd Data"""
    
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json['flavor']
    cupcake.rating = request.json['rating']
    cupcake.size = request.json['size']
    cupcake.image = request.json['image']

    db.session.add(cupcake)
    db.session.commit()

    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """Delete Cupcake, return JSON reponse if successful"""
    
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    
    db.session.delete(cupcake)
    db.session.commit()

    return (jsonify({"message": "Deleted"}), 200)
