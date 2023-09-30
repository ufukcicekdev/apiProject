# errors.py

from fastapi import HTTPException

class InvalidAPIKeyError(Exception):
    def __init__(self, status_code=401, detail="Invalid API key. Please provide a valid API key."):
        self.status_code = status_code
        self.detail = detail
        super().__init__(self.detail)

class DatabaseError(HTTPException):
    def __init__(self, detail="Internal Server Error: Database error occurred."):
        super().__init__(status_code=500, detail=detail)

class UnexpectedError(HTTPException):
    def __init__(self, detail="Internal Server Error: An unexpected error occurred."):
        super().__init__(status_code=500, detail=detail)
