from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from passlib.hash import bcrypt
from datetime import datetime
import random
import redis
import json


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PORT = 8000


r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['user_db']
users_collection = db['users']


OTP_EXPIRY = 300  # 5 minutes

def generate_otp():
    return str(random.randint(100000, 999999))

def store_in_redis(key, data, expiry=OTP_EXPIRY):
    r.setex(key, expiry, json.dumps(data))


class SignUpRequest(BaseModel):
    username: str
    password: str
    mobile: str = None
    email: str = None

class PhoneNumberOTPRequest(BaseModel):
    username: str
    otp: str

class EmailOTPRequest(BaseModel):
    username: str
    otp: str


@app.post("/Phone_Number_Sign_UP")
def phone_number_signup(data: SignUpRequest):
    print("Received phone number signup request")
    if not data.username or not data.password or not data.mobile:
        raise HTTPException(status_code=400, detail="Missing required fields")

    if users_collection.find_one({"mobile": data.mobile}):
        return JSONResponse(status_code=400, content={"error": "User with this mobile already exists"})

    otp = generate_otp()
    print("printing internally generated OTP : " , otp)

    hashed_password = bcrypt.hash(data.password)

    user_key = f"user:{data.username}"

    user_data = {
        "username": data.username,
        "password": hashed_password,
        "mobile": data.mobile,
        "mobile_otp": otp,
        "mobile_verified": False,
        "otp_generated_at": datetime.utcnow().isoformat()
    }

    print("storing data in redis")

    store_in_redis(user_key, user_data, expiry=1800)

    print("returning the OTP just to understand the flow ")
    return JSONResponse(status_code=200, content={
        "message": "Signup initiated, OTP sent to mobile",
        "mobile_otp": otp  
    })


@app.post("/Validate_Phone_Number_OTP")
def validate_phone_number_otp(data: PhoneNumberOTPRequest):
    user_key = f"user:{data.username}"
    user_data_json = r.get(user_key)

    if not user_data_json:
        raise HTTPException(status_code=404, detail="User data expired or not found")

    user_data = json.loads(user_data_json)

    if user_data.get("mobile_verified"):
        raise HTTPException(status_code=400, detail="Mobile already verified")

    print("internally generated OTP which is stored in redis : " , data.otp)
    print("User entered OTP : " , user_data.get("mobile_otp"))

    if user_data.get("mobile_otp") != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    user_data["mobile_verified"] = True
    user_data["mobile_otp"] = None

    mongo_data = {
        "username": user_data["username"],
        "password": user_data["password"],
        "mobile": user_data["mobile"],
        "email": user_data.get("email"),
        "created_at": datetime.utcnow().isoformat()
    }

    print("Uploading data to MongoDB")
    users_collection.insert_one(mongo_data)
    print("Deleting the data in Redis")
    r.delete(user_key)

    return {"message": "Mobile verified and registration finalized successfully"}


@app.post("/Email_Sign_UP")
def email_signup(data: SignUpRequest):
    print("Received Email signup request")
    if not data.username or not data.password or not data.email:
        raise HTTPException(status_code=400, detail="Missing required fields")

    if users_collection.find_one({"email": data.email}):
        return JSONResponse(status_code=400, content={"error": "User with this email already exists"})

    otp = generate_otp()
    print("printing internally generated OTP : " , otp)

    hashed_password = bcrypt.hash(data.password)
    
    user_key = f"user:{data.username}"

    user_data = {
        "username": data.username,
        "password": hashed_password,
        "email": data.email,
        "email_otp": otp,
        "email_verified": False,
        "otp_generated_at": datetime.utcnow().isoformat()
    }

    print("storing data in redis")

    store_in_redis(user_key, user_data, expiry=1800)

    print("returning the OTP just to understand the flow ")

    return JSONResponse(status_code=200, content={
        "message": "Signup initiated, OTP sent to email",
        "email_otp": otp  
    })


@app.post("/Validate_Email_OTP")
def validate_email_otp(data: EmailOTPRequest):
    user_key = f"user:{data.username}"
    user_data_json = r.get(user_key)

    if not user_data_json:
        raise HTTPException(status_code=404, detail="User data expired or not found")

    user_data = json.loads(user_data_json)

    if user_data.get("email_verified"):
        raise HTTPException(status_code=400, detail="Email already verified")
    
    print("internally generated OTP which is stored in redis : " , data.otp)
    print("User entered OTP : " , user_data.get("email_otp"))

    if user_data.get("email_otp") != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    user_data["email_verified"] = True
    user_data["email_otp"] = None

    mongo_data = {
        "username": user_data["username"],
        "password": user_data["password"],
        "email": user_data["email"],
        "mobile": user_data.get("mobile"),
        "created_at": datetime.utcnow().isoformat()
    }

    print("Uploading data to MongoDB")

    users_collection.insert_one(mongo_data)

    print("Deleting the data in Redis")
    
    r.delete(user_key)

    return {"message": "Email verified and registration finalized successfully"}


@app.get("/")
def root():
    return {"message": "OTP-based Sign-Up Server Running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
