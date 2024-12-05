from flask import Flask,jsonify,render_template,request
from flask_jwt_extended import create_access_token, jwt_required, JWTManager,get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash

app=Flask(__name__)
from models import Employee
obj=Employee()

# Secret key for JWT
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
jwt = JWTManager(app)

from datetime import timedelta
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=1000)  # Set token expiry to 100 seconds


data=obj.retrival_through_sp()

users = [{'id' : i[0], 'firstname': i[1], 'lastname': i[2],'Email':i[3],'Phon':i[4],'Address':i[5],'Password':i[6],'Username':i[-1] }for i in data]


# Login route (Token Authentication)
@app.route('/login', methods=['POST'])
def login():
    login_data = request.get_json()
    username = login_data.get('Username')
    password = login_data.get('Password')
    print(username,password)
    # Find user by username
    user = next((u for u in users if u['Username'] == username), None)

    if user and check_password_hash(user['Password'], password):
        print(user['Password'])
        print(user)
        # Create access token for the user
        access_token = create_access_token(identity=user['id'])
        print(access_token)
        return jsonify({"token":access_token}), 200
    return jsonify({"message": "Invalid credentials"}), 401


@app.route('/register',methods=['POST'])
def registrations():
    if request.method == 'POST': 
        new_user = request.get_json()   
        # Define required fields
        required_fields = ['firstname','lastname', 'Email','Phon' ,'Username', 'password', 'Address'] 
        # Validate if all required fields are present in the data
        missing_fields = [field for field in required_fields if field not in new_user]
        if missing_fields:
            
            # If any required fields are missing, return an error message
            return jsonify({
                'error': 'Missing fields',
                'message': f'The following fields are required: {", ".join(missing_fields)}'
            }), 400
        
        # checking wether the email is already exist or not 
        d=[i['Email'] if i['Email']==new_user['Email'] else None  for i in users ]        
        if d[0]:
            return jsonify({
                'error': 'Email already exist',
                'message': f'go to login as your email is already exist or registered'
            }), 400
        
        else:
            # storing user in database by stored procedure
            obj.insertion_through_sp(new_user['firstname'],new_user['lastname'],new_user['Email'],new_user['Phon'],new_user["Address"],generate_password_hash(new_user['password']),new_user['Username'])
            print("success")
        # If all required fields are present, display created user
        return jsonify({
            'message': 'User created successfully',
            'user': new_user 
        }), 201


# Protected route to retrieve user data using token
@app.route('/user', methods=['GET'])
@jwt_required()  # Requires a valid JWT token to access
def get_user():
    # # Get the user ID stored in the token
    user_id = get_jwt_identity()
    # Find user by ID
    user = next((u for u in users if u['id'] == user_id), None)
    print(user)
    if user:
        # Return user details except the password
        user_data = {
            'id': user['id'],
            'username': user['Username'],
            'email': user['Email'],
            'firstname':user['firstname'],
             'lastname':user['lastname'],
             'Phon':user['Phon']
             ,'Address':user['Address']
        }
        return jsonify(user_data), 200
    return jsonify({"message": "User not found"}), 404
     

if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode for easy development and troubleshooting

