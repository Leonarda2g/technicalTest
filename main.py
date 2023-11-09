from fastapi import FastAPI
from database import connect
import httpx
from database import create_database, initialize_db
from fastapi import HTTPException
from database import create_user

app = FastAPI()

# Startup event to create database and initialize
@app.on_event("startup")
async def startup_event():
    create_database()
    initialize_db()

# Root
@app.get("/")
async def root():
    return {"message": "Backend Technical Test"}

# Get all users from the database (Public API: JSONPLACEHOLDER)
@app.get("/api/data")
async def get_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://jsonplaceholder.typicode.com/users")
        data = response.json()
    return data

# Store the name, email and phone from the External API to the database
@app.post("/api/data")
async def store_user():
    data = await get_data()
    inserted_count = 0  # Counter for new data inserted into the database
    for user in data:
        name = user["name"]
        email = user["email"]
        phone = user["phone"]
        # Verify entries in the database
        if not user_exists(email):
            create_user(name, email, phone)
            inserted_count += 1

    if inserted_count > 0:
        return {"message": f"{inserted_count} new data record(s) inserted into the database."}
    else:
        return {"message": "No new data inserted into the database."}

# Check if user exists in the database
def user_exists(email):
    conn = connect()
    cursor = conn.cursor()
    query = """SELECT * FROM users WHERE email = %s"""
    cursor.execute(query, (email,))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# Get a single user from the database given their id
@app.get("/api/data/{id}")
def get_user(id: int):
    conn = connect()
    cursor = conn.cursor()
    query = """SELECT * FROM users WHERE id = %s"""
    cursor.execute(query, (id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return {
            "id": user[0],
            "name": user[1],
            "email": user[2],
            "phone": user[3]
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")
