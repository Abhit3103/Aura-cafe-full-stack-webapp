import logging
import hashlib
import base64
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

import crud
import schemas
from database import SessionLocal

# Configure logger for auth module
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(tags=["Authentication"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _prehash_password(password: str) -> str:
    """
    bcrypt silently truncates passwords longer than 72 bytes.
    To support arbitrary-length passwords securely, we pre-hash with SHA256
    and base64-encode the digest before passing it to bcrypt.
    This preserves full password entropy without truncation.
    """
    digest = hashlib.sha256(password.encode("utf-8")).digest()
    return base64.b64encode(digest).decode("ascii")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(_prehash_password(password))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(_prehash_password(plain_password), hashed_password)


@router.post("/signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = crud.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        hashed_password = get_password_hash(user.password)
        new_user = crud.create_user(db=db, user=user, hashed_password=hashed_password)
        logger.info("User signed up successfully: email=%s", user.email)
        return new_user

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Signup failed for email=%s: %s", user.email, exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Signup failed due to an internal error. Please try again later."
        )


@router.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    try:
        user = crud.get_user_by_email(db, email=user_credentials.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid credentials"
            )

        if not verify_password(user_credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid credentials"
            )

        logger.info("User logged in successfully: email=%s", user_credentials.email)

        # Using a simple mock token for now that frontend can use
        # A real app would generate a JWT token here using python-jose
        return {
            "message": "Login successful",
            "token": f"mock_token_{user.id}",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "phone": user.phone
            }
        }

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Login failed for email=%s: %s", user_credentials.email, exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed due to an internal error. Please try again later."
        )

