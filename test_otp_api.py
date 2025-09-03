import requests

BASE_URL = "http://localhost:8000/"

def phone_number_signup():
    print("\n=== Phone Number Signup ===")
    username = input("Enter username: ")
    password = input("Enter password: ")
    mobile = input("Enter mobile number: ")

    payload = {
        "username": username,
        "password": password,
        "mobile": mobile
    }

    response = requests.post(f"{BASE_URL}/Phone_Number_Sign_UP", json=payload)
    print("Status Code:", response.status_code)
    print("Raw Response:", response.text)

    try:
        data = response.json()
        if response.status_code == 200:
            otp = data.get("mobile_otp")
            print(f"OTP (for testing): {otp}")
            return username, otp
        else:
            print("Error:", data.get("error") or data.get("detail"))
    except Exception as e:
        print("Failed to parse JSON:", e)

    return None, None

def validate_phone_number_otp(username):
    print("\n=== Validate Phone Number OTP ===")
    otp = input("Enter OTP received: ")

    payload = {
        "username": username,
        "otp": otp
    }

    response = requests.post(f"{BASE_URL}/Validate_Phone_Number_OTP", json=payload)
    print("Status Code:", response.status_code)
    print("Response:", response.text)

def email_signup():
    print("\n=== Email Signup ===")
    username = input("Enter username: ")
    password = input("Enter password: ")
    email = input("Enter email: ")

    payload = {
        "username": username,
        "password": password,
        "email": email
    }

    response = requests.post(f"{BASE_URL}/Email_Sign_UP", json=payload)
    print("Status Code:", response.status_code)
    print("Raw Response:", response.text)

    try:
        data = response.json()
        if response.status_code == 200:
            otp = data.get("email_otp")
            print(f"OTP (for testing): {otp}")
            return username, otp
        else:
            print("Error:", data.get("error") or data.get("detail"))
    except Exception as e:
        print("Failed to parse JSON:", e)

    return None, None

def validate_email_otp(username):
    print("\n=== Validate Email OTP ===")
    otp = input("Enter OTP received: ")

    payload = {
        "username": username,
        "otp": otp
    }

    response = requests.post(f"{BASE_URL}/Validate_Email_OTP", json=payload)
    print("Status Code:", response.status_code)
    print("Response:", response.text)

def main():
    print("Select flow to test:")
    print("1. Phone Number Signup")
    print("2. Email Signup")
    choice = input("Enter choice (1 or 2): ")

    if choice == "1":
        username, _ = phone_number_signup()
        if username:
            validate_phone_number_otp(username)

    elif choice == "2":
        username, _ = email_signup()
        if username:
            validate_email_otp(username)

    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
