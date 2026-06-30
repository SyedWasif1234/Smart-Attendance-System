from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv

from utils.db import connect_db, disconnect_db
from utils.dependencies import require_teacher, require_student, get_current_user

from routers.auth_router import auth_router
from routers.student_router import student_router
from routers.subject_router import subject_router
from routers.class_router import class_router


load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs when the server starts
    await connect_db()
    print("Database connected successfully.")
    yield
    # This runs when the server shuts down
    await disconnect_db()
    print("Database disconnected.")


app = FastAPI(lifespan=lifespan, title="Smart AI Attendance API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, change to ["http://localhost:3000", "https://yourdomain.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(student_router)
app.include_router(subject_router)
app.include_router(class_router)

# --- ROOT ENDPOINT ---
@app.get("/")
async def root():
    return {"message": "Smart Attendance API is Running!"}



"""
--- EXAMPLES OF HOW TO USE YOUR NEW RBAC ---

@app.get("/teacher-dashboard", dependencies=[Depends(require_teacher)])
async def teacher_only_route():
 return {"message": "Welcome Teacher! You have exclusive access to this data."}

"""


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)