from flask import Flask,request,render_template,redirect,flash,url_for
import mysql.connector as mc
import bcrypt
from models import Employee
app = Flask(__name__)


@app.route('/',methods=['GET','POST'])
def index():
    return render_template('home.html',message='Welcome to my flask Project')



error=None
@app.route('/registration', methods=['GET', 'POST'])
# login function verify username and password
def registeration():
    error=None
    # data = request.get_json()
    if request.method=="GET":
        return render_template("registration.html")

    elif request.method == 'POST':
        firstname=request.form['name']
        lastname=request.form['lastname'] 
        email=request.form['email']
        username=request.form['username']
        Phone=request.form['phone'] 
        Address=request.form['Address']
        Password=request.form['password']
         
        salt=bcrypt.gensalt()
        encrypted_pass=bcrypt.hashpw(Password.encode('utf-8'),salt)
        print(firstname,lastname,email,username, Phone,Address,encrypted_pass)
        # print(str(encrypted_pass)[1:])
        obj = Employee()
        obj.insertion_through_sp(firstname,lastname,email,Phone,Address,encrypted_pass,username)
        print("succed stored")
        return redirect(url_for('index'))
    else:
        print("Invalid request")

    


@app.route('/login', methods=['GET', 'POST'])
def login_function():
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form['password'] 
        
        # Connect to the database
        connect = mc.connect(user='root', password='root', host='127.0.0.1', port=3306, database='flask_companydb')
        cursor = connect.cursor()

        # Fetch the hashed password from the database
        cursor.execute(f"SELECT ppassword FROM employees WHERE username=%s", (username,))
        result = cursor.fetchone()
        
        if result:
            hashed_password = result[0]  # Extract the hashed password
            
            # Verify the entered password with the stored hashed password
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                return 'Successfully logged in'
            else:
                return 'Incorrect password'
        else:
            return "User not found"
    
    return render_template('login.html')

if __name__=='__main__':
    app.run(debug=True)
    


#     @app.route('/register', methods=['POST'])
# def register():
#     username = data.get('username')
#     password = data.get('password')

#     if not username or not password:
#         return jsonify({'message': 'Username and password are required'}), 400

#     hashed_password = generate_password_hash(password, method='sha256')
    
#     new_user = User(username=username, password=hashed_password)
#     db.session.add(new_user)
#     db.session.commit()

#     return jsonify({'message': 'User registered successfully'}), 201

# obj = Employee()

# obj.insertion_through_sp()
# obj.retrival_through_sp()       
        # return redirect(url_for('index.html'))
# if __name__=='__main__':
#     app.run(debug=True)

