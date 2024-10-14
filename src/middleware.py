import time
import logging
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger("uvicorn.access")
logger.disabled = True

def register_middleware(app: FastAPI):

    @app.middleware("http")
    async def custom_logging(request: Request, call_next):
        start_time = time.time()
        print("before", start_time)

        response = await call_next(request)
        
        processing_time = time.time() - start_time
        print("processed after",processing_time)

        message = f"{request.client.host}:{request.client.port} - {request.method} - {request.url.path} - {response.status_code} completed after {processing_time}s"

        print(message)
        return response
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
    
# Trusted Host Middleware
# To add the Trusted Host Middleware, you can do the following:


# from fastapi.middleware.trustedhost import TrustedHostMiddleware

# def register_middleware(app: FastAPI):
#     ...  # rest of the middleware code
#     app.add_middleware(
#         TrustedHostMiddleware,
#         allowed_hosts=["localhost", "127.0.0.1"],
#     )
# By doing so, we have imported the TrustedHostMiddleware and added it to our application. We have also specified which hosts are allowed to access our application.