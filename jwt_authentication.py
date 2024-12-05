import jwt
import datetime

# Secret key to encode/decode tokens
SECRET_KEY = 'your_secret_key'

# Function to generate a JWT token
def create_jwt(user_id):
    # Define the expiration time (e.g., 1 hour from now)
    expiration = datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
    
    # Create payload with claims
    payload = {
        'user_id': user_id,
        'exp': expiration
    }
    # Generate the JWT token
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    
    print(token)

# @jwtrequire
def decode_jwt(token):
    try:
        # Decode the token using the same secret key
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return 'Token has expired'
    except jwt.InvalidTokenError:
        return 'Invalid token'
p=decode_jwt("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyNjU3Mjk2MCwianRpIjoiNDExOTY1ZjktYmNiMi00OTk3LTg0YTQtNDUwMDBhYzk2ZGY4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MTA0LCJuYmYiOjE3MjY1NzI5NjAsImNzcmYiOiJjOGE1OWI3Zi02NzBiLTQ1YjgtOTExNS05NzNmODE4ZWIwYmQiLCJleHAiOjE3MjY1NzM5NjB9.j1P5wlbMWKLhND2zwAG_zS4i-Q7eFYX0Ep9fOCJjAOM")
print(p['firstname'])



















# from flask import Flask, jsonify, request
# import jwt
# import datetime

# app = Flask(__name__)

# # Secret key for encoding and decoding JWTs
# SECRET_KEY = 'your_secret_key'

# # In-memory user data for demonstration purposes
# users = {
#     'john@example.com': {'password': 'password123', 'id': 1},
#     'jane@example.com': {'password': 'mypassword', 'id': 2}
# }

# # Route to authenticate user and generate JWT
# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')
    
#     user = users.get(email)
    
#     if user and user['password'] == password:
#         # Create JWT token if authentication is successful
#         token = create_jwt(user['id'])
#         return jsonify({'token': token})
#     return jsonify({'message': 'Invalid credentials'}), 401

# # Protected route that requires a valid JWT
# @app.route('/protected', methods=['GET'])
# def protected():
#     token = request.headers.get('Authorization')
    
#     if token:
#         try:
#             # Remove 'Bearer ' prefix if present
#             token = token.split(' ')[1] if 'Bearer ' in token else token
#             decoded_token = decode_jwt(token)
#             return jsonify({'message': 'Access granted', 'user_id': decoded_token['user_id']})
#         except Exception as e:
#             return jsonify({'message': str(e)}), 401
#     return jsonify({'message': 'Token is missing'}), 403

# # Function to create a JWT token
# def create_jwt(user_id):
#     expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
#     payload = {
#         'user_id': user_id,
#         'exp': expiration
#     }
#     token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
#     return token

# # Function to decode and verify a JWT token
# def decode_jwt(token):
#     return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

# if __name__ == '__main__':
#     app.run(debug=True)
