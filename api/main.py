import traceback
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.routers import routers
from src.schemas.api_response import ApiResponse
from src.domain.exceptions import NotFound, Conflict, Unauthorized, InvalidData, Forbidden
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Minha API", version="1.0.0")

for router in routers:
    app.include_router(router)


EXCEPTION_STATUS_MAP = {
    NotFound: 404,
    Conflict: 409,
    Unauthorized: 401,
    Forbidden: 403,
    InvalidData: 422,
    ConnectionError: 503,
}

@app.middleware("http")
async def handle_domain_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except tuple(EXCEPTION_STATUS_MAP.keys()) as e:
        status_code = EXCEPTION_STATUS_MAP[type(e)]
        return JSONResponse(
            status_code=status_code,
            content=ApiResponse(success=False, data=None, error=str(e)).model_dump()
        )
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content=ApiResponse(success=False, data=None, error=str(e)).model_dump()
        )

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API rodando 🚀"}
