from fastapi import FastAPI
from mangum import Mangum
from app.routes.health import router as health_router
from app.routes.dataextract_router import  router as dataextract_router
from app.exceptions.handlers import add_global_error_handler
from app.config.config import Base, init_db
from app.middleware.alb_auth import ALBCognitoAuth
from fastapi import Request
import logging
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
security = ALBCognitoAuth()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 App startup initiated.")
    engine = init_db()
    Base.metadata.create_all(bind=engine)
    logger.info("🚀 App startup end")


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if request.url.path in ["/health", "/public"]:
        request.state.skip_auth = True
    return await call_next(request)

# Add global error handler
add_global_error_handler(app)

# Include routers
app.include_router(health_router)
app.include_router(dataextract_router)

# Lambda handler
handler = Mangum(app)