from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, requests, Response
from fastapi.responses import JSONResponse as JSONR


class ErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    async def dispatch(self, request: requests, call_next) -> Response | JSONR:
        return await super().dispatch(request, call_next)