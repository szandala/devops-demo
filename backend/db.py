from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId
import os

mongodb_host = os.environ.get("MONGODB_HOST", "localhost")
mongodb_username = os.environ.get("MONGODB_USERNAME", "root")
mongodb_password = os.environ.get("MONGODB_PASSWORD", "example")
connection_string = f"mongodb://{mongodb_username}:{mongodb_password}@{mongodb_host}"
client = MongoClient(connection_string)
print(f"Connecting to DB on URL: {connection_string}")
db = client["devops_db"]
users = db.users

def get_users():
    users_cursor = users.find({})
    users_list = []
    for user in users_cursor:
        user['_id'] = str(user['_id'])
        del user['password']
        users_list.append(user)
    return users_list


def create_user(user_data):
    if users.count_documents({"$or": [{"email": user_data["email"]}]}):
        return "User with this email already exists."

    return str(users.insert_one(user_data).inserted_id)

def read_user(email=None, user_id=None):
    if email:
        user = users.find_one({"email": email})
    else:
        user = users.find_one({"_id": ObjectId(user_id)})

    if user:
        user['_id'] = str(user['_id'])
    return user

def update_user(user_id, new_user_data):
    user = users.find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$set": new_user_data},
        return_document=ReturnDocument.AFTER
    )
    if user:
        user['_id'] = str(user['_id'])
    return user

def delete_user(user_id):
    return users.delete_one({"_id": ObjectId(user_id)})

if __name__ == "__main__":

    user_data = {
        "email": "user@example.com",
        "name": "Name",
        "surname": "Surname",
        "password": "password",
        "roles": ["admin"]
    }

    user_id = create_user(user_data)
    print(f"User created with ID: {user_id}")

    user = read_user("user@example.com")
    print(f"User details by email: {user}")


    updated_user = update_user(user_id, {"email": "newemail@example.com"})
    print(f"Updated user details: {updated_user}")


    # delete_user(user_id)
    user = read_user(user_id=user_id)
    # print(f"User after deletion: {user}")