from fastapi import APIRouter, Depends, HTTPException, status

from api.db import get_db_connection
from api.auth import get_current_user, get_password_hash
from api.schemas import UserCreate, UserOut
import psycopg2.extras

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

# Routes
@router.post("/signup", response_model=UserOut)
def signup(user: UserCreate, db=Depends(get_db_connection)):
    """
    Register a new user.
    - **username**: Must be a non-empty string.
    - **password**: Must be a non-empty string.
    """
    cur = None
    try:
        hashed_password = get_password_hash(user.password)
        cur = db.cursor()
        cur.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id, username",
            (user.username.strip(), hashed_password)
        )
        new_user = cur.fetchone()
        db.commit()
        return new_user
    except psycopg2.errors.UniqueViolation:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    except ValueError as e:
         raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    finally:
        if cur:
            cur.close()
        db.close()

@router.get("/me", response_model=UserOut)
def read_users_me(current_user: UserOut = Depends(get_current_user)):
    """
    Returns the details of the currently authenticated user.
    """
    return current_user
