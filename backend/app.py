from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from models import db, User, Driver
import jwt
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            token = token.split(" ")[1]  # Remove 'Bearer ' prefix
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    
    if user and user.check_password(data.get('password')):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({
            'token': token,
            'user': {'id': user.id, 'email': user.email}
        })
    return jsonify({'message': 'Invalid credentials!'}), 401

@app.route('/api/drivers', methods=['GET'])
@token_required
def get_drivers(current_user):
    drivers = Driver.query.all()
    return jsonify([{
        'id': d.id,
        'first_name': d.first_name,
        'last_name': d.last_name,
        'email': d.email,
        'phone': d.phone,
        'license_number': d.license_number,
        'license_expiry': d.license_expiry.isoformat(),
        'status': d.status
    } for d in drivers])

@app.route('/api/drivers/<int:id>', methods=['GET'])
@token_required
def get_driver(current_user, id):
    driver = Driver.query.get_or_404(id)
    return jsonify({
        'id': driver.id,
        'first_name': driver.first_name,
        'last_name': driver.last_name,
        'email': driver.email,
        'phone': driver.phone,
        'license_number': driver.license_number,
        'license_expiry': driver.license_expiry.isoformat(),
        'status': driver.status
    })

@app.route('/api/drivers', methods=['POST'])
@token_required
def create_driver(current_user):
    data = request.get_json()
    
    # Basic validation
    required_fields = ['first_name', 'last_name', 'email', 'phone', 
                      'license_number', 'license_expiry']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400
    
    # Create new driver
    new_driver = Driver(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data['phone'],
        license_number=data['license_number'],
        license_expiry=datetime.strptime(data['license_expiry'], '%Y-%m-%d').date(),
        status=data.get('status', 'active')
    )
    
    try:
        db.session.add(new_driver)
        db.session.commit()
        return jsonify({
            'message': 'Driver created successfully',
            'id': new_driver.id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400

@app.route('/api/drivers/<int:id>', methods=['PUT'])
@token_required
def update_driver(current_user, id):
    driver = Driver.query.get_or_404(id)
    data = request.get_json()
    
    # Update fields
    if 'first_name' in data:
        driver.first_name = data['first_name']
    if 'last_name' in data:
        driver.last_name = data['last_name']
    if 'email' in data:
        driver.email = data['email']
    if 'phone' in data:
        driver.phone = data['phone']
    if 'license_number' in data:
        driver.license_number = data['license_number']
    if 'license_expiry' in data:
        driver.license_expiry = datetime.strptime(data['license_expiry'], '%Y-%m-%d').date()
    if 'status' in data:
        driver.status = data['status']
    
    try:
        db.session.commit()
        return jsonify({'message': 'Driver updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400

@app.route('/api/drivers/<int:id>', methods=['DELETE'])
@token_required
def delete_driver(current_user, id):
    driver = Driver.query.get_or_404(id)
    try:
        db.session.delete(driver)
        db.session.commit()
        return jsonify({'message': 'Driver deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Fleetwise API running'}), 200

def init_db():
    with app.app_context():
        db.create_all()
        # Create admin user if not exists
        admin = User.query.filter_by(email='admin@fleetwise.com').first()
        if not admin:
            admin = User(email='admin@fleetwise.com')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=8000)