import os
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import api.endpoint_router as endpoint_router

# Contains End_Points that exposes End-Points.

app = FastAPI(debug=True)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=[],
)


app.include_router(
    endpoint_router.router,
    prefix="/ttth",
    tags=["ttth"],
    responses={404: {"description": "Not found"}},
)


if __name__ == "__main__":
    PORT = "8000"
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', PORT)))
