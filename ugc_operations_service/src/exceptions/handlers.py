from async_fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import ValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse


def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


async def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"errors": exc.errors()}
    )
