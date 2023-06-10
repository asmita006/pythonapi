from flask import Flask, jsonify, request, render_template
import mysql.connector

app = Flask(__name__)

# MySQL configurations
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mydatabase"  # Add the name of your database here
)

# Route to serve the index.html file
@app.route('/')
def index():
    return render_template('index.html')

# GET request to fetch all users
@app.route('/users', methods=['GET'])
def get_users():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    return jsonify(users)

# GET request to fetch a specific user
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"})

# POST request to create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data['name']
    email = data['email']
    cursor = mydb.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    mydb.commit()
    new_user_id = cursor.lastrowid
    cursor.close()
    new_user = {"id": new_user_id, "name": name, "email": email}
    return jsonify(new_user)

# DELETE request to delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    mydb.commit()
    deleted_rows = cursor.rowcount
    cursor.close()
    if deleted_rows > 0:
        return jsonify({"message": "User deleted"})
    return jsonify({"error": "User not found"})

if __name__ == '__main__':
    app.run(debug=True)



