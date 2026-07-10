# Signup API with Redis & Password Hashing

A simple FastAPI project that implements OTP-based user signup using either a **phone number** or an **email address**. The project uses **Redis** for temporary OTP storage, **MongoDB** for storing verified users, and **bcrypt** for secure password hashing.

---

## Features

- Phone number signup with OTP verification
- Email signup with OTP verification
- Secure password hashing using bcrypt
- Temporary OTP storage in Redis
- User data stored in MongoDB after successful verification
- FastAPI REST APIs

---

## Tech Stack

- FastAPI
- MongoDB
- Redis
- Passlib (bcrypt)
- Python

---

## Project Structure

```text
project/
├── main.py          # FastAPI application
├── test.py          # Test client
├── requirements.txt
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Redis

```bash
redis-server
```

### 4. Start MongoDB

Make sure MongoDB is running locally.

### 5. Run the application

```bash
python main.py
```

or

```bash
uvicorn main:app --reload
```

The server will start at:

```
http://localhost:8000
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/Phone_Number_Sign_UP` | Register using phone number |
| POST | `/Validate_Phone_Number_OTP` | Verify phone OTP |
| POST | `/Email_Sign_UP` | Register using email |
| POST | `/Validate_Email_OTP` | Verify email OTP |

---

## Testing

Run the test script:

```bash
python test.py
```

Choose either:

- Phone Number Signup
- Email Signup

Follow the prompts to complete the OTP verification process.

---

## Workflow

```
Signup Request
      ↓
Generate OTP
      ↓
Store User Data in Redis
      ↓
Verify OTP
      ↓
Store User in MongoDB
      ↓
Registration Complete
```