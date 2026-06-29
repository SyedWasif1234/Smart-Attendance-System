from fastapi import FastAPI
import uvicorn


app = FastAPI(title="Smart Attendance API")


@app.get("/")
async def root():
    return {"status": "ok", "message": "API is running"}

# Run the server using uvicorn (only executed if run directly)
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)