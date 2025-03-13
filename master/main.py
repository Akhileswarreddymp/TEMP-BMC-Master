from fastapi import FastAPI
from ddtrace import tracer
from ddtrace.contrib.asgi import TraceMiddleware
from master.routers.cities import router as city_route


app = FastAPI(
    docs_url="/docs",
    title="Partner App",
    description="Partner onboarding and authentication",
    openapi_url="/openapi.json",
)


app.add_middleware(TraceMiddleware, tracer=tracer)
app.include_router(city_route)

@app.get("/",tags=["Health"])
async def read_root() -> dict:
    return {"message": "Successfully connected to the API"}
