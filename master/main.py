from fastapi import FastAPI
from ddtrace import tracer
from ddtrace.contrib.asgi import TraceMiddleware
from master.routers.cities import router as city_route
from master.routers.roles import router as role_router
from master.routers.sub_roles import router as sub_role_route


app = FastAPI(
    docs_url="/docs",
    title="Partner App",
    description="Partner onboarding and authentication",
    openapi_url="/openapi.json",
)


app.add_middleware(TraceMiddleware, tracer=tracer)
app.include_router(city_route)
app.include_router(role_router)
app.include_router(sub_role_route)


@app.get("/", tags=["Health"])
async def read_root() -> dict:
    return {"message": "Successfully connected to the API"}
