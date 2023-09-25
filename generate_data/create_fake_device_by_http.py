import requests
import random
import string


server_url = "http://localhost:8000/user_service/device/create"

user_number=20
# Gửi 1 batch lớn

def generate_random_device_data(user_id):
    num_devices = random.randint(1, 3)  
    devices = []

    for _ in range(num_devices):
        device_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
        device_name = ''.join(random.choices(string.ascii_letters, k=10))
        plate_no = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        device_data = {
            "device_id": device_id,
            "user_id": user_id,
            "device_name": device_name,
            "plate_no": plate_no,
        }
        devices.append(device_data)
    
    return devices

all_devices_data = []

for user_id in range(user_number):
    device_data = generate_random_device_data(user_id)
    all_devices_data.extend(device_data)

response = requests.post(server_url, json=all_devices_data)

if response.status_code == 201:
    print("Data added successfully for all devices")
else:
    print(f"Failed to add data for all devices - Status Code: {response.status_code}")


# Gửi lần lượt từng cái


# def generate_random_device_data(user_id):
#     device_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
#     device_name = ''.join(random.choices(string.ascii_letters, k=10))
#     plate_no = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
#     device_data = {
#         "device_id": device_id,
#         "user_id": user_id,
#         "device_name": device_name,
#         "plate_no": plate_no,
#     }
#     return device_data

# for user_id in range(user_number):
#     device_data = generate_random_device_data(user_id)
#     response = requests.post(server_url, json=device_data)
#     if response.status_code == 201:
#         print(f"Data added successfully for user_id: {user_id}")
#     else:
#         print(f"Failed to add data for user_id: {user_id} - Status Code: {response.status_code}")
