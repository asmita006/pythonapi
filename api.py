from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
users = [
    {"id": 1, "name": "John Doe", "email": "johndoe@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "janesmith@example.com"}
]

# GET request to fetch all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

# GET request to fetch a specific user
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    for user in users:
        if user['id'] == user_id:
            return jsonify(user)
    return jsonify({"error": "User not found"})

# POST request to create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = {
        "id": len(users) + 1,
        "name": data['name'],
        "email": data['email']
    }
    users.append(new_user)
    return jsonify(new_user)

# DELETE request to delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    for user in users:
        if user['id'] == user_id:
            users.remove(user)
            return jsonify({"message": "User deleted"})
    return jsonify({"error": "User not found"})

if __name__ == '__main__':
    app.run()

