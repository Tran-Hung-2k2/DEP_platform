import requests
import random
import string


server_url = "http://localhost:8000/user_service/user/create"
user_number=20
# Function to generate random data for the user
def generate_random_user_data(user_id):
    username = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=12))
    gender = random.choice(['M', 'F'])
    date_of_birth = f"19{random.randint(60, 99)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
    phone_number = ''.join(random.choices(string.digits, k=10))
    balance = round(random.uniform(0, 1000), 2)
    email = f"{username}@example.com"  # Generate a random email based on the username
    user_data = {
        "user_id": user_id,
        "username": username,
        "password": password,
        "email": email,
        "gender": gender,
        "date_of_birth": date_of_birth,
        "phone_number": phone_number,
        "balance": balance,
    }
    return user_data

for i in range(user_number):
    user_data = generate_random_user_data(i)
    response = requests.post(server_url, json=user_data)
    if response.status_code == 201:
        print(f"User added successfully: {user_data['user_id']}")
    else:
        print(f"Failed to add user: {user_data['user_id']} - Status Code: {response.status_code}")
