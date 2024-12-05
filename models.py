
import mysql.connector as mc

class Employee:
    def __init__(self):
        self.connect = mc.connect(user='root', password='root', host='127.0.0.1', port=3306, database='flask_companydb')
        self.cursor = self.connect.cursor()

    def retrival_through_sp(self):
        self.cursor.execute("select * from employees")
        return self.cursor.fetchall()
    def retrival_specific(self,search_value):
        sqll = f"CALL flask_companydb.Employee_sp_check_value('{search_value}');"
        self.cursor.execute(sqll)

    # Fetch result
        result = self.cursor.fetchone()

    # If a result is returned, the value exists
        if result:
            return True
        
    def insertion_through_sp(self,firstname,lastname,email, phonnumber,Address,password,username):
        sql = "CALL Employee_sp_insertion(%s, %s, %s, %s, %s, %s,%s);"
    
    # Execute the stored procedure with the parameters passed
        self.cursor.execute(sql, (firstname, lastname, email , phonnumber, Address, password,username))
obj=Employee()
# if obj.retrival_specific('mangesh.sathe1353@gmail.com'):
    # print('rapidsexcer')
# if
# obj.cursor.execute('select ppassword from employees where email="mangeshsathe1353@gmail.com";')
# print(obj.cursor.fetchall()[-1][-1])
# obj.insertion_through_sp( "Navi Mumbai","mangesh.sathe1353@gmail.com","Sathe@717",7218920354,"mangesh@123","Mangesh","Sathe")
# print('success')