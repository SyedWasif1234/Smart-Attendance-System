from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from utils.security import verify_token
from utils.db import db 

# This tells FastAPI where the login route is so Swagger UI can use it
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    
    payload = verify_token(token)
    
    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials or token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    # Fetch user from DB using ID (token stores user ID in 'sub')
    user = await db.user.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

async def require_student(current_user = Depends(get_current_user)):
   
    if current_user.role != "STUDENT":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized. Student access required."
        )
    return current_user

async def require_teacher(current_user = Depends(get_current_user)):

    print(f"Current User: {current_user.username}")
    
    if current_user.role != "TEACHER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized. Teacher access required."
        )
    return current_user