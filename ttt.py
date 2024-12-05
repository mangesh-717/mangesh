from flask import Flask, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, JWTManager,get_jwt_identity

app = Flask(__name__)

# Secret key for JWT
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
jwt = JWTManager(app)

# Sample data: passwords are hashed for security
users = [
    {'id': 1, 'username': 'john', 'email': 'john@example.com', 'password': generate_password_hash('password123')},
    {'id': 2, 'username': 'jane', 'email': 'jane@example.com', 'password': generate_password_hash('mypassword')}
]

# Registration route
@app.route('/register', methods=['POST'])
def register():
    new_user = request.get_json()
    if not all(key in new_user for key in ('username', 'email', 'password')):
        return jsonify({"message": "Missing fields"}), 400

    hashed_password = generate_password_hash(new_user['password'])
    user = {
        'id': len(users) + 1,
        'username': new_user['username'],
        'email': new_user['email'],
        'password': hashed_password
    }
    users.append(user)
    return jsonify({'message': 'User registered successfully'}), 201




# Login route (Token Authentication)
@app.route('/login', methods=['POST'])
def login():
    login_data = request.get_json()
    username = login_data.get('username')
    password = login_data.get('password')

    # Find user by username
    user = next((u for u in users if u['username'] == username), None)

    if user and check_password_hash(user['password'], password):
        # Create access token for the user
        access_token = create_access_token(identity=user['id'])
        return jsonify(access_token=access_token), 200
    return jsonify({"message": "Invalid credentials"}), 401




# Protected route to retrieve user data using token
@app.route('/user', methods=['GET'])
# @jwt_required()  # Requires a valid JWT token to access
def get_user():
    # Get the user ID stored in the token
    # user_id = get_jwt_identity()
    # # Find user by ID
    # user = next((u for u in users if u['id'] == user_id), None)
    # if user:
    #     # Return user details except the password
    #     user_data = {
    #         'id': user['id'],
    #         'username': user['username'],
    #         'email': user['email']
    #     }
    #     return jsonify(user_data), 200

    return jsonify(users)#{"message": "User not found"}), 404
  

if __name__ == '__main__':
    app.run(debug=True)
