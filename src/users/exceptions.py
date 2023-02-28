from fastapi import HTTPException, status


def user_not_found():
    return HTTPException(404, "User Not Found")


def login_fail():
    return HTTPException(status.HTTP_401_UNAUTHORIZED, "Login failed")

def credential_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )