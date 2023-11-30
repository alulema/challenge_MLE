from fastapi import Request, FastAPI
from pydantic import ValidationError
from starlette.responses import JSONResponse
from challenge.utils.exceptions import InvalidMonthValueException, InvalidTipoVueloValueException


# Define a function to add exception handlers to a FastAPI application.
def add_exception_handlers(app: FastAPI):
    # Handler for Pydantic validation errors.
    # This captures errors related to request body validation.
    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
        # Returns a JSON response with a 400 status code for invalid data.
        return JSONResponse(
            status_code=400,
            content={"message": "Invalid input data"}
        )

    # Handler for custom InvalidMonthValueException.
    # This is triggered when an invalid 'MES' value is encountered.
    @app.exception_handler(InvalidMonthValueException)
    async def invalid_month_exception_handler(request: Request, exc: InvalidMonthValueException):
        # Returns a JSON response with a 400 status code and a specific error message.
        return JSONResponse(
            status_code=400,
            content={"message": "Invalid input data: MES must be between 1 and 12"}
        )

    # Handler for custom InvalidTipoVueloValueException.
    # This is triggered when an invalid 'TIPOVUELO' value is encountered.
    @app.exception_handler(InvalidTipoVueloValueException)
    async def invalid_tipovuelo_exception_handler(request: Request, exc: InvalidTipoVueloValueException):
        # Returns a JSON response with a 400 status code and a specific error message.
        return JSONResponse(
            status_code=400,
            content={"message": "Invalid input data: TIPOVUELO must be 'N' or 'I'"}
        )

    # General exception handler for catching any other exceptions.
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        # Returns a JSON response with a 500 status code for unspecified server errors.
        return JSONResponse(
            status_code=500,
            content={"message": "Error processing request"}
        )
