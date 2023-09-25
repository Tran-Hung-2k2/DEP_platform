import requests
import random
import string

# Define the URL of your Django server where you want to send the requests
server_url = "http://localhost:8000/user_service/register/create"

# Gửi 1 batch lớn

services = ['TrackAndTrace', 'SmartHome', 'SmartFarm', 'PowerSaving', 'CMP']
register_number=20
def generate_random_register_data(user_id):
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
    service = random.choice(services)  # Randomly select a service from the list
    register_data = {
        "token": token,
        "user_id": user_id,
        "service": service,
    }
    return register_data

register_data_list = [generate_random_register_data(user_id) for user_id in range(register_number)]

response = requests.post(server_url, json=register_data_list)

if response.status_code == 201:
    print("Data added successfully for all users.")
else:
    print(f"Failed to add data - Status Code: {response.status_code}")



# Gửi lần lượt

# def generate_random_register_data(user_id):
#     token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
#     service = ''.join(random.choices(string.ascii_letters, k=10))
#     register_data = {
#         "token": token,
#         "user_id": user_id,
#         "service": service,
#     }
#     return register_data

# for user_id in range(register_number):
#     register_data = generate_random_register_data(user_id)
#     response = requests.post(server_url, json=register_data)
#     if response.status_code == 201:
#         print(f"Data added successfully for user_id: {user_id}")
#     else:
#         print(f"Failed to add data for user_id: {user_id} - Status Code: {response.status_code}")
