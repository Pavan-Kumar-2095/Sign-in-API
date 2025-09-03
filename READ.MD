# Signup API with Redis & Password Hashing

## Overview

This project implements a simple signup API using FastAPI that supports two signup flows:

- **Phone Number Signup** — allows users to sign up using their phone number  
- **Email Signup** — allows users to sign up using their email address  

It uses Redis for temporary data storage (e.g., OTPs) and Passlib with bcrypt for secure password hashing.

To interact with and test these flows, run the provided test script.

---

## Prerequisites

- Python 3.8 or higher  
- Redis server installed and running locally on port 6379  
- `pip` for installing Python packages  

---

## Install Python Dependencies

```bash
pip install fastapi uvicorn redis passlib[bcrypt] bcrypt anyio

