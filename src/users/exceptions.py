from fastapi import HTTPException


def user_not_found():
    return HTTPException(404, "User Not Found")
