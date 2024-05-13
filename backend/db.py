from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId
import os

mongodb_host = os.environ.get("MONGODB_HOST", "localhost")
# Environment variables for MongoDB hosts if specified
mongodb_rw_host = os.environ.get("MONGODB_RW_HOST", mongodb_host)  # Read-Write host
mongodb_ro_host = os.environ.get("MONGODB_RO_HOST", mongodb_host)  # Read-Only host

mongodb_username = os.environ.get("MONGODB_USERNAME", "root")
mongodb_userpass = os.environ.get("MONGODB_PASSWORD", "example")

# Connection strings for both Read-Write and Read-Only databases
connection_string_rw = f"mongodb://{mongodb_username}:{mongodb_userpass}@{mongodb_rw_host}"
connection_string_ro = f"mongodb://{mongodb_username}:{mongodb_userpass}@{mongodb_ro_host}"

# Clients for Read-Write and Read-Only
client_rw = MongoClient(connection_string_rw)
client_ro = MongoClient(connection_string_ro)

print(f"Connecting to Read-Write DB on URL: {connection_string_rw}")
print(f"Connecting to Read-Only DB on URL: {connection_string_ro}")

db_rw = client_rw["devops_db"]  # Read-Write database instance
db_ro = client_ro["devops_db"]  # Read-Only database instance

users_rw = db_rw.users  # Collection for write operations
users_ro = db_ro.users  # Collection for read operations

def get_users():
    users_cursor = users_ro.find({})  # Use Read-Only client for reading data
    users_list = []
    for user in users_cursor:
        user['_id'] = str(user['_id'])
        del user['password']
        users_list.append(user)
    return users_list

def create_user(user_data):
    if users_ro.count_documents({"$or": [{"email": user_data["email"]}]}):  # Use Read-Only client for checking existence
        return "User with this email already exists."
    return str(users_rw.insert_one(user_data).inserted_id)  # Use Read-Write client for writing data

def read_user(email=None, user_id=None):
    if email:
        user = users_ro.find_one({"email": email})
    else:
        user = users_ro.find_one({"_id": ObjectId(user_id)})
    if user:
        user['_id'] = str(user['_id'])
    return user

def update_user(user_id, new_user_data):
    user = users_rw.find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$set": new_user_data},
        return_document=ReturnDocument.AFTER
    )
    if user:
        user['_id'] = str(user['_id'])
    return user

def delete_user(user_id):
    return users_rw.delete_one({"_id": ObjectId(user_id)})

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
