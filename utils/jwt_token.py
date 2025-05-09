<<<<<<< HEAD
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Union
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()
# Secret key to encode and decode the JWT token (make sure to keep it secure!)
SECRET_KEY = f'{os.getenv("JWT_SECRET_KEY")}'
ALGORITHM = f"{os.getenv("JWT_ALGORITHM")}"  # Algorithm for encoding/decoding

# Token expiration time (for example, 1 hour)
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Function to create a token
def create_access_token(data: dict):
    # Setting the expiration time
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Creating the JWT token
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# Function to verify a token and extract user information
def verify_access_token(token: str) -> Union[dict, None]:
    try:
        # Decoding the token using the secret key
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # This will return the user data encoded in the token
        
    except JWTError:
        return None
=======
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Union
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()
# Secret key to encode and decode the JWT token (make sure to keep it secure!)
SECRET_KEY = f'{os.getenv("JWT_SECRET_KEY")}'
ALGORITHM = f"{os.getenv("JWT_ALGORITHM")}"  # Algorithm for encoding/decoding

# Token expiration time (for example, 1 hour)
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Function to create a token
def create_access_token(data: dict):
    # Setting the expiration time
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Creating the JWT token
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# Function to verify a token and extract user information
def verify_access_token(token: str) -> Union[dict, None]:
    try:
        # Decoding the token using the secret key
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # This will return the user data encoded in the token
        
    except JWTError:
        return None
>>>>>>> origin/main
