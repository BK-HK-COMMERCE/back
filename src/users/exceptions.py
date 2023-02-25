from fastapi import HTTPException, status


def user_not_found():
    return HTTPException(404, "User Not Found")


def login_fail():
    return HTTPException(status.HTTP_401_UNAUTHORIZED, "Login failed")

