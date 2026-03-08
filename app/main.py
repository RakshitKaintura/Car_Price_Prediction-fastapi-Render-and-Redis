from fastapi import FastAPI # Essential import to fix the crash
from prometheus_fastapi_instrumentator import Instrumentator #
from app.api import routes_auth, routes_predict #
from app.middleware.logging_middleware import LoggingMiddleware #
from app.core.exceptions import register_exception_handlers #

# Initialize the FastAPI application
app = FastAPI(title='Car Price Prediction API') #

# Add custom logging middleware
app.add_middleware(LoggingMiddleware) #

# Include authentication and prediction routes
app.include_router(routes_auth.router, tags=['Auth']) #
app.include_router(routes_predict.router, tags=['Prediction']) #

# Expose Prometheus metrics at the /metrics endpoint
Instrumentator().instrument(app).expose(app) #

# Register global exception handlers
register_exception_handlers(app) #